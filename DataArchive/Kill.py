import sys
import time
import win32com.client
import wmi

# declare the variables
ProcID = int(sys.argv[1])
TimeOut = int(sys.argv[2])
wshShell = win32com.client.Dispatch("WScript.Shell")
svc = wmi.WMI()

# sleep for the timeout period
time.sleep(TimeOut)

# get all tasks with the specified process id
strQuery = "Select * from Win32_Process where processid=" + str(ProcID)
colproc = svc.query(strQuery)

# if any such processes exist, terminate them
if len(colproc) != 0:
    for proc in colproc:
        proc.Terminate()
