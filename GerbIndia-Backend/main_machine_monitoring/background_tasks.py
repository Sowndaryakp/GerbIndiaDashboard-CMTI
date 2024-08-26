import asyncio
from fastapi import BackgroundTasks
from main_machine_monitoring.database.orm_class import State, LiveRecent, On, Production
from main_machine_monitoring.database.db_setup import get_db
from sqlalchemy import func
from datetime import datetime

last_processed_timestamp = datetime.utcnow()


class BackgroundTaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)


async def periodic_task():
    while True:
        # Your periodic task logic goes here
        print("Periodic task is running...")
        await asyncio.sleep(10)  # Wait for 10 seconds before the next execution


async def process_live_recent_entries(db):
    global last_processed_timestamp

    # Fetch new entries from LiveRecent based on the last processed timestamp
    if last_processed_timestamp is None:
        # Get the minimum timestamp from LiveRecent table if last_processed_timestamp is None
        last_processed_timestamp = db.query(func.min(LiveRecent.created_at)).scalar()

    new_live_recent_entries = db.query(LiveRecent).filter(LiveRecent.created_at > last_processed_timestamp).all()

    # Process the new entries against State ranges
    for entry in new_live_recent_entries:
        current_value = entry.current
        voltage_value = entry.voltage

        try:
            # Fetch all states to check against their respective ranges
            all_states = db.query(State).all()

            # Check against State ranges to determine the corresponding state
            for state in all_states:
                if state.state == 'IDLE':
                    if (state.start_range_current <= current_value <= state.end_range_current) \
                            and (state.start_range_voltage <= voltage_value <= state.end_range_voltage):
                        new_entry = On(current=current_value, voltage=voltage_value, machine_id=entry.machine_id)
                        db.add(new_entry)
                        entry.processed = True
                        break  # Exit the loop after processing the entry

                elif state.state == 'PRODUCTION':
                    if (state.start_range_current <= current_value <= state.end_range_current) \
                            or (state.start_range_voltage <= voltage_value <= state.end_range_voltage):
                        new_entry = Production(current=current_value, voltage=voltage_value, machine_id=entry.machine_id)
                        db.add(new_entry)
                        entry.processed = True
                        break  # Exit the loop after processing the entry

                else:
                    # Handle other states if needed
                    print("Handling logic for other states if necessary.")
                    continue

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error processing entry: {e}")

    # Commit the changes to the database
    db.commit()

    # Update the last processed timestamp to the latest entry's timestamp
    if new_live_recent_entries:
        last_processed_timestamp = max(entry.created_at for entry in new_live_recent_entries)


async def run_periodic_task(background_tasks: BackgroundTasks):
    while True:
        # Get a new DB session
        db = next(get_db())

        # Process LiveRecent entries
        await process_live_recent_entries(db)

        # Sleep for a specific interval before the next check
        await asyncio.sleep(1)  # Adjust the interval as needed (e.g., check every 60 seconds)

        # Close the DB session
        db.close()


def start_background_task():
    # To use the above functions, you can initiate and start the periodic task as follows:
    background_tasks = BackgroundTaskManager()
    background_tasks.add_task(periodic_task)  # Adding the periodic task to the background

    # Start the periodic task
    asyncio.create_task(run_periodic_task(background_tasks))


# Define the main function
def main():
    # Start the background task within an event loop
    asyncio.run(start_background_task())


if __name__ == "__main__":
    # Call the main function
    main()
