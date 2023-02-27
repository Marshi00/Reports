Option Explicit

'declare the variables
Dim objArgs
Dim ProcID
Dim NewPrio
Dim wshShell
Dim svc
Dim strQuery
Dim colproc
Dim proc


'get the script arguments (process id and NewPrio in cryptic code)
Set objArgs = WScript.Arguments
ProcID=objArgs(0)
NewPrio=objArgs(1)

'get the security object to get a processes ID
Set wshShell=CreateObject("WScript.Shell")
Set svc = GetObject("WINMGMTS:\\.\ROOT\CIMV2") 

'get all tasks with the specified process id
strQuery="Select * from Win32_Process where processid=" & ProcID
Set colproc=svc.ExecQuery(strQuery)

'if any such processes exist, set the priority
If colproc.count <> 0 Then
    For Each proc In colproc
        proc.SetPriority(NewPrio)
    Next
End If
