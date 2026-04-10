# jotform-downloader

Download JotForm submissions to an Excel (.xlsx) file from the command line.

---

## Requirements

- Python 3.10 or later
- A JotForm account with an API key ([get one here](https://www.jotform.com/myaccount/api))

---

## Setup

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

> You should see `(.venv)` appear at the start of your terminal prompt. Run the activate command again any time you open a new terminal window.

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Add your API key

Copy the example env file and open it in any text editor:

**Mac / Linux**
```
cp .env.example .env
```

**Windows**
```
copy .env.example .env
```

Edit `.env` and replace `your_api_key_here` with your actual JotForm API key:

```
JOTFORM_API_KEY=abc123yourrealkeyhere
```

---

## Usage

### List all your forms

```
python download.py --list
```

This prints a table of all your forms with their IDs and titles. You'll need a form ID to download submissions.

### Download submissions

```
python download.py <form_id>
```

For example:

```
python download.py 123456789
```

This creates a file called `submissions_123456789.xlsx` in the current directory.

### Specify a custom output filename

```
python download.py 123456789 --output my_responses.xlsx
```

---

## File overview

| File | Purpose |
|---|---|
| `download.py` | CLI entry point — parse arguments, call the module, write the file |
| `jotform.py` | Reusable module — API calls, pagination, data shaping |
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

**`python: command not found` (Windows)**
Download the installer from [python.org](https://www.python.org/downloads/windows/). During installation, check the box that says "Add Python to PATH".

**`ModuleNotFoundError: No module named 'requests'`**
Your virtual environment probably isn't active. Run the activate command from step 2 again, then re-run `pip install -r requirements.txt`.

**`Error: JOTFORM_API_KEY environment variable is not set`**
Make sure you created a `.env` file (not just `.env.example`) and that it contains your key with no extra spaces or quotes around the value.

**`RuntimeError: JotForm API error`**
Double-check your API key. Log in to JotForm, go to Account > API, and confirm the key is correct and hasn't been revoked.

**The `.xlsx` file opens but columns are empty**
Some forms use non-standard answer structures. Open an issue and share the form ID (do not share API keys or submission data publicly).
