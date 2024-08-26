from sqlalchemy.orm import Session

from main_machine_monitoring.database import orm_class
from main_machine_monitoring.database.db_setup import SessionLocal, get_db
from fastapi import status, HTTPException, Depends, APIRouter

from datetime import datetime

from main_machine_monitoring.pydantic_schema import request_schema


router = APIRouter(
    prefix="/remarks",
    tags=['remarks']
)


# CREATING machines
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(remark: request_schema.CreateRemark, db: Session = Depends(get_db)):
    print("Got new request at:", datetime.now())
    new_remark = orm_class.Remarks(**remark.dict())

    db.add(new_remark)
    db.commit()
    db.refresh(new_remark)
    return {"data": new_remark}

