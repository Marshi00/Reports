"""This modified code uses the wait_until_midnight() function to wait until the next midnight before calling the
collect_data() function to collect data from the PLC and store it in the MySQL database. If the data collection
fails, the program will wait 30 minutes and try again until it successfully collects one reading per day. The loop
runs for 1008 iterations, which will cover a period of approximately 3 years.
"""
import mysql.connector
from pylogix import PLC
from datetime import datetime, timedelta
import time


# Define function to collect data from the PLC and store it in the database
def collect_data():
    # Initialize connection to the PLC
    with PLC() as comm:
        # Read values from PLC tags
        tag_values = comm.Read('MyTag1', 'MyTag2', 'MyTag3', 'MyTag4', 'MyTag5')

    # Open connection to the MySQL database
    cnx = mysql.connector.connect(user='user', password='password',
                                  host='host', database='database')
    cursor = cnx.cursor()

    # Insert values into the database
    add_data = ("INSERT INTO my_table "
                "(timestamp, tag1, tag2, tag3, tag4, tag5) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
    data = (datetime.now(), tag_values[0], tag_values[1], tag_values[2], tag_values[3], tag_values[4])
    cursor.execute(add_data, data)

    # Commit changes and close connections
    cnx.commit()
    cursor.close()
    cnx.close()


# Define function to wait until the next midnight
def wait_until_midnight():
    now = datetime.now()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time_to_wait = (midnight - now).total_seconds()
    time.sleep(time_to_wait)


# Define function to run the data collection routine
def run_data_collection():
    # Keep trying until we successfully collect one reading per day
    while True:
        # Wait until the next midnight
        wait_until_midnight()

        # Collect data and store it in the database
        try:
            collect_data()
            print("Data collected successfully.")
            return
        except Exception as e:
            print("Data collection failed: ", e)
            print("Retrying in 30 minutes...")
            time.sleep(1800)


# Run the data collection routine
for i in range(1008):
    run_data_collection()
