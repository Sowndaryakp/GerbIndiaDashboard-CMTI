from main_machine_monitoring.database import orm_class
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from main_machine_monitoring.database.db_setup import get_db

router = APIRouter(
    prefix="/logs",
    tags=['logs']
)


# get all log data
@router.get("/")
def test(db: Session = Depends(get_db)):
    # select * from vol_cur_logs
    vol_cur_logs = db.query(orm_class.Logs).all()
    return {"Data": vol_cur_logs}


