from main_machine_monitoring.database import orm_class
from main_machine_monitoring.pydantic_schema import request_schema
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import has_inherited_table, Session
from main_machine_monitoring.database import db_setup
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/elements",
    tags=['elements']
)


# CREATING elements
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(element: request_schema.CreateElement, db: Session = Depends(db_setup.get_db)):
    print("Got new request at:", datetime.now())

    new_element = orm_class.Element(**element.dict())

    db.add(new_element)
    db.commit()
    db.refresh(new_element)
    return new_element


# RETRIVING elements
@router.get("/{type}", response_model=request_schema.ReturnType)
def root(type: str, db: Session = Depends(db_setup.get_db)):
    type_name = db.query(orm_class.Element).filter(orm_class.Element.type == type).first()

    # if not found
    if not type_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the element with type:{type} not found")

    return type_name


# DELETING elements
@router.delete("/{type}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(type: str, db: Session = Depends(db_setup.get_db)):
    delete_element = db.query(orm_class.Element).filter(orm_class.Element.type == type)

    # if not found
    if delete_element.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"machine with type:{type} does not exsist")

    # if found
    delete_element.delete(synchronize_session=False)
    db.commit()
    return {"message": "element was deleted"}


x = [{"machine_1": {"voltage": 22, "curent": 2.2}},
     {"machine_2": {"voltage": 22, "curent": 2.2}}]
