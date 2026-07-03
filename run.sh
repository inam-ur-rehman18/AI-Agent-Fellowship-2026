#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt --quiet

if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example - add your Gemini API key to it, then re-run this script."
    cp .env.example .env
    ${EDITOR:-nano} .env
    exit 0
fi

python app.py
