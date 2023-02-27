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
Const timeout = 1700 'timeout in seconds for printing report
Const Priority = 16384 'lower priority
Const report_mdb = "DataPresentation_summary"
Const print_subroutine = "AutoPrintReport_DailySummary"

'Sub PrintReports()

    'create a file system object for file manipulation
    Set fso = CreateObject("Scripting.FilesystemObject")

    'get the program directory
    strProjectFolder = fso.GetAbsolutePathName(".") & "\"

    'check for existence of other VB script to kill a process
    'if it doesn't exist, pop up message and abort
    strFile = strProjectFolder & "Kill.vbs"
    if NOT fso.FileExists(strFile) then
        msgbox "not found " & strFile & " --- aborting"
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

    'check for existence of collection database
    'if it doesn't exist, pop up message and abort
    strFile = strProjectFolder & report_mdb & ".mde"
    if NOT fso.FileExists(strFile) then
        strFile = strProjectFolder & report_mdb & ".mdb"
        if NOT fso.FileExists(strFile) then
            msgbox strFile & " not found --- aborting"
            fso = nothing
            wscript.quit
        end if
    end if

    'finished with fso
    Set fso = Nothing

    'make an access instance and load the report presentation database
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
	AccessObj.Run print_subroutine

    'if the access object was killed, let the user know
    if Err.Number=-2147023170 then
	msgbox "Process " & ProcId & " - Killed"
    else
	KillObj.Terminate
	AccessObj.CloseCurrentDatabase
	Set AccessObj = nothing
	WshShell = nothing
    end if

'End Sub