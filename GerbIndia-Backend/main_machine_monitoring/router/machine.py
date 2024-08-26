from main_machine_monitoring.database import orm_class
from main_machine_monitoring.pydantic_schema import request_schema
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from main_machine_monitoring.database.db_setup import get_db

from datetime import datetime

router = APIRouter(
    prefix="/machines",
    tags=['machines']
)


# CREATING machines
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(machine: request_schema.CreateMachine, db: Session = Depends(get_db)):
    print("Got new request at:", datetime.now())
    new_machine = orm_class.Machine(**machine.dict())

    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)
    return {"data": new_machine}


# RETRIVING machines
@router.get("/{model}")
def root(model: str, db: Session = Depends(get_db)):
    model_name = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == model).first()

    # if not found
    if not model_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the machine with model:{model} not found")

    # if found
    print(model_name)
    return {"detail": model_name}


# updating machines
@router.put("/{model}")
def update_post(model: str, machine: request_schema.UpdateMachine, db: Session = Depends(get_db)):
    machine_update_query = db.query(orm_class.Machine).filter(orm_class.Machine.model == model)
    update_machine = machine_update_query.first()

    # if not found
    if update_machine is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"machine with model:{model} does not exsist")

    # if found
    machine_update_query.update(machine.dict(), synchronize_session=False)
    db.commit()
    return {"updated_machine_is ": machine_update_query.first()}


# DELETING machines
@router.delete("/{model}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(model: str, db: Session = Depends(get_db)):
    delete_machine = db.query(orm_class.Machine).filter(orm_class.Machine.model == model)

    # if not found
    if delete_machine.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"machine with model:{model} does not exsist")

    # if found
    delete_machine.delete(synchronize_session=False)
    db.commit()
    return {"message": "machine was deleted"}


