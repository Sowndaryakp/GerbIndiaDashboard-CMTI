from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from main_machine_monitoring.database.orm_class import Live, LiveRecent, Logs
import time
import random

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:siri2251105@localhost/gerb"

# Create the engine and bind it to the base
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
Base.metadata.bind = engine

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

machine_ids = ["7G", "7H", "7J", "7K", "7L", "27C", "27D", "27E"]
CHECK_THRESHOLD_INTERVAL = 30  # 1 minute in seconds


def create_and_insert_data():
    machine_ids = ["7G", "7H", "7J", "7K", "7L", "27C", "27D", "27E"]  # List of machine IDs
    CHECK_THRESHOLD_INTERVAL = 120  # Example interval, you can adjust this

    try:
        threshold_check_timer = 0  # Initialize the timer
        while True:
            for machine_id in machine_ids:
                if threshold_check_timer >= CHECK_THRESHOLD_INTERVAL:
                    # Generate random values for current and voltage
                    if machine_id == '7G':
                        current = 370  # Set current to 370 for machine ID '7G'
                        voltage = round(random.uniform(15, 35), 2)
                    elif machine_id == '7K':
                        current = 0  # Set current to 0 for machine ID '7K'
                        voltage = 0  # Set voltage to 0 for machine ID '7K'
                    else:
                        current = round(random.uniform(180, 270), 2)  # Set current between 180 to 270 for other IDs
                        voltage = round(random.uniform(15, 35), 2)
                else:
                    current = round(random.uniform(0, 0), 2)
                    voltage = round(random.uniform(0, 0), 2)

                with SessionLocal() as session:
                    try:
                        # Create new Live data
                        new_live_data = Live(machine_id=machine_id, current=current,
                                             voltage=voltage, created_at=datetime.now())

                        # Fetch or create LiveRecent data
                        live_recent_data = session.query(LiveRecent).filter_by(machine_id=machine_id).first()

                        if live_recent_data:
                            # Update existing LiveRecent data
                            live_recent_data.current = current
                            live_recent_data.voltage = voltage
                            live_recent_data.created_at = datetime.now()

                            # Set state based on conditions
                            if voltage > 35 or current > 300:
                                live_recent_data.state = True
                            else:
                                live_recent_data.state = False

                            # Set machine_state based on current and voltage values
                            live_recent_data.machine_state = bool(current != 0 or voltage != 0)
                        else:
                            # Create new LiveRecent data
                            new_live_recent_data = LiveRecent(machine_id=machine_id, current=current,
                                                              voltage=voltage, created_at=datetime.now())
                            # Set state based on conditions for new LiveRecent data
                            if voltage > 35 or current > 300:
                                new_live_recent_data.state = True
                            else:
                                new_live_recent_data.state = False

                            # Set machine_state based on current and voltage values
                            new_live_recent_data.machine_state = bool(current != 0 or voltage != 0)

                            session.add(new_live_recent_data)

                        # Add and commit changes to the session
                        session.add(new_live_data)
                        session.commit()

                        # Printing the inserted data details
                        print("Inserted Data for Machine ID:", machine_id)
                        print("ID:", new_live_data.id)
                        print("Current:", new_live_data.current)
                        print("Voltage:", new_live_data.voltage)
                        print("Created At:", new_live_data.created_at)

                    except Exception as e:
                        session.rollback()
                        print("Error:", e)
                    finally:
                        session.close()

            threshold_check_timer += 30
            time.sleep(1)

    except Exception as e:
        print("Error:", e)


create_and_insert_data()
