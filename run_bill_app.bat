@echo off
REM ====================================
REM Flask Bill App - Auto Startup Script
REM ====================================

REM Set working directory
cd /d "C:\Pranav\Personal_projects\Functionhall_bill_app_web"

REM Set log file path
set LOGFILE=C:\Pranav\Personal_projects\Functionhall_bill_app_web\Startuplog\startup_log.txt

REM Clear old log if it's too large (keep last 100KB)
for %%A in ("%LOGFILE%") do (
    if %%~zA gtr 102400 (
        echo Log cleared on %date% %time% > "%LOGFILE%"
    )
)

echo ================================== >> "%LOGFILE%" 2>&1
echo Flask App Startup Attempt >> "%LOGFILE%" 2>&1
echo Date/Time: %date% %time% >> "%LOGFILE%" 2>&1
echo Working Directory: %CD% >> "%LOGFILE%" 2>&1
echo ================================== >> "%LOGFILE%" 2>&1

REM Wait for system to be ready
echo Waiting 5 seconds for system... >> "%LOGFILE%" 2>&1
timeout /t 5 /nobreak >nul 2>&1

REM Check if Python is available
echo Checking Python installation... >> "%LOGFILE%" 2>&1
python --version >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH! >> "%LOGFILE%" 2>&1
    echo Please install Python or add it to PATH >> "%LOGFILE%" 2>&1
    exit /b 1
)
echo Python found successfully >> "%LOGFILE%" 2>&1

REM Check if app.py exists
if not exist "app.py" (
    echo ERROR: app.py not found in %CD% >> "%LOGFILE%" 2>&1
    exit /b 1
)
echo app.py found >> "%LOGFILE%" 2>&1

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment... >> "%LOGFILE%" 2>&1
    call venv\Scripts\activate >> "%LOGFILE%" 2>&1
    echo Virtual environment activated >> "%LOGFILE%" 2>&1
) else (
    echo No virtual environment found, using system Python >> "%LOGFILE%" 2>&1
)

REM Kill any existing Python instances running app.py (avoid port conflicts)
echo Checking for existing Flask instances... >> "%LOGFILE%" 2>&1
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if %ERRORLEVEL% EQU 0 (
    echo Found existing Python process, checking if it's our app... >> "%LOGFILE%" 2>&1
    REM Optional: Kill it to avoid port conflict
    REM taskkill /F /IM python.exe /FI "WINDOWTITLE eq Flask Bill App*" >> "%LOGFILE%" 2>&1
)

REM Start Flask app in minimized window
echo Starting Flask application... >> "%LOGFILE%" 2>&1
start "Flask Bill App" /MIN python app.py >> "%LOGFILE%" 2>&1

REM Wait a moment and verify it started
timeout /t 3 /nobreak >nul 2>&1

REM Check if Python process is running
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Flask app started successfully! >> "%LOGFILE%" 2>&1
    echo Access the app at: http://127.0.0.1:5000 >> "%LOGFILE%" 2>&1
) else (
    echo ERROR: Flask app failed to start >> "%LOGFILE%" 2>&1
)

echo ================================== >> "%LOGFILE%" 2>&1
echo. >> "%LOGFILE%" 2>&1

exit /b 0