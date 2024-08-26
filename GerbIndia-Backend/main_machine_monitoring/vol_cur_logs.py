from collections import defaultdict

from sqlalchemy import event
from main_machine_monitoring.database.orm_class import LiveRecent, Logs
from main_machine_monitoring.database.db_setup import get_db
import asyncio


# Define a function to monitor existing live_recent data for changes in state and update vol_cur_logs
def monitor_existing_live_recent_state():
    # Dictionary to store last updated time for each machine's True state
    last_true_time = defaultdict(lambda: None)

    async def check_existing_live_recent_state():
        while True:
            # Get a database session
            db = next(get_db())

            # Query the existing LiveRecent table data
            existing_entries = db.query(LiveRecent).all()

            # Iterate through existing entries
            for entry in existing_entries:
                # Check if the state is True for each entry
                if entry.state:
                    # Get the current time
                    current_time = entry.created_at

                    # Check the last updated time for this machine's True state
                    last_updated = last_true_time[entry.machine_id]

                    if last_updated is None:
                        # If no previous timestamp exists, add it to the dictionary
                        last_true_time[entry.machine_id] = current_time
                    else:
                        # Calculate the time difference in seconds
                        time_difference = (current_time - last_updated).total_seconds()

                        if time_difference >= 5:
                            # Check if the entry already exists in vol_cur_logs
                            existing_log_entry = db.query(Logs).filter(
                                Logs.created_at == entry.created_at,
                                Logs.machine_id == entry.machine_id
                            ).first()

                            if not existing_log_entry:
                                # Log the data in vol_cur_logs
                                new_log_entry = Logs(current=entry.current, voltage=entry.voltage, created_at=entry.created_at, machine_id=entry.machine_id)
                                db.add(new_log_entry)
                                db.commit()

                            # Update the last updated time for this machine
                            last_true_time[entry.machine_id] = current_time

                else:
                    # Reset the last updated time if the state is False
                    last_true_time[entry.machine_id] = None

            # Commit changes to the database
            db.commit()

            # Wait for a certain interval before checking again (e.g., every 1 second)
            await asyncio.sleep(10)

    # Run the check_existing_live_recent_state function in the background as a task
    asyncio.create_task(check_existing_live_recent_state())