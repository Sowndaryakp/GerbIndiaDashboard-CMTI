from main_machine_monitoring.database import orm_class, db_setup
from main_machine_monitoring.pydantic_schema.request_schema import ShiftOpCreate, ShiftOpGet, ShiftOpUpdate
from fastapi import status, HTTPException, Depends, APIRouter
from main_machine_monitoring.database.orm_class import ShiftOp, Machine, Welder, Element, Shift
from sqlalchemy.orm import Session
from main_machine_monitoring.database.db_setup import get_db
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import func, and_, TIME
from sqlalchemy.orm import aliased
from sqlalchemy import extract
from sqlalchemy import cast, TIMESTAMP
from sqlalchemy import String

router = APIRouter(
    prefix="/op_shift",
    tags=['op_shift']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(shift: ShiftOpCreate, db: Session = Depends(get_db)):
    print("Got a new request at:", datetime.now())

    # Convert the integer epoch timestamps to datetime objects
    start_time = datetime.utcfromtimestamp(shift.start_time)
    end_time = datetime.utcfromtimestamp(shift.end_time)

    # Calculate the duration based on the difference between start_time and end_time
    duration = (end_time - start_time).total_seconds() / 3600.0  # Calculate duration in hours

    # Define a timedelta representing 5 hours and 30 minutes
    time_to_add = timedelta(hours=5, minutes=30)

    # Add the timedelta to the original time
    start_time = start_time + time_to_add
    end_time = end_time + time_to_add

    print("========================")
    print(start_time)
    print(end_time)
    print("========================")

    # Convert datetime objects to PostgreSQL timestamp strings
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    shift_query = db.query(orm_class.Shift).filter(
        and_(
            orm_class.Shift.start_time <= start_time_str,
            orm_class.Shift.end_time >= end_time_str
        )
    ).first()

    if shift_query is None:
        # If no matching shift is found, raise an exception or handle it as needed
        raise HTTPException(status_code=400, detail="No matching shift found")

    operator_name = db.query(orm_class.Welder).filter(orm_class.Welder.welder_name == shift.operator_name).first()
    element_type = db.query(orm_class.Element).filter(orm_class.Element.type == shift.element_type).first()
    machine_name = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == shift.machine_name).first()

    # Create a new ShiftOp instance with the calculated duration and the found shift
    new_shift = orm_class.ShiftOp(
        operator_id=operator_name.id,
        element_id=element_type.id,
        machine_id=machine_name.id,
        start_time=start_time,  # Use the original start_time with date and time
        end_time=end_time,  # Use the original end_time with date and time
        duration=duration,
        shift=shift_query  # Assign the found shift instance
    )

    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)
    return {"data": new_shift}


@router.put("/shiftops/update")
def update_shift_ops(
    machine_id: str,
    operator_name: str,
    shift_op_update: ShiftOpUpdate,
    db: Session = Depends(get_db)
):
    print("Got a request to update ShiftOp records at:", datetime.now())

    # Find the machine by its machine_id
    machine = db.query(Machine).filter(Machine.machine_id == machine_id).first()

    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    # Query Welder records based on operator_name
    welder = db.query(Welder).filter(Welder.welder_name == operator_name).first()

    if not welder:
        raise HTTPException(status_code=404, detail="Welder not found")

    # Query Element records based on the provided element_type
    element = db.query(Element).filter(Element.type == shift_op_update.element_type).first()

    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    # Query ShiftOp records based on the provided machine and welder
    shift_op = db.query(ShiftOp).filter(
        ShiftOp.machine_id == machine.id,
        ShiftOp.operator_id == welder.id
    ).first()

    if not shift_op:
        raise HTTPException(status_code=404, detail="ShiftOp record not found")
    # Convert provided timestamps to time without time zone
    start_time = datetime.fromtimestamp(shift_op_update.start_time).time()
    end_time = datetime.fromtimestamp(shift_op_update.end_time).time()

    # Convert datetime objects to PostgreSQL timestamp strings
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    # Fetch the shift_id based on the transformed values
    shift = db.query(orm_class.Shift).filter(
        and_(
            orm_class.Shift.start_time <= start_time_str,
            orm_class.Shift.end_time >= end_time_str
        )
    ).first()

    # Convert epoch timestamps to datetime
    start_time = datetime.fromtimestamp(shift_op_update.start_time)
    end_time = datetime.fromtimestamp(shift_op_update.end_time)

    # Update the ShiftOp record
    shift_op.start_time = start_time
    shift_op.end_time = end_time

    # Update the element_id based on the provided element_type
    shift_op.element_id = element.id

    # Update the shift_id based on the fetched shift record
    shift_op.shift_id = shift.id

    # Calculate the duration in hours
    duration = (end_time - start_time).total_seconds() / 3600
    shift_op.duration = duration

    db.commit()
    db.refresh(shift_op)

    return {"message": "ShiftOp record updated successfully"}


@router.get("/{machine_name}", response_model=List[ShiftOpGet])
def root(machine_name: str, db: Session = Depends(db_setup.get_db)):
    try:
        # Query the Machine table to find the machine with the specified machine_name
        machine = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == machine_name).first()
        print("mc id", machine.id)
        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")

        # Query the ShiftOp table, filtering by machine_id based on the machine object's id
        shift_ops = db.query(orm_class.ShiftOp).filter(orm_class.ShiftOp.machine_id == machine.id).all()

        if not shift_ops:
            raise HTTPException(status_code=404, detail="ShiftOps for machine not found")

        # Create a list to store the results with additional information
        results = []

        # Iterate through the shift_ops and add information to the results list
        for shift_op in shift_ops:
            result_item = ShiftOpGet(
                machine_name=machine_name,
                element_type=shift_op.element.type,  # You can adjust this based on your data model
                operator_name=shift_op.welder.welder_name,  # You can adjust this based on your data model
                start_time=shift_op.start_time,
                end_time=shift_op.end_time,
                shift=shift_op.shift.shift
            )
            results.append(result_item)

        # Return the results list
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/")
def delete_shift_ops(
    machine_name: str,
    start_time: int,
    end_time: int,
    db: Session = Depends(get_db)
):
    print("Got a request to delete ShiftOp records at:", datetime.now())

    # Convert the integer epoch timestamps to datetime objects
    start_datetime = datetime.fromtimestamp(start_time)
    end_datetime = datetime.fromtimestamp(end_time)

    # print("..............................................................")
    # print(start_datetime)
    # print(end_datetime)
    # print("..............................................................")

    # Find the machine by its machine_name
    machine = db.query(Machine).filter(Machine.machine_id == machine_name).first()

    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    # Query ShiftOp records to delete based on machine, start_time, and end_time
    shift_ops_to_delete = db.query(ShiftOp).filter(
        ShiftOp.machine_id == machine.id,
        ShiftOp.start_time >= start_datetime,
        ShiftOp.end_time <= end_datetime
    ).all()

    if not shift_ops_to_delete:
        raise HTTPException(status_code=404, detail="No ShiftOp records found to delete")

    # Delete the ShiftOp records
    for shift_op in shift_ops_to_delete:
        db.delete(shift_op)

    # Commit the changes to the database to apply the deletion
    db.commit()

    return {"message": "ShiftOp records deleted successfully"}
