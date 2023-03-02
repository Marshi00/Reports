import win32com.client
import sys

# get the script arguments (process id and NewPrio in cryptic code)
ProcID = int(sys.argv[1])
NewPrio = int(sys.argv[2])

# get the security object to get a processes ID
wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

# get all tasks with the specified process id
procs = wmi.ExecQuery(f"Select * from Win32_Process where ProcessId = {ProcID}")

# if any such processes exist, set the priority
if len(procs) != 0:
    for proc in procs:
        proc.SetPriority(NewPrio)
