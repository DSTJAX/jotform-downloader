# jotform-downloader

Download JotForm submissions to an Excel (.xlsx) file — from the command line or a password-protected web UI.

---

## Requirements

- Python 3.10 or later
- A JotForm account with an API key ([get one here](https://www.jotform.com/myaccount/api))

---

## Setup (local)

### 1. Clone the repo

```
git clone <your-repo-url>
cd jotform-downloader
```

### 2. Create a virtual environment

**Mac / Linux**
```
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt)**
```
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Add your environment variables

Copy the example env file:

**Mac / Linux**
```
cp .env.example .env
```

**Windows**
```
copy .env.example .env
```

Edit `.env` with your values:

```
JOTFORM_API_KEY=abc123yourrealkeyhere
APP_PASSWORD=choose_a_strong_password
SECRET_KEY=a_long_random_string
```

Generate a good `SECRET_KEY` with:
```
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Usage — CLI

### List all your forms

```
python download.py --list
```

### Download submissions

```
python download.py <form_id>
```

For example:

```
python download.py 123456789
```

This creates `submissions_123456789.xlsx` in the current directory.

### Specify a custom output filename

```
python download.py 123456789 --output my_responses.xlsx
```

---

## Usage — Web UI

Start the web server locally:

```
python app.py
```

Then open `http://localhost:5000` in your browser. You'll be prompted for the password you set in `APP_PASSWORD`. After logging in, pick a form from the dropdown and click **Download .xlsx**.

---

## Deploying to Render

Render is the easiest way to host the web UI so you can use it from your phone or iPad without running anything locally.

### 1. Push your repo to GitHub

Make sure `.env` is in `.gitignore` (it is by default) — never push your secrets.

### 2. Create a new Web Service on Render

1. Go to [render.com](https://render.com) and sign in.
2. Click **New → Web Service**.
3. Connect your GitHub repo.
4. Set the following in the Render dashboard:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### 3. Set environment variables

In your Render service, go to **Environment** and add:

| Key | Value |
|---|---|
| `JOTFORM_API_KEY` | Your JotForm API key |
| `APP_PASSWORD` | A strong password of your choice |
| `SECRET_KEY` | A long random string (run `python -c "import secrets; print(secrets.token_hex(32))"` locally to generate one) |

### 4. Deploy

Click **Deploy**. Render will build and start your app. Once it's live, open the service URL in any browser — phone, iPad, or desktop.

> **Free tier note:** Render's free tier spins down after 15 minutes of inactivity. The first request after a sleep may take 30–60 seconds to respond. Upgrade to a paid instance ($7/mo) for always-on availability.

---

## File overview

| File | Purpose |
|---|---|
| `app.py` | Flask web UI — password login, form picker, xlsx download |
| `download.py` | CLI entry point — parse arguments, call the module, write the file |
| `jotform.py` | Reusable module — API calls, pagination, data shaping |
| `templates/` | HTML templates for the web UI |
| `Procfile` | Tells Render/Railway how to start the web server |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for environment variables |
| `.gitignore` | Keeps secrets and generated files out of git |

---

## Troubleshooting

**`python3: command not found` (Mac)**
Install Python from [python.org](https://www.python.org/downloads/) or via Homebrew:
```
brew install python
```

**`ModuleNotFoundError: No module named 'requests'`**
Your virtual environment probably isn't active. Run the activate command and then `pip install -r requirements.txt` again.

**`Error: JOTFORM_API_KEY environment variable is not set`**
Make sure you created a `.env` file (not just `.env.example`) and that it contains your key with no extra spaces or quotes.

**`RuntimeError: JotForm API error`**
Double-check your API key. Log in to JotForm, go to Account > API, and confirm the key is correct and hasn't been revoked.

**The `.xlsx` file opens but columns are empty**
Some forms use non-standard answer structures. Open an issue and share the form ID (do not share API keys or submission data publicly).

**The web UI is slow on first load (Render free tier)**
This is expected — Render free services spin down after inactivity. Upgrade to a paid instance for always-on speed.
