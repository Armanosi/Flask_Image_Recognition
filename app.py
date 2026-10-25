
"""Flask application for hand-sign image recognition."""

from flask import Flask, render_template, request
from model import preprocess_img, predict_result

app = Flask(__name__)


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
