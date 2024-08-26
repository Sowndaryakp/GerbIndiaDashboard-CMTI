from datetime import datetime
from typing import List, Dict, Optional

from fastapi import FastAPI, Depends, HTTPException, APIRouter, Query
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from starlette import status
from main_machine_monitoring.database.db_setup import get_db
from main_machine_monitoring.database.orm_class import Graph, Machine
from main_machine_monitoring.graph_tasks import update_graph_table
from main_machine_monitoring.pydantic_schema.request_schema import GraphDataResponse, ProductionGraphData

router = APIRouter(
    prefix="/graph",
    tags=['graph']
)


# Route to update the Graph table based on LiveRecent and State tables
@router.get("/update_graph_table")
def update_graph_table_route(db: Session = Depends(get_db)):
    try:
        update_graph_table(db)
        return {"message": "Graph table updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update Graph table: {str(e)}")


@router.get("/get_graph_data", response_model=GraphDataResponse)
def get_graph_data(db: Session = Depends(get_db)):
    try:
        # Fetch graph data with associated machine details
        graph_data = db.query(Graph).options(joinedload(Graph.machine)).all()

        # Initialize variables to find minimum timestamp
        min_timestamp = float('inf')
        output_data = []

        for graph in graph_data:
            # Convert start_time to epoch timestamp
            start_time_epoch = int(graph.start_time.timestamp()) * 1000
            # Convert end_time to epoch timestamp
            end_time_epoch = int(graph.end_time.timestamp()) * 1000
            # Calculate duration between epochs
            duration_seconds = end_time_epoch - start_time_epoch

            # Update minimum timestamp if a smaller timestamp is found
            if start_time_epoch < min_timestamp:
                min_timestamp = start_time_epoch

            item = {
                "name": graph.state,
                "value": [int(graph.machine.id), int(start_time_epoch), int(end_time_epoch), int(duration_seconds)],
                "itemStyle": {
                    "normal": {
                        "color": graph.color
                    }
                }
            }
            output_data.append(item)

        response = {
            "minimumTimestamp": min_timestamp if min_timestamp != float('inf') else None,
            "dataPoints": output_data
        }

        return response

    except Exception as e:
        error_message = {"error": str(e)}
        # Log the error message for debugging purposes
        print(f"Error occurred: {error_message}")
        # Return an error response with details
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.get("/get_production_data", response_model=GraphDataResponse)
def get_graph_data(machine_id: str = Query(...), date: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Convert date string to datetime object
        target_date = datetime.strptime(date, "%Y-%m-%d")

        # Extract the start and end of the target date
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = datetime.combine(target_date, datetime.max.time())

        # Fetch graph data with associated machine details filtered by the target date
        graph_data = db.query(Graph).options(joinedload(Graph.machine)) \
            .filter(
                and_(
                    Graph.machine_id == machine_id,
                    Graph.start_time >= start_of_day,
                    Graph.end_time <= end_of_day
                )
            ).all()

        # Initialize variables to find minimum timestamp
        min_timestamp = float('inf')
        if not graph_data:  # Check for no data found
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Data does not exist for the selected date range")

        output_data = []

        for graph in graph_data:
            # Convert start_time to epoch timestamp
            start_time_epoch = int(graph.start_time.timestamp()) * 1000
            # Convert end_time to epoch timestamp
            end_time_epoch = int(graph.end_time.timestamp()) * 1000
            # Calculate duration between epochs
            duration_seconds = end_time_epoch - start_time_epoch

            # Update minimum timestamp if a smaller timestamp is found
            if start_time_epoch < min_timestamp:
                min_timestamp = start_time_epoch

            item = {
                "name": graph.state,
                "value": [int(graph.machine.id), int(start_time_epoch), int(end_time_epoch), int(duration_seconds)],
                "itemStyle": {
                    "normal": {
                        "color": graph.color
                    }
                }
            }
            output_data.append(item)

        response = {
            "minimumTimestamp": min_timestamp if min_timestamp != float('inf') else None,
            "dataPoints": output_data
        }

        return response

    except Exception as e:
        error_message = {"error": str(e)}
        # Log the error message for debugging purposes
        print(f"Error occurred: {error_message}")
        # Return an error response with details
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Data does not exist for the selected date range")


@router.get("/get_production_end_data", response_model=List[ProductionGraphData])
def get_graph_data(
    machine_id: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        target_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        target_end_date = datetime.strptime(end_date, "%Y-%m-%d")

        start_of_day_start = datetime.combine(target_start_date, datetime.min.time())
        end_of_day_end = datetime.combine(target_end_date, datetime.max.time())

        print("------------------------------------------------")
        print(f"start_datetime: {start_of_day_start}")
        print(f"end_datetime: {end_of_day_end}")
        print("------------------------------------------------")

        graph_data = db.query(Graph).filter(
            and_(
                Graph.machine_id == machine_id,
                Graph.start_time >= start_of_day_start,
                Graph.end_time <= end_of_day_end
            )
        ).all()

        if not graph_data:  # Check for no data found
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Data does not exist for the selected date range")
        response_data = []

        for graph in graph_data:
            start_time_epoch = int(graph.start_time.timestamp())
            end_time_epoch = int(graph.end_time.timestamp())
            duration_seconds = end_time_epoch - start_time_epoch

            item = ProductionGraphData(
                machine_id=graph.machine_id,
                state=graph.state,
                duration=duration_seconds,
                start_time=datetime.fromtimestamp(start_time_epoch),
                end_time=datetime.fromtimestamp(end_time_epoch ),
            )
            response_data.append(item)

        return response_data

    except Exception as e:
        error_message = {"error": str(e)}
        print(f"Error occurred: {error_message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Data does not exist for the selected date range")



@router.get("/get_graph_data_new", response_model=GraphDataResponse)
def get_graph_data(
    start_time: Optional[int] = Query(None, description="Start time in epoch seconds"),
    end_time: Optional[int] = Query(None, description="End time in epoch seconds"),
    db: Session = Depends(get_db)
):
    try:
        # Convert epoch time to datetime if provided
        start_datetime = datetime.fromtimestamp(start_time) if start_time else None
        end_datetime = datetime.fromtimestamp(end_time) if end_time else None

        # Fetch graph data with associated machine details
        query = db.query(Graph).options(joinedload(Graph.machine))
        print(query)

        if start_datetime:
            query = query.filter(Graph.start_time >= start_datetime)
        if end_datetime:
            query = query.filter(Graph.end_time <= end_datetime)

        graph_data = query.all()

        # Log the retrieved graph data for debugging
        print("Retrieved graph data:", graph_data)

        # Initialize variables to find minimum timestamp
        min_timestamp = float('inf')
        output_data = []

        for graph in graph_data:
            # Convert start_time to epoch timestamp
            start_time_epoch = int(graph.start_time.timestamp())
            # Convert end_time to epoch timestamp
            end_time_epoch = int(graph.end_time.timestamp())
            # Calculate duration between epochs
            duration_seconds = end_time_epoch - start_time_epoch

            # Update minimum timestamp if a smaller timestamp is found
            if start_time_epoch < min_timestamp:
                min_timestamp = start_time_epoch

            item = {
                "name": graph.state,
                "value": [int(graph.machine.id), start_time_epoch, end_time_epoch, duration_seconds],
                "itemStyle": {
                    "normal": {
                        "color": graph.color
                    }
                }
            }
            output_data.append(item)

        response = {
            "minimumTimestamp": min_timestamp if min_timestamp != float('inf') else None,
            "dataPoints": output_data
        }

        # # Log the response structure for debugging
        # print("Response data:", response)

        return response

    except Exception as e:
        error_message = {"error": str(e)}
        # Log the error message for debugging purposes
        print(f"Error occurred: {error_message}")
        # Return an error response with details
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)