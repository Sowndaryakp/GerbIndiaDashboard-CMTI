import traceback
from datetime import datetime, timezone
from urllib.parse import unquote

from sqlalchemy import and_, func

from main_machine_monitoring.database import orm_class
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from main_machine_monitoring.database import db_setup
from main_machine_monitoring.pydantic_schema.request_schema import Edit, UpdateElement
from main_machine_monitoring.router.oauth2 import get_current_user

router = APIRouter(
    prefix="/edit",
    tags=['edit']
)


@router.put("/type/welder_name")
def update_data(element: Edit, machine_id: str, welder_name: str, type: str = Depends(unquote),
                db: Session = Depends(db_setup.get_db)):
    current_time = datetime.now()

    try:
        # Fetch machine_id, element_id, and operator_id
        machine = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == machine_id).first()
        element_data = db.query(orm_class.Element).filter(
            and_(orm_class.Element.type == type, orm_class.Element.is_active == True)).first()
        operator = db.query(orm_class.Welder).filter(
            and_(orm_class.Welder.welder_name == welder_name, orm_class.Welder.is_active == True)).first()

        if not all([machine, element_data, operator]):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Machine, Element, or Welder not found"
            )

        machine_id = machine.id
        element_id = element_data.id
        operator_id = operator.id

        # Find ShiftOp record where the current_time falls within the range
        shift_op_record = db.query(orm_class.ShiftOp).filter(
            and_(
                orm_class.ShiftOp.machine_id == machine_id,
                orm_class.ShiftOp.element_id == element_id,
                orm_class.ShiftOp.operator_id == operator_id,
                orm_class.ShiftOp.start_time <= current_time,
                orm_class.ShiftOp.end_time >= current_time
            )
        ).first()
        print("-------------------------------------------------------------------------------------------------------")
        print("Current Time:", current_time)
        print("Start Time:", shift_op_record.start_time if shift_op_record else None)
        print("End Time:", shift_op_record.end_time if shift_op_record else None)

        print("-------------------------------------------------------------------------------------------------------")
        if shift_op_record:
            # Update the found ShiftOp record with the provided project details
            shift_op_record.I_no = element.I_no
            shift_op_record.Fc_no = element.Fc_no
            shift_op_record.project = element.project

            remarks_id = shift_op_record.remarks_id
            remarks_record = db.query(orm_class.Remarks).filter(orm_class.Remarks.id == remarks_id).first()

            if remarks_record is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Remarks record not found"
                )

            # Update the found Remarks record with element.remarks
            remarks_record.Remarks = element.remarks

            plate_id = shift_op_record.plate_id
            plate_record = db.query(orm_class.Plate).filter(orm_class.Plate.id == plate_id).first()

            if plate_record is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Plate record not found"
                )

            # Update the found Plate record with the provided element data
            plate_record.plate_thickness = element.plate_thickness
            plate_record.plate_description = element.plate_description

            # Update the Element table with the provided element description and range
            db.query(orm_class.Element).filter(orm_class.Element.id == element_id).update({
                "element_description": element.element_description,
                "range": element.range
            }, synchronize_session=False)

            db.commit()
            return {"message": "Data updated successfully"}
        else:
            return {"message": "No ShiftOp record found for the current time range"}

    except Exception as e:
        db.rollback()  # Rollback changes to prevent partial updates
        return {"message": f"Failed to update data: {e}"}


# ---------------------------------------------------------------------------------------------------------------------

# updating elements
@router.put("/{type}")
def update_post(type: str, element: UpdateElement, db: Session = Depends(db_setup.get_db),
                user_id: int = Depends(get_current_user)):
    print("==============================================")
    print(user_id)
    print("==============================================")
    element_update_query = db.query(orm_class.Element).filter(orm_class.Element.type == type)
    update_element = element_update_query.first()

    # if not found
    if update_element is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"machine with type:{type} does not exsist")

    # if found
    element_update_query.update(element.dict(), synchronize_session=False)
    db.commit()
    return {"updated_element_is ": element_update_query.first()}
