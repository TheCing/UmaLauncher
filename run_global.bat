@echo off
set IS_UL_GLOBAL=1
cd /d "%~dp0umalauncher"
uv run python threader.py
pause
