Get-Process Python  | Where-Object { $_.ID -ne $pid } | Stop-Process
python "C:\Users\Bloomberg\Desktop\project\Quest_Manager\Quest_Manager.py"