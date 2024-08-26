import asyncio
import random
from datetime import datetime
from typing import List
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState
from fastapi import WebSocket
from main_machine_monitoring.database import orm_class
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from main_machine_monitoring.database.db_setup import get_db
from main_machine_monitoring.database.orm_class import LiveRecent
from main_machine_monitoring.pydantic_schema.request_schema import LiveRecentResponse

router = APIRouter(
    prefix="/machine_color",
    tags=['machine_color']
)


@router.get("/", response_model=List[LiveRecentResponse])
async def get_all_live_recent_data(db: Session = Depends(get_db)):
    records = db.query(orm_class.LiveRecent).all()

    return records
