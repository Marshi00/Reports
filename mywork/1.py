"""This code will attempt to collect data every 5 minutes for the past 7 days, and if it encounters any errors (such
as a failure to read data from the PLC or a failure to connect to the database), it will print an error message and
wait for 30 minutes before retrying.
"""

import mysql.connector
import datetime
import time

# Define MySQL database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)

# Define PLC connection
plc = ...  # Initialize PLC connection here

# Define tags to read from PLC
tags = ["tag1", "tag2", "tag3", "tag4", "tag5"]


# Define function to insert data into MySQL database
def insert_data(data):
    # Create cursor
    cursor = mydb.cursor()

    # Prepare query
    query = "INSERT INTO flow_data (timestamp, tag1, tag2, tag3, tag4, tag5) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data["timestamp"], data["tag1"], data["tag2"], data["tag3"], data["tag4"], data["tag5"])

    # Execute query
    cursor.execute(query, values)

    # Commit changes
    mydb.commit()

    # Print message
    print(f"Data inserted into database: {data}")


# Define function to read tags from PLC
def read_tags(tags):
    data = {}
    for tag in tags:
        value = plc.read(tag)
        if value is not None:
            data[tag] = value
        else:
            raise Exception(f"Failed to read value for tag: {tag}")
    return data


# Define function to run data collection process
def collect_data():
    try:
        # Get current timestamp
        timestamp = datetime.datetime.now()

        # Read tags from PLC
        data = read_tags(tags)

        # Add timestamp to data
        data["timestamp"] = timestamp

        # Insert data into MySQL database
        insert_data(data)

    except Exception as e:
        print(f"Error collecting data: {e}")

        # Wait for 30 minutes before retrying
        print("Waiting for 30 minutes before retrying...")
        time.sleep(1800)


# Run data collection process every 5 minutes for the past 7 days
for i in range(1008):
    collect_data()
    time.sleep(300)
