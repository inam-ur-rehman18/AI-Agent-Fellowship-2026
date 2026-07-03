# AI Workspace

A chat interface for talking to an AI model, built from scratch with a Python (FastAPI) backend and a single-file HTML/CSS/JavaScript frontend. It uses **Google Gemini's free tier** (no credit card required) and keeps your API key safely on the server, never exposed to the browser.

---

## What This Project Does

AI Workspace lets you:
- Chat with Google's Gemini AI model through a clean, ChatGPT-style interface
- Set a custom system prompt to control how the AI behaves
- Use quick-start templates (Summarize Text, Explain Code, Generate Ideas, etc.)
- Switch between light and dark mode
- Export your conversation as a Markdown file
- Get clear, human-readable error messages if something goes wrong (bad API key, rate limits, network issues, etc.)

---

## Project Structure

```
AI-Workspace/
├── app.py              # FastAPI backend: /health, /models, /chat + serves the frontend
├── requirements.txt    # Python packages needed
├── .env.example         # Template for your API key and settings
├── run.sh                # One-command setup + start (Mac/Linux)
├── run.bat                # One-command setup + start (Windows)
├── frontend/
│   └── index.html        # The entire user interface (HTML + CSS + JS, no build step)
└── README.md               # This file
```

---

## Quickest Way to Run It

**Windows:** double-click `run.bat`
**Mac/Linux:** open a terminal in this folder and run `./run.sh`

The script will create a virtual environment, install dependencies, and on the first run it will open `.env` for you to paste in your API key. Save it, close the editor, and run the script again to start the server.

For full step-by-step instructions (including manual setup), see **INSTALLATION_GUIDE.md**.

---

## How It Works

1. You type a message in the browser and hit **Send**.
2. The frontend sends your message to your own backend server (not directly to Gemini).
3. The backend (`app.py`) attaches your private API key, forwards the request to Gemini, and gets back a reply.
4. The reply is sent back to the frontend and displayed as a chat bubble.

This backend-in-the-middle design exists for one main reason: **security**. If the API key lived in the browser code, anyone could open developer tools and steal it. Keeping it only on the server means it's never exposed.

### Backend Routes

| Route | Method | What it does |
|---|---|---|
| `/health` | GET | Checks if the server is running and whether an API key is configured |
| `/models` | GET | Returns the list of models shown in the UI dropdown |
| `/chat` | POST | Sends your conversation to Gemini and returns the AI's reply |

### Model

Uses `gemini-3.5-flash` by default, currently on Google's free tier (free input/output tokens, no credit card, rate-limited rather than metered by cost). Confirm current free-tier models any time at [ai.google.dev/pricing](https://ai.google.dev/gemini-api/docs/pricing).

Only **Gemini** is wired to a real model. Other options shown in the dropdown (GPT-4o Mini, Claude, etc.) are simulated for interface parity only.

---

## Requirements

- Python 3.10 or newer
- A free Gemini API key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Internet access (to reach Google's Gemini API)

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "Server is missing GEMINI_API_KEY" | You haven't created `.env`, or it's empty |
| "Invalid or unauthorized Gemini API key" | The key in `.env` is wrong, or the Generative Language API isn't enabled for it |
| "Free-tier rate limit exceeded" | You've hit Gemini's per-minute or per-day free quota |
| "Gemini blocked this request" | The prompt tripped Gemini's safety filters, try rephrasing |
| "Could not reach the AI provider" | No internet access from the machine running the backend |
| Page loads but Send does nothing | Check the terminal running `python app.py` for errors, and your browser console (F12) |
| `run.bat` / `run.sh` says "python not found" | Install Python 3.10+ from [python.org](https://python.org) and make sure it's added to PATH |

---

## Customizing the Model or Output Length

Uncomment and edit these in `.env`:
```
GEMINI_MODEL=gemini-3.5-flash
GEMINI_MAX_OUTPUT_TOKENS=8192
```

---

## License / Notes

This is a personal learning project built to understand how real AI applications are structured: a frontend, a backend that protects sensitive credentials, and a live connection to an external AI provider.
