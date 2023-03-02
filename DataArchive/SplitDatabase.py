import os
import win32com.client

# declare all variables
wshshell = win32com.client.Dispatch("WScript.Shell")
fso = win32com.client.Dispatch("Scripting.FileSystemObject")
strProjectFolder = os.path.abspath(".") + "\\"
strFile = strProjectFolder + "DataSources.mde"

# check for existence of collection database
# if it doesn't exist, pop up message and abort
if not fso.FileExists(strFile):
    strFile = strProjectFolder + "DataSources.mdb"
    if not fso.FileExists(strFile):
        wshshell.Popup(strFile + " not found --- aborting")
        fso = None
        wshshell = None
        quit()

# make an access instance and load the data collection database
AccessObj = win32com.client.Dispatch("Access.Application")
AccessObj.OpenCurrentDatabase(strFile)

# tell access to split the database
AccessObj.Run("SplitDatabase_fromAccess")
AccessObj.CloseCurrentDatabase()
AccessObj = None

# finally, release the wshshell object
wshshell = None
