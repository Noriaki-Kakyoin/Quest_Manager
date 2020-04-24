Get-Process Python  | Where-Object { $_.ID -ne $pid } | Stop-Process
python "C:\Users\Odin\Desktop\Quest_Manager\Quest_Manager.py"