@echo off
cd /d "%~dp0"
"%~dp0venv\Scripts\python.exe" unpack_runs.py %*
pause
