from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "hackathon_secret_key"

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000/predict"

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        # HARD-CODED HACKATHON LOGIN
        if username == "Vansh" and password == "Sadadvel":
            session["user"] = "Vansh"
            return redirect(url_for("upload"))
        else:
            return render_template(
                "login.html",
                error="Invalid credentials. Try again."
            )

    return render_template("login.html")


@app.route("/guest")
def guest_login():
    session["user"] = "Guest"
    return redirect(url_for("upload"))


@app.route("/upload")
def upload():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("upload.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    # 1. Check login
    if "user" not in session:
        return redirect(url_for("login"))

    # 2. Get uploaded file
    file = request.files.get("image")

    if not file or file.filename == "":
        return redirect(url_for("upload"))

    # 3. Send image to FastAPI
    response = requests.post(
        FASTAPI_URL,
        files={
            "file": (file.filename, file.stream, file.mimetype)
        }
    )

    if response.status_code != 200:
        return "Prediction service failed", 500

    result = response.json()

    # 4. Store result in session
    session["status"] = result.get("status")
    session["confidence"] = result.get("confidence")

    # 5. Redirect to result page
    return redirect(url_for("result"))


@app.route("/result")
def result():
    if "status" not in session:
        return redirect(url_for("upload"))

    return render_template(
        "result.html",
        status=session.get("status"),
        confidence=session.get("confidence")
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
