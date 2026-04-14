@echo off
set IS_JP_STEAM=1
cd /d "%~dp0umalauncher"
uv run python threader.py
pause
