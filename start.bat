@echo off
echo Starting Database Search Application Setup...

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Force reinstall all packages to ensure they're in the virtual environment
echo Installing/Updating required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

REM Apply migrations if needed
python manage.py migrate

echo Starting server on port 8181...
python manage.py runserver 8181

pause
