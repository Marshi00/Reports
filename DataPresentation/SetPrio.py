import win32com.client
import sys
import time
import psutil

# get the script arguments (process id and NewPrio in cryptic code)
ProcID = int(sys.argv[1])
NewPrio = int(sys.argv[2])

# get all processes with the specified process id
procs = [p for p in psutil.process_iter(['pid', 'name']) if p.info['pid'] == ProcID]

# if any such processes exist, set the priority
if procs:
    for proc in procs:
        proc_obj = win32com.client.GetObject('winmgmts:').Get('Win32_Process.Handle="%d"' % proc.info['pid'])
        proc_obj.SetPriority(NewPrio)
