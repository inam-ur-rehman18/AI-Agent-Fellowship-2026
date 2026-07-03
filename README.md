# AI Workspace

## About Me

Name: Inam Ur Rehman

University: The University of Faisalabad

Fellowship Track: NLP and AI Agents — Visibility Bots Internship

## Career Goals

I want to become an AI Engineer who builds practical, production-ready AI systems, particularly intelligent agents and NLP-driven tools that solve real business problems. My long-term goal is to work on AI products that combine language models with automation, helping companies build smarter, more visible, and more responsive digital systems. I'm especially interested in the intersection of conversational AI and agentic workflows, where AI doesn't just answer questions but actively completes tasks.

## Technical Skills


Languages: Python, JavaScript, HTML, CSS
Frameworks/Libraries: FastAPI
AI/ML: Prompt engineering, working with LLM APIs (Google Gemini), understanding of NLP fundamentals
Tools: Git, REST APIs, virtual environments, Uvicorn
Concepts: Client-server architecture, API security (keeping credentials server-side), error handling, environment configuration


## Learning Goals


Build a solid foundation in how AI agents plan, reason, and use tools to complete multi-step tasks.
Get comfortable designing and deploying full-stack AI applications, not just calling APIs in isolation.
Deepen my understanding of NLP concepts and how they apply to real-world bots and automation.
Learn best practices for making AI systems reliable, secure, and easy for others to use.
Move from building guided projects to independently designing and shipping my own AI tools by the end of the internship.



A chat interface for talking to an AI model, built from scratch with a Python (FastAPI) backend and a single-file HTML/CSS/JavaScript frontend. It uses Google Gemini's free tier (no credit card required) and keeps your API key safely on the server, never exposed to the browser.


# What This Project Does

### AI Workspace lets you:


Chat with Google's Gemini AI model through a clean, ChatGPT-style interface
Set a custom system prompt to control how the AI behaves
Use quick-start templates (Summarize Text, Explain Code, Generate Ideas, etc.)
Switch between light and dark mode
Export your conversation as a Markdown file
Get clear, human-readable error messages if something goes wrong (bad API key, rate limits, network issues, etc.)
A chat interface for talking to an AI model, with a system prompt editor,
prompt templates, Markdown rendering, and error handling — backed by a small
FastAPI server that keeps your API key off the client and uses **Google
Gemini's free tier** (no credit card required).

```
AI-Workspace/
├── app.py              # FastAPI app: /health, /models, /chat + serves frontend
├── requirements.txt
├── .env.example
├── run.sh              # One-command setup + start (Mac/Linux)
├── run.bat              # One-command setup + start (Windows)
├── frontend/
│   └── index.html      # Single-file UI (no build step)
└── README.md
```

## Quickest way to run it

**Windows:** double-click `run.bat`
**Mac/Linux:** open a terminal in this folder and run `./run.sh`

The script will create a virtual environment, install dependencies, and on
the first run it will open `.env` for you to paste in your API key — save
it, close the editor, and run the script again to start the server.

## Manual setup (if you'd rather do it by hand)

1. **Open the project folder in your editor/terminal.**

2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Get a free Gemini API key** (no credit card needed):
   [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

4. **Add the key:**
   ```bash
   cp .env.example .env          # Windows: copy .env.example .env
   ```
   Open `.env` and paste it in:
   ```
   GEMINI_API_KEY=AIza...
   ```

5. **Run the server:**
   ```bash
   python app.py
   ```

6. **Open the app:** go to **http://localhost:8000** in your browser.
   The backend serves the frontend directly, so this one URL is all you need —
   no separate frontend server, no CORS issues.

## How it works

- The browser never touches your API key. It calls `POST /chat` on your own
  backend, which attaches the key server-side and forwards the request to
  Gemini.
- Uses `gemini-3.5-flash` by default — currently on Google's free tier
  (free input/output tokens, no credit card, rate-limited rather than
  metered by cost). Confirm current free-tier models any time at
  [ai.google.dev/pricing](https://ai.google.dev/gemini-api/docs/pricing)
  before relying on this for anything beyond prototyping.
- Output is capped at 8192 tokens per reply (configurable — see below),
  well above the old 1024 cap, so long-form answers won't get cut off.
  There's no artificial limit on input length in this code; the practical
  ceiling is Gemini's own context window and your free-tier rate limits.
- `GET /models` lists the model picker options. Only **Gemini** is wired to
  a real model; the others (GPT-4o Mini, Claude, etc.) are shown for
  interface parity but are simulated — selecting them still routes through
  Gemini, same as the original spec allows for a single-provider build.
- `GET /health` reports whether a key is configured — useful for a quick
  sanity check: `curl http://localhost:8000/health`.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "Server is missing GEMINI_API_KEY" | You haven't created `.env`, or it's empty — see step 4. |
| "Invalid or unauthorized Gemini API key" | The key in `.env` is wrong, or the Generative Language API isn't enabled for it. |
| "Free-tier rate limit exceeded" | You've hit Gemini's per-minute or per-day free quota. Wait, or check usage in AI Studio. |
| "Gemini blocked this request" | The prompt tripped Gemini's safety filters — try rephrasing. |
| "Could not reach the AI provider" | No internet access from the machine running the backend. |
| Page loads but Send does nothing | Check the terminal running `python app.py` for errors, and your browser console (F12). |
| `run.bat` / `run.sh` says "python not found" | Install Python 3.10+ from [python.org](https://python.org) and make sure it's added to PATH. |

## Customizing the model or output length

Uncomment and edit these in `.env`:
```
GEMINI_MODEL=gemini-3.5-flash
GEMINI_MAX_OUTPUT_TOKENS=8192
```
