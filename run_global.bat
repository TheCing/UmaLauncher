@echo off
set IS_UL_GLOBAL=1
cd /d "%~dp0umalauncher"
"%~dp0venv\Scripts\python.exe" threader.py
pause
