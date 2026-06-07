@echo off
REM Fortnite Matchmaking Bot - Build Setup Script
REM This script will install dependencies and build the executable

echo.
echo ========================================
echo Fortnite Matchmaking Bot Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

echo [2/4] Installing required packages...
pip install customtkinter fortnitepy pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)
echo.

echo [3/4] Building executable...
pyinstaller --onefile --windowed --name=FortniteMatchmakingBot fortnite_matchmaking_bot.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)
echo.

echo [4/4] Build complete!
echo.
echo ========================================
echo SUCCESS! Your executable is ready!
echo ========================================
echo.
echo Location: dist\FortniteMatchmakingBot.exe
echo.
echo You can now:
echo - Move FortniteMatchmakingBot.exe anywhere
echo - Share it with friends
echo - Run it without Python installed
echo.
pause
