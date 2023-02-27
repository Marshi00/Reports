Option Explicit

'declare all variables
Dim AccessObj
Dim wshshell
Dim fso
Dim strProjectFolder
Dim strFile


'create a file system object for file manipulation
Set fso = CreateObject("Scripting.FilesystemObject")

'get the program directory
strProjectFolder = fso.GetAbsolutePathName(".") & "\"


'     *************************************************************************************
'              Run split procedure
'
'check for existence of collection database
'if it doesn't exist, pop up message and abort
strFile = strProjectFolder & "DataSources.mde"
if NOT fso.FileExists(strFile) then
    strFile = strProjectFolder & "DataSources.mdb"
    if NOT fso.FileExists(strFile) then
        msgbox strFile & " not found --- aborting"
        fso = nothing
        wscript.quit
    end if
end if


'make an access instance and load the data collection database
Set AccessObj = CreateObject("Access.Application")
AccessObj.OpenCurrentDatabase strFile

'tell access to split the database

AccessObj.Run "SplitDatabase_fromAccess"
AccessObj.CloseCurrentDatabase
Set AccessObj = nothing

'finally, release the wshshell object
WshShell = nothing
