@echo off
REM ==========================================
REM SEAL VERIFICATION API - STARTUP SCRIPT
REM ==========================================

echo.
echo ==========================================
echo SEAL VERIFICATION API - STARTUP
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create output directory if it doesn't exist
if not exist "output" mkdir output
if not exist "input" mkdir input

REM Start API
echo.
echo ==========================================
echo Starting API on http://localhost:8000
echo ==========================================
echo.
echo Swagger UI: http://localhost:8000/docs
echo ReDoc UI: http://localhost:8000/redoc
echo.

python api.py

pause
