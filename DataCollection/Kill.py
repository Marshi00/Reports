import win32com.client
import win32api
import win32con
import time
import sys
import os

# get the script arguments (process id and timeout in seconds)
ProcID = int(sys.argv[1])
Timeout = int(sys.argv[2])

# sleep for the timeout period
time.sleep(Timeout)

# get the security object to get a processes ID
wmi = win32com.client.GetObject("winmgmts:")
processes = wmi.InstancesOf('Win32_Process')

# find the process with the specified process id
for process in processes:
    if process.Properties_('ProcessID').Value == ProcID:
        # terminate the process
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, process.Properties_('ProcessID').Value)
        win32api.TerminateProcess(handle, 0)
        win32api.CloseHandle(handle)
        break
