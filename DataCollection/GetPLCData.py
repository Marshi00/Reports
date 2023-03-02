import os
import subprocess
import sys
import win32com.client

# set up some constants
timeout = 1700 # timeout in seconds for collecting data
priority = 16384 # lower priority

def main():
    # get the program directory
    strProjectFolder = os.path.abspath(".\\")

    # check for existence of other Python script to kill a process
    # if it doesn't exist, pop up message and abort
    strFile = os.path.join(strProjectFolder, "Kill.py")
    if not os.path.exists(strFile):
        print(f"{strFile} not found --- aborting")
        sys.exit(1)

    # check for existence of other Python script to lower the priority of a process
    # if it doesn't exist, pop up message and abort
    strFile = os.path.join(strProjectFolder, "SetPrio.py")
    if not os.path.exists(strFile):
        print(f"{strFile} not found --- aborting")
        sys.exit(1)

    # check for existence of collection database
    # if it doesn't exist, pop up message and abort
    strFile = os.path.join(strProjectFolder, "DataSources.mde")
    if not os.path.exists(strFile):
        strFile = os.path.join(strProjectFolder, "DataSources.mdb")
        if not os.path.exists(strFile):
            print(f"{strFile} not found --- aborting")
            sys.exit(1)

    # make an Access instance and load the data collection database
    accessObj = win32com.client.Dispatch("Access.Application")
    accessObj.OpenCurrentDatabase(strFile)

    # get the process id of Access
    accessObj.Run("GetProcId")
    procID = accessObj.Application.Eval("ProcId")

    # set the priority of the process lower
    subprocess.call(["wscript", os.path.join(strProjectFolder, "SetPrio.vbs"), str(procID), str(priority)])

    # kill the Access object after a time
    subprocess.call(["wscript", os.path.join(strProjectFolder, "Kill.vbs"), str(procID), str(timeout)])

    # an error is generated intentionally if we kill the process due to timeout
    try:
        # tell Access to read the data then quit
        accessObj.Run("GetPLCData")
    except:
        # if the Access object was killed, let the user know
        # otherwise stop the kill process, close the database and release the Access object
        print(f"Process {procID} - Killed")
    else:
        subprocess.call(["taskkill", "/F", "/PID", str(procID)])
        accessObj.CloseCurrentDatabase()
        del accessObj

if __name__ == '__main__':
    main()
