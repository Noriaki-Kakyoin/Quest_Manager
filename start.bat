@echo off

call getCmdPID
set "current_pid=%errorlevel%"

taskkill /f /im "start.bat"

python "C:\Users\Odin\Desktop\Quest_Manager\Quest_Manager.py"

PAUSE