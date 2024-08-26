from sqlalchemy.orm import Session
from main_machine_monitoring.database.orm_class import LiveRecent, State, Graph
import logging

logger = logging.getLogger(__name__)


def update_graph_table(db: Session):
    live_recent_data = db.query(
        LiveRecent.machine_id, LiveRecent.current, LiveRecent.voltage, LiveRecent.created_at
    ).all()

    for data in live_recent_data:
        machine_id, current, voltage, created_at = data
        state_info = db.query(State.state).filter(
            State.start_range_current <= current,
            State.end_range_current >= current,
            State.start_range_voltage <= voltage,
            State.end_range_voltage >= voltage
        ).first()

        logger.info(f"Data from LiveRecent: {data}, State Info: {state_info}")

        last_graph_entry = db.query(Graph).filter_by(machine_id=machine_id).order_by(
            Graph.id.desc()
        ).first()

        if last_graph_entry:
            if state_info and last_graph_entry.state != state_info[0]:
                logger.info(f"State changed: {last_graph_entry.state} -> {state_info[0]}")

                # Update the end time and duration of the existing entry if state changes
                last_graph_entry.end_time = created_at
                duration_seconds = (last_graph_entry.end_time - last_graph_entry.start_time).total_seconds()
                duration_minutes = duration_seconds / 60  # Convert seconds to minutes
                last_graph_entry.duration = duration_minutes if duration_seconds else 0.0

                db.add(last_graph_entry)

                # Create a new entry for the changed state
                new_graph_entry = Graph(
                    machine_id=machine_id,
                    start_time=created_at,
                    end_time=created_at,
                    state=state_info[0] if state_info and state_info[0] else "default_state", # Set default state if
                    # None
                    duration=0.0,
                    color="default_color"  # Replace with an appropriate default color value
                )

                # Fetch color based on state from check_state table
                state_color = db.query(State.color).filter(State.state == state_info[0]).scalar()
                new_graph_entry.color = state_color if state_color else "default_color"  # Set default color if None

                db.add(new_graph_entry)
            else:
                logger.info("State remains the same. Not updating.")

        else:
            new_graph_entry = Graph(
                machine_id=machine_id,
                start_time=created_at,
                end_time=created_at,
                state=state_info[0] if state_info and state_info[0] else "default_state",  # Set default state if None
                duration=0.0,
                color="default_color"  # Replace with an appropriate default color value
            )

            # Fetch color based on state from check_state table
            state_color = db.query(State.color).filter(State.state == state_info[0]).scalar()
            new_graph_entry.color = state_color if state_color else "default_color"  # Set default color if None

            db.add(new_graph_entry)

    db.commit()
    logger.info("Committing changes to the database")
