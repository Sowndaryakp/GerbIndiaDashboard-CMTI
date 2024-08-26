import asyncio
import json
import subprocess
from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from main_machine_monitoring.database import orm_class
from main_machine_monitoring.database.db_setup import engine, get_db
from main_machine_monitoring.router import element, machine, live_data, welder, edit, auth, users, \
    op_shift, vol_cur_logs, all_logs, states, graph, report, remarks, excel, logs, production_data, \
    machine_color, plate, instruction, scheduling_filter
from main_machine_monitoring.background_tasks import BackgroundTaskManager, run_periodic_task, periodic_task
from main_machine_monitoring.graph_tasks import update_graph_table
from main_machine_monitoring.vol_cur_logs import monitor_existing_live_recent_state

orm_class.Base.metadata.create_all(bind=engine)

app = FastAPI()
background_tasks = BackgroundTaskManager()  # Create an instance of BackgroundTaskManager

ALLOWED_ORIGINS = ["*"]
# ALLOWED_ORIGINS = ["http://localhost:8080", "http://172.18.20.27:8080", "http://172.18.20.27"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# get all machines data
@app.get("/machines")
def test(db: Session = Depends(get_db)):
    # select * from machine
    machines = db.query(orm_class.Machine).all()
    return {"Data": machines}


# get all elements data

@app.get("/elements")
def test(db: Session = Depends(get_db)):
    # Filter active elements from the database
    active_elements = db.query(orm_class.Element).filter(orm_class.Element.is_active == True).all()

    # Map active elements to a dictionary excluding the 'is_active' field
    elements_data = [
        {k: v for k, v in element.__dict__.items() if k != '_sa_instance_state' and k != 'is_active'}
        for element in active_elements
    ]

    return {"Data": elements_data}


# getting the router
app.include_router(element.router)
app.include_router(machine.router)
app.include_router(live_data.router)
app.include_router(welder.router)
app.include_router(edit.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(op_shift.router)
# app.include_router(shift.router)
app.include_router(vol_cur_logs.router)
app.include_router(all_logs.router)
app.include_router(states.router)
app.include_router(graph.router)
app.include_router(report.router)
app.include_router(excel.router)
app.include_router(logs.router)
app.include_router(production_data.router)
app.include_router(machine_color.router)
app.include_router(remarks.router)
app.include_router(plate.router)
app.include_router(instruction.router)
app.include_router(scheduling_filter.router)



# Define an async function to start the app and background tasks
async def start_app():
    # Additional startup logic if required

    # Start monitoring existing LiveRecent state for vol_cur_logs update
    monitor_existing_live_recent_state()

    # Start background tasks
    await start_background_tasks()


# Define an async function to start the background tasks
async def start_background_tasks():
    asyncio.create_task(run_periodic_task(background_tasks))

    # Start the periodic task in the background
    background_tasks.add_task(periodic_task)

    async def run_update_graph_task():
        while True:
            db = next(get_db())  # Access the database session
            update_graph_table(db)
            await asyncio.sleep(10)  # Adjust the interval as needed (e.g., 10 seconds)

    background_tasks.add_task(run_update_graph_task)  # Add the task to the manager
    asyncio.create_task(run_update_graph_task())  # Start the periodic task in the background

    # Add the update_graph_table function to the background tasks to execute periodically or as needed
    background_tasks.add_task(run_update_graph_task)


# Define a function to fetch live recent data from the database
def fetch_live_recent_data(db: Session) -> list:
    live_recent_data = (
        db.query(orm_class.LiveRecent).order_by(orm_class.LiveRecent.id.desc()).all()
    )

    data_list = []
    for entry in live_recent_data:
        data_dict = {
            "id": entry.id,
            "current": entry.current,
            "voltage": entry.voltage,
            "created_at": entry.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Convert to string
            "state": entry.state,
            "machine_state": entry.machine_state,
            "machine_id": entry.machine_id
        }
        data_list.append(data_dict)

    return data_list


websocket_clients: List[WebSocket] = []


# Define a WebSocket endpoint for live recent data updates
@app.websocket("/live_recent_ws")
async def live_recent_websocket(websockets: WebSocket, db: Session = Depends(get_db)):
    await websockets.accept()
    websocket_clients.append(websockets)  # Append the connected client to the list

    try:
        while True:
            # Fetch LiveRecent data from the database using the provided function
            live_recent_data = fetch_live_recent_data(db)  # Pass the database session 'db' here

            # Convert the data to JSON format
            json_data = json.dumps(live_recent_data)
            print(json_data)

            # Send the JSON data to all connected clients
            for client in websocket_clients:
                print("Websoket data is being sent to the client")
                await client.send_text(json_data)
                print(json_data)
                print("sent")

            # Wait for 2 seconds before sending the next update
            await asyncio.sleep(2)

    except Exception as e:
        print(f"Error in websockets connection: {e}")

    finally:
        # Remove the websockets client when the connection is closed
        websocket_clients.remove(websockets)


# Define the main function to start the app
async def main():
    # Start the FastAPI application
    await start_app()

    # Run the cmti_gerb_final.py script
    subprocess.Popen(["python3", r"D:\siri\codes\pycharm\projects\gerb_project\main\cmti_gerb_final.py"])

    # Run the FastAPI app using uvicorn
    uvicorn_config = uvicorn.Config(app, reload=True, host="172.18.100.240", port=6969)
    server = uvicorn.Server(uvicorn_config)
    await server.serve()



if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())

# uvicorn main:app --reload --host 172.18.100.240 --port 6969
# uvicorn main:app --reload --host 172.18.100.54 --port 6969