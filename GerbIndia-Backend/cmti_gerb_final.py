#!/usr/bin/env python3

from datetime import datetime, timezone
import time, calendar

import logging
import psycopg2
from pymodbus.client.sync import ModbusTcpClient
from tabulate import tabulate
import requests

print("runing....")
# Modbus device configuration for voltage values
modbus_ip = "192.168.0.24"
modbus_port = 502

# Modbus Voltage Register Addresses
modbus_voltage_registers = 4096

# Modbus Current Register Addresses
modbus_current_registers = 4104

machine_ids = ['7G', '7H', '7J', '7K', '7L', '27C', '27D', '27E']

machine_states = [False for i in range(len(machine_ids))]
machine_state = [False for i in range(len(machine_ids))]

def fetch_volcur_limits(epoch_time):
    data = []
    try:
        for i in machine_ids:
            response = requests.get(f"http://192.168.0.105:6969/for_log/{i}/{epoch_time}")
            data.append(response.json())
            
        return data 

    except requests.exceptions.RequestException as e:
        print(f'Error Fetching Data: {e}')
        return None
    finally:
        return data
    
# Function to read Modbus data from PLC for voltage values
def read_modbus_voltage_data(register_range):
    try:
        with ModbusTcpClient(modbus_ip, port=modbus_port) as client:
            response = client.read_holding_registers(register_range, 8, unit=1)
            values = response.registers
        data = dict(zip(machine_ids, values))
        return data

    except Exception as e:
        logger.error(f"Error reading Modbus voltage data: {e}")
        return None

# Function to read Modbus data from PLC for current values
def read_modbus_current_data(register_range):
    try:
        with ModbusTcpClient(modbus_ip, port=modbus_port) as client:
            response = client.read_holding_registers(register_range, 8, unit=1)
            values = response.registers
        data = dict(zip(machine_ids, values))
        return data

    except Exception as e:
        logger.error(f"Error reading Modbus current data: {e}")
        return None

# Database parameters
sleep_time = 1
database_connection_params = {
    "host": "192.168.0.105",
    "database": "gerb",
    "user": "postgres",
    "password": "siri2251105"
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(**database_connection_params)
    cur = conn.cursor()

    print('Database successfully connected!')

    # Create Vol_Cur_Logs table if not exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS public.live_data (
            id SERIAL PRIMARY KEY,
            machine_id VARCHAR(10), 
            time TIMESTAMP WITH TIME ZONE,
            voltage NUMERIC(6,2),
            current NUMERIC(6,2)
        )
    ''')
    conn.commit()

    print('Table Commit Successful')

    try:
        yag = None  # Initialize yag object outside of the try block

        while True:
            created_at = datetime.now(timezone.utc)
            current_data = read_modbus_current_data(modbus_current_registers)
            voltage_data = read_modbus_voltage_data(modbus_voltage_registers)   

            limits_data = fetch_volcur_limits(calendar.timegm(created_at.timetuple()))
            print(limits_data)
            # Replace undefined values with 0
            current_data = {key: value if 10 < value < 60000 else 0 for key, value in current_data.items()}
            voltage_data = {key: value if 10 < value < 60000 else 0 for key, value in voltage_data.items()}

            # Iterate over the machine_ids and insert data into 'live_data' table
            for i in range(len(machine_ids)):
                machine_id = machine_ids[i]
                current = current_data[machine_id]
                voltage = voltage_data[machine_id]

                try:
                    if(current >= limits_data[i]['high_std_curr'] or voltage >= limits_data[i]['high_std_vol'] or current >= limits_data[i]['low_std_curr'] or voltage >= limits_data[i]['low_std_vol']):
                        machine_states[i] = True
                except:
                    machine_states[i] = False

                # Modify the condition for displaying current
                current_display = current if current > 10 else 0

                if (current>50 or voltage>0):
                    machine_state[i] = True
                else:
                    machine_state[i] = False

                # Insert data into 'live_data' table
                cur.execute(
                    "INSERT INTO public.live_data (current, voltage, created_at, machine_id) VALUES (%s, %s, %s, %s) RETURNING id",
                    (current_display, voltage, created_at, machine_id)
                )
                cur.execute(
                'UPDATE public."Live_recent" '
                'SET current=%s, voltage=%s, created_at=%s, machine_id=%s, state=%s, machine_state=%s '
                'WHERE machine_id=%s',
                (current, voltage, created_at, machine_id, machine_states[i], machine_state[i],machine_id)
                )
            
            temp_limc = []
            temp_limv = []
            for i in range(len(machine_ids)):
                try:
                    temp_limc += [f'{limits_data[i]["low_std_curr"]}-{limits_data[i]["high_std_curr"]}']
                    temp_limv += [f'{limits_data[i]["low_std_vol"]}-{limits_data[i]["high_std_vol"]}']
                except:
                    temp_limc += ['None']
                    temp_limv += ['None']

            logger.info('\n'+tabulate([['Voltage in volts']+list(voltage_data.values()), 
                                       ['Current in amps']+list(current_data.values()),
                                       ['Machine State']+machine_state, 
                                       ['Voltage Range']+temp_limv,
                                       ['Current Range']+temp_limc,
                                       ['Alert State']+machine_states],
                                headers=['Machine ID']+machine_ids, tablefmt='grid'))
            logger.info('Time Stamp : '+created_at.strftime("%m/%d/%Y, %H:%M:%S")+'\n')

            conn.commit()
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        logger.info("Script interrupted by user.")
    finally:
        if yag:
            yag.close()  # Close yag object if it's defined
        cur.close()
        conn.close()

except psycopg2.Error as e:
    logger.error(f"Error connecting to the database: {e}")
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")
