"""Flask application for hand-sign digit recognition."""

import os

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from model import preprocess_img, predict_result

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY"
)

if not app.config["SECRET_KEY"]:
    if os.environ.get("FLASK_ENV") == "development":
        app.config["SECRET_KEY"] = "development-only-change-me"
    else:
        raise RuntimeError("FLASK_SECRET_KEY must be configured")

csrf = CSRFProtect(app)



@app.route("/")
def main():
    """Display the image upload page."""
    return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def predict_image_file():
    """Process an uploaded image and display its prediction."""
    try:
        uploaded_file = request.files.get("file")

        if uploaded_file is None or uploaded_file.filename == "":
            return render_template(
                "result.html",
                err="File cannot be processed."
            )

        image = preprocess_img(uploaded_file.stream)
        prediction = predict_result(image)

        return render_template(
            "result.html",
            predictions=str(prediction)
        )

    except (OSError, ValueError, KeyError):
        return render_template(
            "result.html",
            err="File cannot be processed."
        )


if __name__ == "__main__":
    app.run(port=9000, debug=True)
