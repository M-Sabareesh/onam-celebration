@echo off
echo 🚨 EMERGENCY DATABASE FIX
echo ========================

cd /d "%~dp0"

echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 🔧 Running database fix...
python direct_fix.py

echo.
echo ⌛ Fix complete. Press any key to continue...
pause
