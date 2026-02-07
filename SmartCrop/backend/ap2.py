from flask import Flask, render_template, request, redirect, url_for, session
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# ------------------ APP SETUP ------------------

app = Flask(__name__)
app.secret_key = "hackathon_secret_key"

# ------------------ LOAD MODEL ------------------

MODEL_PATH = "model/tomato_leaf_baseline.h5"

model = tf.keras.models.load_model(
    MODEL_PATH,
    custom_objects={"TrueDivide": tf.math.truediv}
)

CLASS_NAMES = [
    "Healthy",
    "Early Blight",
    "Late Blight",
    "Bacterial Spot"
]

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        # simple hackathon auth
        if username and password:
            session["user"] = username
            return redirect(url_for("upload"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/upload")
def upload():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("upload.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "user" not in session:
        return redirect(url_for("login"))

    file = request.files.get("image")

    if not file or file.filename == "":
        return redirect(url_for("upload"))

    # ---------- IMAGE PREPROCESS ----------
    image_bytes = file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))

    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # ---------- PREDICTION ----------
    preds = model.predict(img_array)
    confidence = float(np.max(preds)) * 100
    class_index = int(np.argmax(preds))

    disease = CLASS_NAMES[class_index]

    # ---------- STORE RESULT ----------
    session["disease"] = disease
    session["confidence"] = round(confidence, 2)

    return redirect(url_for("result"))


@app.route("/result")
def result():
    if "disease" not in session:
        return redirect(url_for("upload"))

    return render_template(
        "result.html",
        disease=session.get("disease"),
        confidence=session.get("confidence")
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
