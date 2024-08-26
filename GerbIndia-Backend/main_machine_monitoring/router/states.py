
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, APIRouter
from main_machine_monitoring.database.db_setup import get_db
from main_machine_monitoring.background_tasks import process_live_recent_entries

router = APIRouter(
)


# Define an endpoint to trigger the background task
@router.post("/process_live_recent")
async def trigger_processing_task(db: Session = Depends(get_db)):
    await process_live_recent_entries(db)
    return {"message": "Processing initiated"}
