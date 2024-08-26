from datetime import datetime

from sqlalchemy import func

from main_machine_monitoring.database import orm_class
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, session
from main_machine_monitoring.database import db_setup
from main_machine_monitoring.database.db_setup import get_db
from main_machine_monitoring.database.orm_class import Live
from main_machine_monitoring.pydantic_schema.request_schema import ReportData

router = APIRouter(
    prefix="/report_data",
    tags=['report_data']
)


@router.get("/")
def get_average_for_date(
        machine_id: str,
        date: str,
        db: Session = Depends(get_db)
):
    # Convert date string to datetime object
    selected_date = datetime.strptime(date, "%Y-%m-%d")

    # Fetch live data for the selected machine and date
    live_data = db.query(Live).filter(
        Live.machine_id == machine_id,
        func.DATE(Live.created_at) == selected_date
    ).all()

    if live_data:
        total_current = sum(data.current for data in live_data)
        total_voltage = sum(data.voltage for data in live_data)
        data_count = len(live_data)

        avg_current = total_current / data_count
        avg_voltage = total_voltage / data_count

        report_data = ReportData(
            machine_id=machine_id,
            avg_current=avg_current,
            avg_voltage=avg_voltage
        )

        return report_data.dict()

    else:
        return {"message": "No data found for the specified date and machine ID."}


