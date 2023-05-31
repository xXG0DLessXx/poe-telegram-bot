@echo off

setlocal

REM Create a virtual environment in a subdirectory of the project
set "venv_dir=%CD%\env"
if not exist "%venv_dir%" (
    if "%PY_ENV%" == "env" (
        python -m venv "%venv_dir%"
    ) else (
        py -m venv "%venv_dir%"
    )
)

REM Activate the virtual environment
call "%venv_dir%\Scripts\activate.bat"

REM Install the required packages from the requirements.txt file
python -m pip install -r requirements.txt

REM Run PoeTelegramBot.py within the virtual environment
python PoeTelegramBot.py

REM Deactivate the virtual environment
call "%venv_dir%\Scripts\deactivate.bat"

endlocal
