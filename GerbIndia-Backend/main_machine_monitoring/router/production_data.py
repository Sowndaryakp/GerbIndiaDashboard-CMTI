import logging
from datetime import datetime
from typing import List

import pytz

from sqlalchemy import and_, cast, Date

from main_machine_monitoring.database import orm_class
from fastapi import status, HTTPException, Depends, APIRouter, Query
from sqlalchemy.orm import Session
from main_machine_monitoring.database import db_setup
from main_machine_monitoring.database.db_setup import get_db
from main_machine_monitoring.database.orm_class import Live
from main_machine_monitoring.pydantic_schema.request_schema import LiveData

router = APIRouter(
    prefix="/production_data",
    tags=['production_data']
)


@router.get("/{machine_id}/{start_date}/{end_date}")
def get_production_data_by_date_range(
    machine_id: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(db_setup.get_db)
):
    try:
        # Convert string dates to datetime objects
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD format for dates.")

    try:
        production_data = db.query(orm_class.Production) \
            .filter(orm_class.Production.machine_id == machine_id) \
            .filter(
                cast(orm_class.Production.created_at, Date) >= start_datetime.date()
            ) \
            .filter(
                cast(orm_class.Production.created_at, Date) <= end_datetime.date()
            ) \
            .all()

        # Check if production data is empty
        if not production_data:
            raise HTTPException(status_code=404, detail=f"No production data found for machine_id: {machine_id}")

        return production_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/live-data/", response_model=List[LiveData])
def get_live_data(
        start_time: int,
        machine_id: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    start_datetime = datetime.utcfromtimestamp(start_time)

    live_data = db.query(Live).filter(
      Live.created_at >= start_datetime,
        Live.machine_id == machine_id
    ).order_by(Live.created_at).offset(skip).limit(limit).all()

    if not live_data:
        raise HTTPException(status_code=404, detail="No data found for the given parameters")

    return live_data