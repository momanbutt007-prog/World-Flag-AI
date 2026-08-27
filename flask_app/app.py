from pathlib import Path
import sys

from flask import Flask, jsonify, render_template, request
from PIL import Image, UnidentifiedImageError


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# IMPORTS
# ============================================================

from core.predictor import WorldFlagPredictor
from core.country_info import load_country_info


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    template_folder=str(
        BASE_DIR / "flask_app" / "templates"
    ),
    static_folder=str(
        BASE_DIR / "flask_app" / "static"
    ),
)


# ============================================================
# LOAD MODEL ONCE
# ============================================================

print("\n" + "=" * 70)
print("STARTING WORLD FLAG AI FLASK APP")
print("=" * 70)

predictor = WorldFlagPredictor()

print("=" * 70)
print("FLASK APP READY")
print("=" * 70 + "\n")


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# HEALTH
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        **predictor.info()
    })


# ============================================================
# PREDICTION
# ============================================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
def predict():

    # --------------------------------------------------------
    # CHECK IMAGE
    # --------------------------------------------------------

    if "image" not in request.files:

        return jsonify({
            "success": False,
            "error": "No image uploaded."
        }), 400

    uploaded_file = request.files["image"]

    if not uploaded_file.filename:

        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400

    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    try:

        image = Image.open(
            uploaded_file.stream
        ).convert("RGB")

        result = predictor.predict(image)

        # ----------------------------------------------------
        # IMPORTANT FIX
        #
        # result["country"] is a DICT.
        #
        # Example:
        # {
        #     "country_name": "Italy",
        #     "official_name": "Italian Republic",
        #     ...
        # }
        #
        # load_country_info() expects a STRING.
        # ----------------------------------------------------

        country = result.get("country", {})

        if isinstance(country, dict):

            country_name = country.get(
                "country_name",
                ""
            )

        else:

            country_name = str(country)

        # ----------------------------------------------------
        # LOAD ADDITIONAL COUNTRY INFORMATION
        # ----------------------------------------------------

        try:

            country_info = load_country_info(
                country_name
            )

        except Exception as info_error:

            app.logger.warning(
                f"Country info loading failed: {info_error}"
            )

            country_info = {}

        # ----------------------------------------------------
        # ADD COUNTRY INFO
        # ----------------------------------------------------

        result["country_info"] = country_info

        # ----------------------------------------------------
        # SUCCESS RESPONSE
        # ----------------------------------------------------

        return jsonify({
            "success": True,
            **result
        })

    # --------------------------------------------------------
    # INVALID IMAGE
    # --------------------------------------------------------

    except UnidentifiedImageError:

        return jsonify({
            "success": False,
            "error": "Uploaded file is not a valid image."
        }), 400

    # --------------------------------------------------------
    # OTHER ERROR
    # --------------------------------------------------------

    except Exception as error:

        app.logger.exception(
            "Prediction error"
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )