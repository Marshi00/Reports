import os
import sys
import win32com.client

# set up some constants
TIMEOUT = 1700 # timeout in seconds for printing report
PRIORITY = 16384 # lower priority
REPORT_MDB = "DataPresentation_summary"
PRINT_SUBROUTINE = "AutoPrintReport_DailySummary"

# create a file system object for file manipulation
fso = win32com.client.Dispatch("Scripting.FileSystemObject")

#get the program directory
strProjectFolder = os.path.abspath(".") + "\\"

#check for existence of other VB script to kill a process
#if it doesn't exist, pop up message and abort
strFile = strProjectFolder + "Kill.vbs"
if not fso.FileExists(strFile):
    print("not found", strFile, "--- aborting")
    sys.exit()

#check for existence of other VB script to lower the priority of a process
#if it doesn't exist, pop up message and abort
strFile = strProjectFolder + "SetPrio.vbs"
if not fso.FileExists(strFile):
    print(strFile, "not found --- aborting")
    sys.exit()

#check for existence of collection database
#if it doesn't exist, pop up message and abort
strFile = strProjectFolder + report_mdb + ".mde"
if not fso.FileExists(strFile):
    strFile = strProjectFolder + report_mdb + ".mdb"
    if not fso.FileExists(strFile):
        print(strFile, "not found --- aborting")
        sys.exit()

#finished with fso
fso = None

#make an access instance and load the report presentation database
AccessObj = win32com.client.Dispatch("Access.Application")
AccessObj.OpenCurrentDatabase(strFile)

#get the process id of access
AccessObj.Run("GetProcId", ProcId)

#shell a vb script to kill the access object after a time
WshShell = win32com.client.Dispatch("WScript.Shell")
KillObj = WshShell.Exec("wscript \"" + strProjectFolder + "Kill.vbs\" " + str(ProcId) + " " + str(TIMEOUT))

#an error is generated intentionally if we kill the process due to timeout
try:
    #tell access to read the data then quit
    AccessObj.Run(PRINT_SUBROUTINE)
except Exception:
    #if the access object was killed, let the user know
    print("Process", ProcId, "- Killed")
else:
    KillObj.Terminate()
    AccessObj.CloseCurrentDatabase()
    AccessObj = None
    WshShell = None
