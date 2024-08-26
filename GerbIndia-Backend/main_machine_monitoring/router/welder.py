from typing import List

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from main_machine_monitoring.database import orm_class
from main_machine_monitoring.database.orm_class import ShiftOp, Welder, Remarks
from main_machine_monitoring.pydantic_schema import request_schema
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, selectinload
from main_machine_monitoring.database import db_setup
from datetime import datetime

from main_machine_monitoring.pydantic_schema.request_schema import GetWelder

router = APIRouter(
    prefix="/welder",
    tags=['welder']
)


@router.get("/", response_model=List[GetWelder])
def test(db: Session = Depends(db_setup.get_db)):
    # Select active welders from the database
    active_welders = db.query(orm_class.Welder).filter(orm_class.Welder.is_active == True).all()

    # Filter and map the active welders to the GetWelder model
    active_welders_mapped = [
        GetWelder(
            welder_name=welder.welder_name,
            welder_number=welder.welder_number,
            date_of_joining=welder.date_of_joining,
            welder_qualification=welder.welder_qualification,
            qualified_thickness=welder.qualified_thickness
        )
        for welder in active_welders
    ]

    return active_welders_mapped


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(welder: request_schema.CreateWelder, db: Session = Depends(db_setup.get_db)):
    existing_welder = db.query(orm_class.Welder).filter(orm_class.Welder.welder_number == welder.welder_number).first()

    if existing_welder:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Welder with number {welder.welder_number} already exists."
        )

    new_welder = orm_class.Welder(**welder.dict())

    db.add(new_welder)
    db.commit()
    db.refresh(new_welder)
    return new_welder


@router.put("/{welder_name}")
def update_post(welder_number: int , welder: request_schema.UpdateWelder, db: Session = Depends(db_setup.get_db)):
    try:
        welder_update_query = db.query(orm_class.Welder).filter(orm_class.Welder.welder_number == welder_number)
        update_welder = welder_update_query.first()

        if update_welder is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Welder {welder_number} does not exist"
            )

        welder_update_query.update(welder.dict(), synchronize_session=False)
        db.commit()

        return {"updated"}

    except IntegrityError as e:
        db.rollback()
        if "Welder details_welder_number_key" in str(e):
            # Here, you catch the specific IntegrityError related to the unique constraint violation
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Welder with number {welder.welder_number} already exists."
            )
        else:
            # For other IntegrityErrors or unexpected errors, you can provide a generic message
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the welder details."
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update welder details: {e}"
        )


@router.delete("/{welder_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(welder_number: int, db: Session = Depends(db_setup.get_db)):
    welder = db.query(orm_class.Welder).filter(orm_class.Welder.welder_number == welder_number).first()

    # Check if the welder exists
    if welder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Welder with name '{welder_number}' does not exist")

    # Soft delete: Mark the welder as inactive
    welder.is_active = False
    db.commit()
    return {"message": "Welder record marked as inactive"}
