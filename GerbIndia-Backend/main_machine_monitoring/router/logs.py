from main_machine_monitoring.database import orm_class
from main_machine_monitoring.database.db_setup import get_db
from main_machine_monitoring.database.orm_class import Machine, ShiftOp, Element, StandardData
from main_machine_monitoring.pydantic_schema import request_schema
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from main_machine_monitoring.database import db_setup
from datetime import datetime

from main_machine_monitoring.pydantic_schema.request_schema import LogsData

router = APIRouter(
    prefix="/for_log",
    tags=['for_log']
)


@router.get("/{machine_id}/{epoch_time}", response_model=LogsData)
def root(machine_id: str, epoch_time: int, db: Session = Depends(db_setup.get_db)):
    # Convert epoch time to a datetime timestamp
    timestamp = datetime.fromtimestamp(epoch_time)

    # Query machine table to get the machine's ID
    machine = db.query(Machine).filter(Machine.machine_id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine not found")

    # Query ShiftOp table to find the relevant shift for the machine at the given time
    shift_op = db.query(ShiftOp).filter(
        ShiftOp.machine_id == machine.id,
        ShiftOp.start_time <= timestamp,
        ShiftOp.end_time >= timestamp
    ).first()
    if not shift_op:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shift data not found")

    # Retrieve element ID from ShiftOp
    element_id = shift_op.element_id

    # Query Element table to get the type based on element ID
    element = db.query(Element).filter(Element.id == element_id).first()
    if not element:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Element not found")

    # Retrieve type name
    type_name = element.type

    # Query StandardData table to get the standard current and voltage for the type
    std_data = db.query(StandardData).filter(StandardData.type_id == type_name).first()
    if not std_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Standard data not found")

    # Create and return LogsData object
    logs_data = LogsData(
        low_std_curr=std_data.low_std_curr,
        high_std_curr=std_data.high_std_curr,
        low_std_vol=std_data.low_std_vol,
        high_std_vol=std_data.high_std_vol
    )
    return logs_data


