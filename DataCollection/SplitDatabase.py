import os
import win32com.client as win32

# create a file system object for file manipulation
fso = win32.Dispatch('Scripting.FileSystemObject')

# get the program directory
strProjectFolder = os.path.abspath('.') + '\\'

# check for existence of collection database
# if it doesn't exist, pop up message and abort
strFile = strProjectFolder + 'DataSources.mde'
if not fso.FileExists(strFile):
    strFile = strProjectFolder + 'DataSources.mdb'
    if not fso.FileExists(strFile):
        print(strFile + ' not found --- aborting')
        fso = None
        quit()

# make an Access instance and load the data collection database
access = win32.Dispatch('Access.Application')
access.OpenCurrentDatabase(strFile)

# tell Access to split the database
access.Run('SplitDatabase_fromAccess')
access.CloseCurrentDatabase()
access = None
