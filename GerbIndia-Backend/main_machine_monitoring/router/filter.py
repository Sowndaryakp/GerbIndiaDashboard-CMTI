from main_machine_monitoring.database import orm_class, db_setup
from main_machine_monitoring.pydantic_schema.request_schema import ShiftOpCreate, ShiftOpGet, ShiftOpUpdate, \
    ShiftOpDisplay
from fastapi import status, HTTPException, Depends, APIRouter
from main_machine_monitoring.database.orm_class import ShiftOp, Machine, Welder, Element
from sqlalchemy.orm import Session
from main_machine_monitoring.database.db_setup import get_db
from typing import List
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/filter",
    tags=['filter']
)


@router.get("/", response_model=List[ShiftOpDisplay])
def root(db: Session = Depends(db_setup.get_db)):
    try:
        # Query all ShiftOps without filtering by machine_id
        shift_ops = db.query(orm_class.ShiftOp).all()

        if not shift_ops:
            raise HTTPException(status_code=404, detail="No ShiftOps found")

        # Create a List to store the results with additional information
        results = []

        # Iterate through the shift_ops and add information to the results List
        for shift_op in shift_ops:
            machine_name = shift_op.machine.machine_id  # Assuming ShiftOp has a relationship with Machine
            result_item = ShiftOpGet(
                machine_name=machine_name,
                element_type=shift_op.element.type,  # Adjust this based on your data model
                operator_name=shift_op.welder.welder_name,  # Adjust this based on your data model
                start_time=shift_op.start_time,
                end_time=shift_op.end_time,

            )
            results.append(result_item)

        # Return the results List
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
