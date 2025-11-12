@echo off
REM ----------------------------
REM Install script for web-pirate
REM ----------------------------

REM 1. Create virtual environment
python -m venv venv

REM 2. Activate virtual environment
call venv\Scripts\activate

REM 3. Upgrade pip
python -m pip install --upgrade pip

REM 4. Install dependencies
pip install -r requirements.txt

REM 5. Install Playwright browsers
python -m playwright install

echo.
echo Installation complete!
pause
