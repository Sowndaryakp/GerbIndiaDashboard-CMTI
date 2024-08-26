from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select, Integer, func, and_, or_, desc
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from datetime import datetime, timezone
from main_machine_monitoring.database import db_setup, orm_class
from main_machine_monitoring.pydantic_schema.request_schema import ShiftOpDisplay

router = APIRouter(
    prefix="/excel",
    tags=['excel']
)

@router.get("/", response_model=List[ShiftOpDisplay])
def root(
        start_time: str = Query(None),
        end_time: str = Query(None),
        machine_id: str = Query(None),
        welder_name: str = Query(None),
        type: str = Query(None),
        range: Optional[str] = Query(None),
        I_no: str = Query(None),
        Fc_no: str = Query(None),
        project: str = Query(None),
        db: Session = Depends(db_setup.get_db)
):
    try:
        current_time = datetime.now(timezone.utc)

        # Check if start_time and end_time are not None before parsing
        if start_time is not None:
            target_start_date = datetime.strptime(start_time, "%Y-%m-%d")
        else:
            target_start_date = datetime.min

        if end_time is not None:
            target_end_date = datetime.strptime(end_time, "%Y-%m-%d")
        else:
            target_end_date = datetime.max

        start_datetime = datetime.combine(target_start_date, datetime.min.time())
        end_datetime = datetime.combine(target_end_date, datetime.max.time())

        # Create a base query to retrieve ShiftOp entities with specified relationships
        base_query = (
            db.query(orm_class.ShiftOp)
                .options(
                    selectinload(orm_class.ShiftOp.machine),
                    selectinload(orm_class.ShiftOp.welder),
                    selectinload(orm_class.ShiftOp.element),
                )
                .filter(
                    and_(
                        orm_class.ShiftOp.start_time <= end_datetime,
                        orm_class.ShiftOp.end_time >= start_datetime
                    )
                )
        )

        # Apply filters based on provided query parameters
        if machine_id:
            base_query = base_query.filter(orm_class.ShiftOp.machine.has(orm_class.Machine.machine_id == machine_id))

        if welder_name:
            operator = db.query(orm_class.Welder).filter(
                and_(
                    orm_class.Welder.welder_name == welder_name,
                    orm_class.Welder.is_active == True
                )
            ).first()
            if not operator:
                raise HTTPException(status_code=404, detail=f"Welder '{welder_name}' not found or is inactive")
            base_query = base_query.filter(orm_class.ShiftOp.welder.has(orm_class.Welder.welder_name == welder_name))

        if type:
            element_type = db.query(orm_class.Element).filter(
                and_(
                    orm_class.Element.type == type,
                    orm_class.Element.is_active == True
                )
            ).first()
            if not element_type:
                raise HTTPException(status_code=404, detail=f"Element type '{type}' not found or is inactive")
            base_query = base_query.filter(orm_class.ShiftOp.element.has(orm_class.Element.type == type))

        if range:
            element_id = db.query(orm_class.Element.id).filter(orm_class.Element.range == range).scalar()
            if element_id:
                base_query = base_query.filter(orm_class.ShiftOp.element_id == element_id)
            else:
                return []

        if I_no or Fc_no or project:
            if I_no:
                base_query = base_query.filter(orm_class.ShiftOp.I_no == I_no)
            if Fc_no:
                base_query = base_query.filter(orm_class.ShiftOp.Fc_no == Fc_no)
            if project:
                base_query = base_query.filter(orm_class.ShiftOp.project == project)

        # Determine the order based on the presence of start_time
        if start_time:
            # Sort in ascending order if start_time is provided
            base_query = base_query.order_by(orm_class.ShiftOp.start_time)
        else:
            # Default behavior: sort in descending order
            base_query = base_query.order_by(desc(orm_class.ShiftOp.start_time))

        # Execute the query and retrieve the results
        shift_ops = base_query.all()

        if not shift_ops:
            raise HTTPException(status_code=404, detail="Not Found")

        results = []

        for shift_op in shift_ops:
            plate_details = db.query(orm_class.Plate).filter(orm_class.Plate.id == shift_op.plate_id).first()
            production_data = (
                db.query(orm_class.Production)
                    .filter(
                        orm_class.Production.machine_id == shift_op.machine.machine_id,
                        orm_class.Production.created_at >= shift_op.start_time,
                        orm_class.Production.created_at <= shift_op.end_time
                    )
                    .all()
            )

            highest_std_curr = db.query(func.max(orm_class.StandardData.high_std_curr)).scalar() or 0
            highest_std_vol = db.query(func.max(orm_class.StandardData.high_std_vol)).scalar() or 0

            current_threshold = highest_std_curr + 50
            voltage_threshold = highest_std_vol + 5

            valid_current_values = [prod.current for prod in production_data if prod.current <= current_threshold]
            valid_voltage_values = [prod.voltage for prod in production_data if prod.voltage <= voltage_threshold]

            average_current = round(float(sum(valid_current_values)) / len(valid_current_values), 2) if valid_current_values else None
            average_voltage = round(float(sum(valid_voltage_values)) / len(valid_voltage_values), 2) if valid_voltage_values else None

            all_current_values = [prod.current for prod in production_data]
            non_zero_current_values = [value for value in all_current_values if value != 0]
            min_current = min(non_zero_current_values) if non_zero_current_values else None
            max_current = max(non_zero_current_values) if non_zero_current_values else None

            all_voltage_values = [prod.voltage for prod in production_data]
            non_zero_voltage_values = [value for value in all_voltage_values if value != 0]
            min_voltage = min(non_zero_voltage_values) if non_zero_voltage_values else None
            max_voltage = max(non_zero_voltage_values) if non_zero_voltage_values else None

            result_item = ShiftOpDisplay(
                machine_id=shift_op.machine.machine_id,
                type=shift_op.element.type,
                welder_name=shift_op.welder.welder_name,
                start_time=shift_op.start_time,
                end_time=shift_op.end_time,
                I_no=shift_op.I_no,
                Fc_no=shift_op.Fc_no,
                project=shift_op.project,
                standard_current=shift_op.element.standard_current,
                standard_voltage=shift_op.element.standard_voltage,
                average_current=average_current,
                average_voltage=average_voltage,
                min_current=min_current,
                max_current=max_current,
                min_voltage=min_voltage,
                max_voltage=max_voltage,
                range=shift_op.element.range,
                plate_thickness=plate_details.plate_thickness,
                plate_description=plate_details.plate_description
            )
            results.append(result_item)

        if not results:
            raise HTTPException(status_code=404, detail="Not Found")

        return results

    except Exception as e:
        print(f"=== Exception ===")
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
