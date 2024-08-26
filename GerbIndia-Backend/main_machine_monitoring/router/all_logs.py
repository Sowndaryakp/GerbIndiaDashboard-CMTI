from sqlalchemy import desc

from main_machine_monitoring.database import orm_class
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from main_machine_monitoring.database.db_setup import get_db
from datetime import datetime



router = APIRouter(
    prefix="/all_logs",
    tags=['all_logs']
)


@router.get("/{machine_name}/{start_date}/{end_date}")
def test(machine_name: str, start_date: str, end_date: str , db: Session = Depends(get_db)):
    query = db.query(orm_class.Logs).filter(orm_class.Logs.machine_id == machine_name)

    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(orm_class.Logs.created_at >= start_datetime)

    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        # Assuming you want records up to the end of the specified date (e.g., up to 23:59:59)
        end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
        query = query.filter(orm_class.Logs.created_at <= end_datetime)

    machines = query.order_by(desc(orm_class.Logs.created_at)).all()

    if not machines:
        raise HTTPException(status_code=404, detail="No data found")

    return {"detail": machines}