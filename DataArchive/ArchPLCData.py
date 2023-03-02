import os
import subprocess
import win32com.client as win32

# set up some constants
TIMEOUT = 1700  # timeout in seconds for collecting data
PRIORITY = 16384  # lower priority

# create a file system object for file manipulation
fso = win32.Dispatch("Scripting.FileSystemObject")

# get the program directory
strProjectFolder = os.path.abspath(".") + "\\"

# check for existence of other VB script to kill a process
# if it doesn't exist, pop up message and abort
strFile = strProjectFolder + "Kill.vbs"
if not fso.FileExists(strFile):
    print(strFile, "not found --- aborting")
    fso = None
    quit()

# check for existence of other VB script to lower the priority of a process
# if it doesn't exist, pop up message and abort
strFile = strProjectFolder + "SetPrio.vbs"
if not fso.FileExists(strFile):
    print(strFile, "not found --- aborting")
    fso = None
    quit()

# check for existence of archive database
# if it doesn't exist, pop up message and abort
strFile = strProjectFolder + "DataArchive.mde"
if not fso.FileExists(strFile):
    strFile = strProjectFolder + "DataArchive.mdb"
    if not fso.FileExists(strFile):
        print(strFile, "not found --- aborting")
        fso = None
        quit()

# finished with fso
fso = None

# make an access instance and load the data collection database
AccessObj = win32.Dispatch("Access.Application")
AccessObj.OpenCurrentDatabase(strFile)

# get the process id of access
AccessObj.Run("GetProcId", ProcId=None)

# shell a vb script to kill the access object after a time
kill_script_path = strProjectFolder + "Kill.vbs"
kill_process_cmd = "wscript \"" + kill_script_path + "\" " + str(ProcId) + " " + str(TIMEOUT)
kill_process_obj = subprocess.Popen(kill_process_cmd, shell=True)

# tell access to read the data then quit
AccessObj.Run("ArchiveData")

# if the access object was killed, let the user know
# otherwise stop the kill process, close the database and release the access object
if kill_process_obj.poll() is not None:
    print("Process ", ProcId, "- Killed")
else:
    kill_process_obj.terminate()
    AccessObj.CloseCurrentDatabase()
    AccessObj = None
    print("Data archiving complete.")
