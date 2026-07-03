# Installation Guide — AI Workspace

This guide walks you through setting up and running AI Workspace on your computer, step by step.

---

## Before You Start

You'll need:
1. **Python 3.10 or newer** installed on your computer
2. **Internet access** (to install packages and reach Google's Gemini API)
3. A **free Google Gemini API key** (instructions below, no credit card required)

To check if Python is already installed, open a terminal (Mac/Linux) or Command Prompt (Windows) and run:
```
python3 --version
```
On Windows, try:
```
python --version
```
If you see a version number (3.10 or higher), you're good. If not, download Python from [python.org](https://python.org) and install it. **On Windows, make sure to check "Add Python to PATH" during installation.**

---

## Option A: Automatic Setup (Recommended)

This is the easiest way, using the included setup scripts.

### On Windows
1. Open the `AI-Workspace` folder.
2. Double-click **`run.bat`**.
3. A terminal window will open and:
   - Create a virtual environment (a self-contained space for Python packages)
   - Install all required packages
   - Open Notepad with a `.env` file for you to add your API key
4. Paste your Gemini API key into the `.env` file where it says `GEMINI_API_KEY=your_key_here`, replacing `your_key_here` with your actual key.
5. Save the file and close Notepad.
6. Double-click **`run.bat`** again. This time it will start the server.
7. Open your browser and go to **http://localhost:8000**.

### On Mac/Linux
1. Open a terminal in the `AI-Workspace` folder.
2. Run:
   ```
   ./run.sh
   ```
   If you get a "permission denied" error, first run:
   ```
   chmod +x run.sh
   ```
   then try again.
3. The script will create a virtual environment, install packages, and open a `.env` file in a text editor (nano) for you to add your API key.
4. Paste your Gemini API key into the `.env` file where it says `GEMINI_API_KEY=your_key_here`.
5. Save and exit the editor:
   - In nano: press `Ctrl + O`, then `Enter` to save, then `Ctrl + X` to exit.
6. Run `./run.sh` again. This time it will start the server.
7. Open your browser and go to **http://localhost:8000**.

---

## Option B: Manual Setup

If you'd rather do it step by step yourself:

### Step 1: Open the project folder
Open a terminal or command prompt inside the `AI-Workspace` folder.

### Step 2: Create a virtual environment
```bash
python3 -m venv venv
```
On Windows, use `python` instead of `python3` if needed.

### Step 3: Activate the virtual environment
**Mac/Linux:**
```bash
source venv/bin/activate
```
**Windows:**
```bash
venv\Scripts\activate
```
You'll know it worked if you see `(venv)` at the start of your terminal line.

### Step 4: Install the required packages
```bash
pip install -r requirements.txt
```
This installs FastAPI, Uvicorn, Requests, python-dotenv, and Pydantic.

### Step 5: Get a free Gemini API key
1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with a Google account.
3. Click to create a new API key.
4. Copy the key (it will look something like `AIza...`).

### Step 6: Add your key to the project
Copy the example environment file:
```bash
cp .env.example .env
```
On Windows:
```bash
copy .env.example .env
```
Open `.env` in any text editor and paste your key:
```
GEMINI_API_KEY=AIza...your_actual_key_here
```
Save the file.

### Step 7: Start the server
```bash
python app.py
```
You should see a message like:
```
Starting AI Workspace on http://localhost:8000
```

### Step 8: Open the app
Go to **http://localhost:8000** in your web browser. The chat interface should load, and the backend serves both the API and the interface from that same address.

---

## Verifying It's Working

To quickly check the server is running and your key is configured, open a new terminal (leave the server running) and run:
```bash
curl http://localhost:8000/health
```
You should see something like:
```json
{"status": "ok", "key_configured": true, "model": "gemini-3.5-flash"}
```
If `key_configured` says `false`, double check that your `.env` file has the correct key saved.

---

## Common Problems and Fixes

| Problem | Fix |
|---|---|
| "python not found" | Install Python from python.org and make sure it's added to PATH |
| "pip not found" | Make sure your virtual environment is activated (Step 3) |
| "Server is missing GEMINI_API_KEY" | Check that `.env` exists and has your real key, not `your_key_here` |
| "Invalid or unauthorized Gemini API key" | Double check you copied the full key correctly, and that it's enabled in Google AI Studio |
| Page loads but nothing happens when you click Send | Check the terminal running `python app.py` for error messages, and press F12 in your browser to check the console |
| "Free-tier rate limit exceeded" | Wait a minute and try again, or check your usage at Google AI Studio |
| Permission denied running `run.sh` | Run `chmod +x run.sh` first, then try `./run.sh` again |

---

## Stopping the Server

Go back to the terminal window running the server and press `Ctrl + C`.

## Running It Again Later

You don't need to repeat the full setup each time. Just:
- **Windows:** double-click `run.bat`
- **Mac/Linux:** run `./run.sh`

Since the virtual environment and `.env` file already exist, it will skip straight to starting the server.
