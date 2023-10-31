from main_machine_monitoring.database import orm_class
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import has_inherited_table, Session
from main_machine_monitoring.database import db_setup
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/live_data",
    tags=['live_data']
)


# Fixing machine_name to "7D"

@router.get("/{machine_name}")
def root(machine_name: str, db: Session = Depends(db_setup.get_db)):
    try:
        # Query the Machine table to find the machine with the name "7D"
        machine = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == machine_name).first()

        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")

        # Query the LiveRecent table, joining with Machine table, to get recent data for the specified machine
        machine_name = db.query(orm_class.LiveRecent).filter(orm_class.LiveRecent.machine == machine).limit(20).all()

        return machine_name
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



