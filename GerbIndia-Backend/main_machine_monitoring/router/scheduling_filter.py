from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from main_machine_monitoring.database import db_setup, orm_class
from main_machine_monitoring.pydantic_schema.request_schema import ShiftOpGet, ShiftOpGetnew

router = APIRouter(
    prefix="/scheduling_filter",
    tags=['scheduling_filter']
)


@router.get("/shift_ops", response_model=List[ShiftOpGet])
def get_shift_ops(
        machine_name: Optional[str] = None,
        welder_name: Optional[str] = None,
        specific_date: Optional[date] = None,
        db: Session = Depends(db_setup.get_db)
):
    try:
        query = db.query(orm_class.ShiftOp).join(orm_class.Machine)

        if machine_name:
            # Query the Machine table to find the machine with the specified machine_name
            machine = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == machine_name).first()
            if not machine:
                raise HTTPException(status_code=404, detail="Machine not found")
            # Filter ShiftOp by machine_id
            query = query.filter(orm_class.ShiftOp.machine_id == machine.id)

        if welder_name:
            # Query the Welder table to find the welder with the specified welder_name
            welder = db.query(orm_class.Welder).filter(orm_class.Welder.welder_name == welder_name).first()
            if not welder:
                raise HTTPException(status_code=404, detail="Welder not found")
            # Filter ShiftOp by operator_id (welder_id)
            query = query.filter(orm_class.ShiftOp.operator_id == welder.id)

        if specific_date:
            # Convert the date to datetime at the start and end of the day
            start_datetime = datetime.combine(specific_date, datetime.min.time())
            end_datetime = datetime.combine(specific_date, datetime.max.time())

            # Filter ShiftOp by checking if the specific_date is within the start_time and end_time
            query = query.filter(
                and_(
                    orm_class.ShiftOp.start_time <= end_datetime,
                    orm_class.ShiftOp.end_time >= start_datetime
                )
            )

        # Fetch the results
        shift_ops = query.all()

        if not shift_ops:
            raise HTTPException(status_code=404, detail="No ShiftOps found with the given criteria")

        # Create a List to store the results with additional information
        results = []

        # Iterate through the shift_ops and add information to the results List
        for shift_op in shift_ops:
            plate_info = db.query(orm_class.Plate).filter(orm_class.Plate.id == shift_op.plate_id).first()
            remarks_info = db.query(orm_class.Remarks).filter(orm_class.Remarks.id == shift_op.remarks_id).first()

            # Get the machine_name from the ShiftOp's related Machine
            machine_name_from_db = db.query(orm_class.Machine).filter(
                orm_class.Machine.id == shift_op.machine_id).first().machine_id

            result_item = ShiftOpGet(
                machine_name=machine_name_from_db,
                element_type=shift_op.element.type,
                operator_name=shift_op.welder.welder_name,
                start_time=shift_op.start_time,
                end_time=shift_op.end_time,
                I_no=shift_op.I_no,
                Fc_no=shift_op.Fc_no,
                project=shift_op.project,
                plate_thickness=plate_info.plate_thickness if plate_info else None,
                plate_description=plate_info.plate_description if plate_info else None,
                remarks=remarks_info.Remarks if remarks_info else None
            )
            results.append(result_item)

        # Return the results List
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

