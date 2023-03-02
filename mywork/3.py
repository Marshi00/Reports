"""
In this example, the database connection parameters are defined in a dictionary named db_config, and the PLC connection parameters are defined in a dictionary named plc_config. The tags list in the plc_config dictionary contains the names of up to 5 tags to be read from the PLC.

The MySQL database is connected to using the mysql.connector.connect() function, and a cursor is created to execute SQL statements. The PyLogix library is used to connect to the ControlLogix PLC and read the tag values.

For each day in the past 7 days, the date is calculated using the timedelta function, and the values of all the tags in the tags list are read from the PLC using a loop. The tag value for the current date is then stored in the MySQL database using an INSERT statement with the cursor.execute() function.

Note that you will need to have the PyLogix library and the mysql-connector-python library installed for this code to work. Also, make sure to replace the database connection parameters and PLC connection parameters with the appropriate values for your system.
"""
import mysql.connector
from datetime import datetime, timedelta
from pylogix import PLC

# Define the database connection parameters
db_config = {
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost',
    'database': 'mydatabase'
}

# Define the PLC connection parameters
plc_config = {
    'ip': '192.168.1.1',
    'tags': [
        'MyPLCTag1',
        'MyPLCTag2',
        'MyPLCTag3',
        'MyPLCTag4',
        'MyPLCTag5'
    ]
}

# Connect to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Connect to the ControlLogix PLC
with PLC() as plc:
    # Loop through the past 7 days
    for i in range(7):
        # Calculate the date for the current iteration
        date = datetime.now() - timedelta(days=i)

        # Loop through the tags and read their values from the PLC
        for tag in plc_config['tags']:
            # Read the value of the current tag from the PLC
            plc_data = plc.read(f'{tag}', datetime=date)

            # Store the tag value in the database
            cursor.execute("INSERT INTO TagData (Date, TagName, TagValue) VALUES (%s, %s, %s)",
                           (date.strftime('%Y-%m-%d %H:%M:%S'), tag, plc_data.value))

# Commit the changes to the database and close the connection
conn.commit()
conn.close()
