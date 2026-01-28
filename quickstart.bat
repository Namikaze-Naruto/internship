@echo off
REM Quick Start Script for Unstop Scraper

echo ========================================
echo   Unstop Internships Portal - Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo [1/6] Checking Python... OK
echo.

REM Create virtual environment if not exists
if not exist "venv\" (
    echo [2/6] Creating virtual environment...
    python -m venv venv
    echo       Created!
) else (
    echo [2/6] Virtual environment exists... OK
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo       Activated!
echo.

REM Install dependencies
echo [4/6] Installing dependencies...
pip install -q -r requirements.txt
echo       Installed!
echo.

REM Check .env file
if not exist ".env" (
    echo [5/6] Creating .env file from template...
    copy .env.example .env >nul
    echo       Created! Please edit .env and add API_BASE_URL
    echo.
    echo [WARNING] API_BASE_URL is required for scraping!
    echo           Edit .env file and add the Unstop API endpoint.
) else (
    echo [5/6] .env file exists... OK
)
echo.

REM Run tests
echo [6/6] Running tests...
python test_scraper.py
if errorlevel 1 (
    echo.
    echo [ERROR] Tests failed. Please check the error above.
    pause
    exit /b 1
)
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo What would you like to do?
echo.
echo   1. Run the scraper
echo   2. Start local web server (http://localhost:8000)
echo   3. Open documentation
echo   4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Running scraper...
    python -m src.scraper
    pause
) else if "%choice%"=="2" (
    echo.
    echo Starting web server at http://localhost:8000
    echo Press Ctrl+C to stop
    echo.
    cd docs
    python -m http.server 8000
) else if "%choice%"=="3" (
    echo.
    start README.md
    start DEPLOYMENT.md
) else (
    echo.
    echo Goodbye!
)
