import logging
import traceback

from main_machine_monitoring.database import orm_class, db_setup
from main_machine_monitoring.pydantic_schema.request_schema import ShiftOpCreate, ShiftOpGet, ShiftOpUpdate, \
    ShiftOpDisplay, ShiftOpGetnew
from fastapi import status, HTTPException, Depends, APIRouter, Query
from main_machine_monitoring.database.orm_class import ShiftOp, Machine, Welder, Element, Plate, Remarks
from sqlalchemy.orm import Session
from main_machine_monitoring.database.db_setup import get_db
from typing import List, Optional
from datetime import datetime, timedelta, date
from sqlalchemy import and_, func, or_, DateTime, cast, text, desc

router = APIRouter(
    prefix="/op_shift",
    tags=['op_shift']
)
from sqlalchemy.orm import aliased


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(shift: ShiftOpCreate, db: Session = Depends(db_setup.get_db)):
    try:
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

        # Check if the machine exists in ShiftOp table and overlaps with the given time
        Machine = aliased(orm_class.Machine)
        existing_shift = db.query(orm_class.ShiftOp).join(Machine).filter(
            Machine.machine_id == shift.machine_name,
            or_(
                and_(
                    orm_class.ShiftOp.start_time <= start_time,
                    orm_class.ShiftOp.end_time >= start_time
                ),
                and_(
                    orm_class.ShiftOp.start_time <= end_time,
                    orm_class.ShiftOp.end_time >= end_time
                )
            )
        ).first()

        if existing_shift:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Shift already exists for the machine {shift.machine_name} from {existing_shift.start_time} to {existing_shift.end_time}")

        operator_name = db.query(orm_class.Welder).filter(
            orm_class.Welder.welder_name == shift.operator_name,
            orm_class.Welder.is_active == True
        ).first()

        if operator_name is None:
            print(f"Operator: {shift.operator_name} not found or is inactive")  # Debug print
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Operator either does not exist or is inactive")

        element_type = db.query(orm_class.Element).filter(orm_class.Element.type == shift.element_type).first()

        if element_type is None or not element_type.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Element either does not exist or is inactive")

        machine_name = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == shift.machine_name).first()

        plate_instance = orm_class.Plate(
            plate_thickness=shift.plate_thickness,
            plate_description=shift.plate_description,
            element_id=element_type.id
        )
        db.add(plate_instance)
        db.commit()
        db.refresh(plate_instance)

        remarks_instance = orm_class.Remarks(
            Remarks=shift.remarks,
            operator_id=operator_name.id
        )
        db.add(remarks_instance)
        db.commit()
        db.refresh(remarks_instance)

        new_shift = orm_class.ShiftOp(
            operator_id=operator_name.id,
            element_id=element_type.id,
            machine_id=machine_name.id,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            I_no=shift.I_no,  # Directly enter I_no from the request
            Fc_no=shift.Fc_no,  # Directly enter Fc_no from the request
            project=shift.project,  # Directly enter project from the request
            plate_id=plate_instance.id,
            remarks_id=remarks_instance.id
        )

        db.add(new_shift)
        db.commit()
        db.refresh(new_shift)

        return {"data": new_shift}  # Return just the new_shift data

    except HTTPException as http_error:
        raise http_error  # Raise the HTTPException to let FastAPI handle it

    except Exception as e:
        # Log the specific error message and traceback
        traceback.print_exc()  # This will print the traceback to the console
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error")


# UPDATINGGGGGG
@router.put("/shiftops/update")
def update_shift_ops(
        machine_id: str,
        operator_name: str,
        shift_op_update: ShiftOpUpdate,
        db: Session = Depends(get_db)
):
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

    # Convert provided timestamps to datetime
    start_time = datetime.fromtimestamp(shift_op_update.start_time)
    end_time = datetime.fromtimestamp(shift_op_update.end_time)

    # Query the ShiftOp record based on machine_id and welder_id
    shift_op = db.query(ShiftOp).filter(
        ShiftOp.machine_id == machine.id,
        ShiftOp.operator_id == welder.id
    ).first()

    if not shift_op:
        raise HTTPException(status_code=404, detail="ShiftOp record not found")

    # Update the ShiftOp record with the new values
    shift_op.start_time = start_time
    shift_op.end_time = end_time
    shift_op.element_id = element.id

    # Update I_no, Fc_no, and project directly in the ShiftOp record
    shift_op.I_no = shift_op_update.I_no
    shift_op.Fc_no = shift_op_update.Fc_no
    shift_op.project = shift_op_update.project

    # Calculate the duration in hours
    duration = (end_time - start_time).total_seconds() / 3600
    shift_op.duration = duration

    db.commit()
    db.refresh(shift_op)

    return {"message": "ShiftOp record updated successfully"}


@router.get("/{machine_name}", response_model=List[ShiftOpGet])
def get_shift_ops_by_machine(machine_name: str, db: Session = Depends(db_setup.get_db)):
    try:
        # Query the Machine table to find the machine with the specified machine_name
        machine = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == machine_name).first()

        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")

        # Get today's date
        today = date.today()

        # Query the ShiftOp table, filtering by machine_id based on the machine object's id
        shift_ops = db.query(orm_class.ShiftOp).filter(orm_class.ShiftOp.machine_id == machine.id).order_by(
            desc(func.date(orm_class.ShiftOp.start_time) == today),  # Prioritize today's data
            desc(orm_class.ShiftOp.start_time)  # Then sort by start_time in descending order
        ).all()

        if not shift_ops:
            raise HTTPException(status_code=404, detail="ShiftOps for machine not found")

        # Create a List to store the results with additional information
        results = []

        # Iterate through the shift_ops and add information to the results List
        for shift_op in shift_ops:
            # Fetch additional details based on project_id

            plate_info = db.query(orm_class.Plate).filter(orm_class.Plate.id == shift_op.plate_id).first()
            remarks_info = db.query(orm_class.Remarks).filter(orm_class.Remarks.id == shift_op.remarks_id).first()

            result_item = ShiftOpGet(
                machine_name=machine_name,
                element_type=shift_op.element.type,
                operator_name=shift_op.welder.welder_name,
                start_time=shift_op.start_time,
                end_time=shift_op.end_time,
                I_no=shift_op.I_no,  # Fetch I_no directly from ShiftOp
                Fc_no=shift_op.Fc_no,  # Fetch Fc_no directly from ShiftOp
                project=shift_op.project,  # Fetch project directly from ShiftOp
                plate_thickness=plate_info.plate_thickness if plate_info else None,
                plate_description=plate_info.plate_description if plate_info else None,
                remarks=remarks_info.Remarks if remarks_info else None
            )
            results.append(result_item)

        # Return the results List
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/")
def delete_shift_ops(
        machine_name: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        element_name: Optional[str] = None,
        operator_name: Optional[str] = None,
        I_no: Optional[str] = None,
        Fc_no: Optional[str] = None,
        project: Optional[str] = None,
        db: Session = Depends(get_db)
):
    print("Got a request to delete ShiftOp records at:", datetime.now())

    start_timestamp = int(start_time) if start_time else None
    end_timestamp = int(end_time) if end_time else None

    start_datetime = datetime.fromtimestamp(start_timestamp) if start_timestamp else None
    end_datetime = datetime.fromtimestamp(end_timestamp) if end_timestamp else None

    # Find the machine by its machine_name
    machine = db.query(Machine).filter(Machine.machine_id == machine_name).first()

    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    # Prepare filters for ShiftOp records based on machine_id, start_time, end_time, element_id, operator_id,
    # I_no, Fc_no, and project
    filters = [
        ShiftOp.machine_id == machine.id
    ]

    if start_datetime:
        filters.append(ShiftOp.start_time >= start_datetime)

    if end_datetime:
        filters.append(ShiftOp.end_time <= end_datetime)

    if element_name:
        element = db.query(Element).filter(Element.type == element_name).first()
        if element:
            filters.append(ShiftOp.element_id == element.id)
        else:
            raise HTTPException(status_code=404, detail="Element not found")

    if operator_name:
        welder = db.query(Welder).filter(Welder.welder_name == operator_name).first()
        if welder:
            filters.append(ShiftOp.operator_id == welder.id)
        else:
            raise HTTPException(status_code=404, detail="Welder not found")

    if I_no:
        filters.append(ShiftOp.I_no == I_no)

    if Fc_no:
        filters.append(ShiftOp.Fc_no == Fc_no)

    if project:
        filters.append(ShiftOp.project == project)

    # Query ShiftOp records to delete based on filters
    shift_ops_to_delete = db.query(ShiftOp).filter(*filters).all()

    if not shift_ops_to_delete:
        raise HTTPException(status_code=404, detail="No ShiftOp records found to delete")

    # Delete the ShiftOp records
    for shift_op in shift_ops_to_delete:
        db.delete(shift_op)

    # Commit the changes to the database to apply the deletion
    db.commit()

    return {"message": "ShiftOp records deleted successfully"}


@router.get("/", response_model=List[ShiftOpGet])
def get_shift_ops(db: Session = Depends(db_setup.get_db)):
    try:
        # Get today's date
        today = date.today()

        # Query all ShiftOps and order by whether the start_time is today, then by start_time in descending order
        shift_ops = db.query(orm_class.ShiftOp).order_by(
            desc(func.date(orm_class.ShiftOp.start_time) == today),  # Prioritize today's data
            desc(orm_class.ShiftOp.start_time)  # Then sort by start_time in descending order
        ).all()

        if not shift_ops:
            raise HTTPException(status_code=404, detail="No ShiftOps found")

        # Create a List to store the results with additional information
        results = []

        # Iterate through the shift_ops and add information to the results List
        for shift_op in shift_ops:
            plate_info = db.query(orm_class.Plate).filter(orm_class.Plate.id == shift_op.plate_id).first()
            remarks_info = db.query(orm_class.Remarks).filter(orm_class.Remarks.id == shift_op.remarks_id).first()

            result_item = ShiftOpGet(
                machine_name=shift_op.machine.machine_id,  # Assuming ShiftOp has a relationship with Machine
                element_type=shift_op.element.type,  # Adjust this based on your data model
                operator_name=shift_op.welder.welder_name,  # Adjust this based on your data model
                start_time=shift_op.start_time,
                end_time=shift_op.end_time,
                I_no=shift_op.I_no,  # Fetch I_no directly from ShiftOp
                Fc_no=shift_op.Fc_no,  # Fetch Fc_no directly from ShiftOp
                project=shift_op.project,  # Fetch project directly from ShiftOp
                plate_thickness=plate_info.plate_thickness if plate_info else None,
                plate_description=plate_info.plate_description if plate_info else None,
                remarks=remarks_info.Remarks if remarks_info else None
            )
            results.append(result_item)

        # Return the results List
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
