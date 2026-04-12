cd ./umalauncher
uv run python create_version.py
uv run pyinstaller threader_jp_steam.spec || exit /b 1
cd ..