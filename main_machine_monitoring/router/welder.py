from main_machine_monitoring.database import orm_class
from main_machine_monitoring.pydantic_schema import request_schema
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import has_inherited_table, Session
from main_machine_monitoring.database import db_setup
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/welder",
    tags=['welder']
)


@router.get("/")
def test(db: Session = Depends(db_setup.get_db)):
    # select * from machine
    welders = db.query(orm_class.Welder).all()
    return {"Data": welders}


# CREATING elements
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(welder: request_schema.CreateWelder, db: Session = Depends(db_setup.get_db)):
    print("Got new request at:", datetime.now())

    new_welder = orm_class.Welder(**welder.dict())

    db.add(new_welder)
    db.commit()
    db.refresh(new_welder)
    return new_welder


# RETRIVING
@router.get("/{welder_name}", response_model=request_schema.ReturnWelder)
def root(welder_name: str, db: Session = Depends(db_setup.get_db)):
    name = db.query(orm_class.Welder).filter(orm_class.Welder.welder_name == welder_name).first()

    # if not found
    if not name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the welder with name:{welder_name} not found")

    return name


@router.put("/{welder_name}")
def update_post(welder_name: str, welder: request_schema.UpdateWelder, db: Session = Depends(db_setup.get_db)):
    welder_update_query = db.query(orm_class.Welder).filter(orm_class.Welder.welder_name == welder_name)

    update_welder = welder_update_query.first()

    # if not found
    if update_welder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,

                            detail=f"welder {welder_name} does not exist")
    welder_update_query.update(welder.dict(), synchronize_session=False)
    db.commit()

    return {"updated"}

