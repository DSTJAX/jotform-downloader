"""
Flask web interface for downloading JotForm submissions.
Password-protected single-page app — just another wrapper around jotform.py.
"""

import io
import os
import secrets
from functools import wraps

import openpyxl
from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import jotform

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

APP_PASSWORD = os.environ.get("APP_PASSWORD", "")
JOTFORM_API_KEY = os.environ.get("JOTFORM_API_KEY", "")


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if APP_PASSWORD and secrets.compare_digest(password, APP_PASSWORD):
            session["authenticated"] = True
            return redirect(url_for("index"))
        error = "Incorrect password."
    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@require_auth
def index():
    forms = jotform.get_forms(JOTFORM_API_KEY)
    return render_template("index.html", forms=forms)


@app.route("/download", methods=["POST"])
@require_auth
def download():
    form_id = request.form.get("form_id", "")
    form_title = request.form.get("form_title", form_id)
    if not form_id:
        return "No form selected.", 400

    submissions = jotform.get_submissions(JOTFORM_API_KEY, form_id)
    headers, rows = jotform.submissions_to_rows(submissions)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Submissions"
    if headers:
        ws.append(headers)
    for row in rows:
        ws.append(row)

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in form_title)
    filename = f"{safe_title.strip()}_{form_id}.xlsx"

    return Response(
        buf,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
