Option Explicit

'declare the variables
Dim objArgs
Dim ProcID
Dim Timeout
Dim wshShell
Dim svc
Dim strQuery
Dim colproc
Dim proc


'get the script arguments (process id and timeout in seconds)
Set objArgs = WScript.Arguments
ProcID=objArgs(0)
TimeOut=objArgs(1)

'sleep for the timeout period
wscript.sleep TimeOut*1000

'get the security object to get a processes ID
Set wshShell=CreateObject("WScript.Shell")
Set svc = GetObject("WINMGMTS:{impersonationLevel=impersonate,(Security)}!\\.\ROOT\CIMV2") 

'get all tasks with the specified process id
strQuery="Select * from Win32_Process where processid=" & ProcID
Set colproc=svc.ExecQuery(strQuery)

'if any such processes exist, terminate them
If colproc.count <> 0 Then
    For Each proc In colproc
        proc.terminate()
    Next
End If
