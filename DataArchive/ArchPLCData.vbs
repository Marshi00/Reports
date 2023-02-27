Option Explicit

'declare all variables
Dim AccessObj
Dim wshshell
Dim fso
Dim strProjectFolder
Dim strFile
Dim ProcID
Dim KillObj

'set up some constants
Const timeout = 1700 'timeout in seconds for collecting data
Const Priority = 16384 'lower priority

'Sub AchPLCData()

    'create a file system object for file manipulation
    Set fso = CreateObject("Scripting.FilesystemObject")

    'get the program directory
    strProjectFolder = fso.GetAbsolutePathName(".") & "\"

    'check for existence of other VB script to kill a process
    'if it doesn't exist, pop up message and abort
    strFile = strProjectFolder & "Kill.vbs"
    if NOT fso.FileExists(strFile) then
        msgbox strFile & " not found --- aborting"
        fso = nothing
        wscript.quit
    end if

    'check for existence of other VB script to lower the priority of a process
    'if it doesn't exist, pop up message and abort
    strFile = strProjectFolder & "SetPrio.vbs"
    if NOT fso.FileExists(strFile) then
        msgbox strFile & " not found --- aborting"
        fso = nothing
        wscript.quit
    end if

    'check for existence of archive database
    'if it doesn't exist, pop up message and abort
    strFile = strProjectFolder & "DataArchive.mde"
    if NOT fso.FileExists(strFile) then
        strFile = strProjectFolder & "DataArchive.mdb"
        if NOT fso.FileExists(strFile) then
            msgbox strFile & " not found --- aborting"
            fso = nothing
            wscript.quit
        end if
    end if

    'finished with fso
    Set fso = Nothing

    'make an access instance and load the data collection database
    Set AccessObj = CreateObject("Access.Application")
    AccessObj.OpenCurrentDatabase strFile

    'get the process id of access
    AccessObj.Run "GetProcId", ProcId

    'shell a vb script to kill the access object after a time
    set WshShell = WScript.CreateObject("WScript.Shell")
    set KillObj = WshShell.Exec("wscript """ & strProjectFolder & "Kill.vbs"" " & ProcId & " " & timeout)

    'an error is generated intentionally if we kill the process due to timeout
    On Error Resume Next

    'tell access to read the data then quit
    AccessObj.Run "ArchiveData"

    'if the access object was killed, let the user know
    'otherwise stop the kill process, close the database and release the access object
    if Err.Number=-2147023170 then
        msgbox "Process " & ProcId & " - Killed"
    else
        killObj.Terminate
        AccessObj.CloseCurrentDatabase
        Set AccessObj = nothing
    end if

    'finally, release the wshshell object
    WshShell = nothing

'End Sub
