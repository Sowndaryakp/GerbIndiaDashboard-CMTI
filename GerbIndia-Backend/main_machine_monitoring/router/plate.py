from sqlalchemy.orm import Session

from main_machine_monitoring.database import orm_class
from main_machine_monitoring.database.db_setup import SessionLocal, get_db
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/plate",
    tags=['plate']
)


# get all machines data
@router.get("/plate")
def test(db: Session = Depends(get_db)):
    # select * from machine
    plate = db.query(orm_class.Plate).all()
    return {"Data": plate}
