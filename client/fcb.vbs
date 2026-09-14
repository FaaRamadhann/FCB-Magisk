' FCB launcher — double-click untuk jalan tanpa jendela cmd.
' Path otomatis mengikuti folder file ini, jadi tetap jalan
' walau folder FCB dipindah / hasil clone dari GitHub.
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("Wscript.Shell")
here = fso.GetParentFolderName(WScript.ScriptFullName)
sh.Run "pythonw """ & here & "\fcc.py""", 0, False
