import asyncio
from datetime import datetime
from typing import List

from sqlalchemy import text, and_
from starlette import websockets
from starlette.websockets import WebSocket

from main_machine_monitoring.database import orm_class
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, session
from main_machine_monitoring.database import db_setup

router = APIRouter(
    prefix="/live_data",
    tags=['live_data']
)


# Fixing machine_name to "7D"

@router.get("/{machine_name}")
def root(machine_name: str, db: Session = Depends(db_setup.get_db)):
    try:
        machine = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == machine_name).first()

        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")

        recent_data = db.query(orm_class.LiveRecent).filter(orm_class.LiveRecent.machine == machine).limit(20).all()

        return recent_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/{machine_name}/ws")
async def websocket_endpoint(websocket: WebSocket, machine_name: str):
    await websocket.accept()

    try:
        # Your logic to fetch and send live recent data through WebSocket
        db = db_setup.get_db()
        machine = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == machine_name).first()

        if not machine:
            await websocket.send_text("Machine not found")
            return

        while True:
            recent_data = db.query(orm_class.LiveRecent).filter(orm_class.LiveRecent.machine == machine).limit(20).all()
            await websocket.send_json({"recent_data": recent_data})

            # Adjust the sleep time according to your requirement
            await asyncio.sleep(5)  # Send data every 5 seconds (adjust as needed)
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()


@router.get("/live_type/{machine_name}")
def root(machine_name: str, db: Session = Depends(db_setup.get_db)):
    try:
        # Query the Machine table to find the machine with the specified machine_name
        machine = db.query(orm_class.Machine).filter(orm_class.Machine.machine_id == machine_name).first()

        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")

        # Get the ID of the machine from the Machine table
        machine_id = machine.id

        # Get the LiveRecent data for the specified machine
        live_recent_data = db.query(orm_class.LiveRecent).filter(orm_class.LiveRecent.machine == machine).first()

        if not live_recent_data:
            raise HTTPException(status_code=404, detail="Live recent data not found for this machine")

        # Extract created_at timestamp, current, and voltage from live_recent_data
        created_at_timestamp = live_recent_data.created_at
        current = live_recent_data.current
        voltage = live_recent_data.voltage

        # Query the ShiftOp table to find the relevant shift based on created_at timestamp and machine_id
        relevant_shift = db.query(orm_class.ShiftOp).filter(
            and_(
                orm_class.ShiftOp.machine_id == machine_id,
                orm_class.ShiftOp.start_time <= created_at_timestamp,
                orm_class.ShiftOp.end_time >= created_at_timestamp
            )
        ).first()

        if not relevant_shift:
            raise HTTPException(status_code=404, detail="Shift data not found for this machine and timestamp")

        # Get the element_id from the relevant_shift
        element_id = relevant_shift.element_id

        # Query the Element table to get the element type
        element = db.query(orm_class.Element).filter(orm_class.Element.id == element_id).first()

        if not element:
            raise HTTPException(status_code=404, detail="Element data not found")

        element_type = element.type  # Assuming this provides the type (e.g., 'type-1')

        # Query the StandardData table to get all details for the element type
        std_cur_vol_data = db.query(orm_class.StandardData).filter(orm_class.StandardData.type_id == element_type).all()

        # Extracting the first set of standard data
        if std_cur_vol_data:
            first_data = std_cur_vol_data[0]
            low_std_curr = first_data.low_std_curr
            high_std_curr = first_data.high_std_curr
            low_std_vol = first_data.low_std_vol
            high_std_vol = first_data.high_std_vol
        else:
            low_std_curr = None
            high_std_curr = None
            low_std_vol = None
            high_std_vol = None

        # Construct the final response object
        response_data = [{
            "machine_id": machine_name,
            "created_at": created_at_timestamp,
            "current": current,
            "voltage": voltage,
            "element_type": element_type,
            "low_std_curr": low_std_curr,
            "high_std_curr": high_std_curr,
            "low_std_vol": low_std_vol,
            "high_std_vol": high_std_vol
        }]

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


