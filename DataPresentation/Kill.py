import sys
import time
import win32com.client

# get the script arguments (process id and timeout in seconds)
ProcID = int(sys.argv[1])
TimeOut = int(sys.argv[2])

# sleep for the timeout period
time.sleep(TimeOut)

# get all tasks with the specified process id
wmi = win32com.client.GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
query = "SELECT * FROM Win32_Process WHERE ProcessId = {}".format(ProcID)
colproc = wmi.ExecQuery(query)

# if any such processes exist, terminate them
if len(colproc) != 0:
    for proc in colproc:
        proc.Terminate()

