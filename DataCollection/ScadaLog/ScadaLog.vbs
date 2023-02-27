Option Explicit

'declare the variables
Dim fso
Dim strProjectFolder
Dim csvFile
Dim objArgs
Dim FileName
Dim logFile


Set objArgs = WScript.Arguments
FileName=objArgs(0)

Const SCADALog = "c:\progra~1\scadalog\SCADALog.exe"
Const LogFileName = "CollectData.log"

'Sub ScadaLog()

    'get a file system object for file stuff
    Set fso=CreateObject("Scripting.FilesystemObject")

    'if the scadalog program doesn't exist, pop a msgbox and abort
    If NOT fso.FileExists(SCADALog) then
       msgbox SCADALog & " can't be found --- aborting"
       set fso = nothing
       wscript.quit
    End if

    'get the current directory
    strProjectFolder = fso.GetAbsolutePathName(".") & "\"

    'delete the error log file if it exists
    If fso.FileExists(LogFileName) then
       Set logFile = fso.GetFile(LogFileName)
       logFile.delete
    End if

    'create the error log file
    Set logFile = fso.OpenTextFile(LogFileName, 8, True)

    'read the data
    Call SCADALogLaunch(300, FileName & ".slc")

    'close the error log file
    logFile.close

    'clean up
    set fso = nothing

'End Sub

Sub SCADALogLaunch(pTimeOut, pFile)
'launch scadalog program with timeout
'takes the timeout in seconds and the scadalog .slc file as parameters
'returns nothing

    'launch with timeout the program to read data
    Call AppLaunch(pTimeOut, "SCADALog, " & pFile, SCADALog & " " & strProjectFolder & pFile & " /s=" & strProjectFolder & "ReadAll.aut /NoWindow")

End sub



Sub AppLaunch(pTimeOut, pLogName, pLaunchCmd)
'launch an application with timeout
'takes the timeout in secons, the log filename and the launch command as parameters
'returns nothing

    'declare variables
    Dim objWScript
    Dim objExec
    Dim intCount

    'Create the WScript shell object
    Set objWScript = CreateObject("WScript.Shell")

    'Runs <pLaunchCmd> command in a child command-shell
    Set objExec = objWScript.Exec(pLaunchCmd)
    logFile.write Now() & ", " & pLogName & ", Launched, "& vbcrlf

    'Set the timeout counter to zero
    intCount = 0

    'Loop for <pTimeOut> seconds or until objExec status = 0 (success) 
    Do While intCount/100 < pTimeOut

        'Exit the loop if the status is not zero
        If objExec.Status <> 0 Then
	    logFile.write Now() & ", " & pLogName & ", Success, " & cstr(Round(intCount/100, 2)) & " sec" & vbcrlf
            Exit Do
        End If

        intCount = intCount + 1
        WScript.Sleep 10
    Loop
    
    'Terminate the process if it is still running (status = 0)
    If objExec.Status = 0 Then
        objExec.Terminate
        logFile.write Now() & ", " & pLogName & ", Timed Out, " & cstr(Round(intCount/100, 2)) & " sec" & vbcrlf
    End If

    Set objWScript = Nothing

End sub
