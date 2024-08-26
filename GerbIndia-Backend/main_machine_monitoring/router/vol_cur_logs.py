from sqlalchemy import desc

from main_machine_monitoring.database import orm_class
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from main_machine_monitoring.database.db_setup import get_db

router = APIRouter(
    prefix="/logs",
    tags=['logs']
)


@router.get("/{machine_name}")
def test(machine_name: str, db: Session = Depends(get_db)):
    machine = db.query(orm_class.Logs).filter(orm_class.Logs.machine_id == machine_name).order_by(
        desc(orm_class.Logs.created_at)).first()

    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    return {"detail": machine}



