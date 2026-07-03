@echo off
cd /d "%~dp0"

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt --quiet

if not exist .env (
    echo Creating .env from .env.example - add your Gemini API key to it, then re-run.
    copy .env.example .env
    notepad .env
    exit /b
)

python app.py
pause
