from pathlib import Path
import json

import numpy as np
import tensorflow as tf
from PIL import Image


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "model" / "World_Flag_AI_final.keras"
COUNTRIES_PATH = BASE_DIR / "country_data" / "countries.json"


# ============================================================
# MODEL CONFIGURATION
# ============================================================

IMAGE_SIZE = (300, 300)
NUM_CLASSES = 194
TOP_K = 5


# ============================================================
# WORLD FLAG AI PREDICTOR
# ============================================================

class WorldFlagPredictor:

    def __init__(self):

        print("=" * 70)
        print("WORLD FLAG AI")
        print("=" * 70)

        # ----------------------------------------------------
        # CHECK MODEL
        # ----------------------------------------------------

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"\nModel not found:\n{MODEL_PATH}\n"
            )

        # ----------------------------------------------------
        # CHECK COUNTRY DATA
        # ----------------------------------------------------

        if not COUNTRIES_PATH.exists():
            raise FileNotFoundError(
                f"\nCountry metadata not found:\n{COUNTRIES_PATH}\n"
            )

        # ----------------------------------------------------
        # LOAD COUNTRY METADATA
        # ----------------------------------------------------

        print("\nLoading country metadata...")
        print(COUNTRIES_PATH)

        with open(
            COUNTRIES_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            countries = json.load(file)

        if not isinstance(countries, list):
            raise ValueError(
                "countries.json must contain a JSON list."
            )

        if len(countries) != NUM_CLASSES:
            raise ValueError(
                "\nWrong number of country records.\n"
                f"Expected: {NUM_CLASSES}\n"
                f"Found   : {len(countries)}"
            )

        # ----------------------------------------------------
        # CREATE CLASS LOOKUP
        #
        # class_id 1 -> index 0
        # class_id 2 -> index 1
        # ...
        # class_id 194 -> index 193
        # ----------------------------------------------------

        self.countries = {}

        for country in countries:

            if not isinstance(country, dict):
                raise ValueError(
                    "Every country entry must be a JSON object."
                )

            if "class_id" not in country:
                raise ValueError(
                    "Country entry is missing class_id."
                )

            class_id = int(country["class_id"])

            if class_id in self.countries:
                raise ValueError(
                    f"Duplicate class_id found: {class_id}"
                )

            self.countries[class_id] = country

        # ----------------------------------------------------
        # VERIFY CLASS IDS
        # ----------------------------------------------------

        expected_ids = set(range(1, NUM_CLASSES + 1))
        actual_ids = set(self.countries.keys())

        if actual_ids != expected_ids:

            missing = sorted(
                expected_ids - actual_ids
            )

            extra = sorted(
                actual_ids - expected_ids
            )

            raise ValueError(
                "\nInvalid class IDs.\n"
                f"Missing: {missing}\n"
                f"Extra  : {extra}"
            )

        # ----------------------------------------------------
        # VERIFY PALESTINE
        # ----------------------------------------------------

        palestine = [
            country
            for country in self.countries.values()
            if country.get("country_name") == "Palestine"
        ]

        if not palestine:
            raise ValueError(
                "Palestine is missing from countries.json."
            )

        # ----------------------------------------------------
        # VERIFY ISRAEL ABSENT
        # ----------------------------------------------------

        israel = [
            country
            for country in self.countries.values()
            if country.get("country_name") == "Israel"
        ]

        if israel:
            raise ValueError(
                "Israel must not be present in countries.json."
            )

        print("✅ 194 country records loaded")
        print("✅ Class IDs = 1 → 194")
        print("✅ Palestine included")
        print("✅ Israel absent")

        # ----------------------------------------------------
        # LOAD MODEL
        # ----------------------------------------------------

        print("\nLoading model...")
        print(MODEL_PATH)

        self.model = tf.keras.models.load_model(
            MODEL_PATH,
            compile=False
        )

        print("✅ Model loaded")

        # ----------------------------------------------------
        # VERIFY MODEL INPUT
        # ----------------------------------------------------

        print("\nModel input :", self.model.input_shape)
        print("Model output:", self.model.output_shape)

        expected_input = (
            None,
            300,
            300,
            3
        )

        if tuple(self.model.input_shape) != expected_input:

            raise ValueError(
                "\nWrong model input shape.\n"
                f"Expected: {expected_input}\n"
                f"Found   : {self.model.input_shape}"
            )

        # ----------------------------------------------------
        # VERIFY MODEL OUTPUT
        # ----------------------------------------------------

        output_classes = self.model.output_shape[-1]

        if output_classes != NUM_CLASSES:

            raise ValueError(
                "\nWrong number of model classes.\n"
                f"Expected: {NUM_CLASSES}\n"
                f"Found   : {output_classes}"
            )

        print("\n✅ Input  = 300 × 300 × 3")
        print("✅ Output = 194 classes")
        print("✅ Metadata = 194 countries")

        print("=" * 70)

    # ========================================================
    # IMAGE PREPROCESSING
    # ========================================================

    def prepare_image(self, image):

        # ----------------------------------------------------
        # PIL IMAGE
        # ----------------------------------------------------

        if not isinstance(image, Image.Image):

            raise TypeError(
                "image must be a PIL.Image.Image object."
            )

        # ----------------------------------------------------
        # FORCE RGB
        # ----------------------------------------------------

        image = image.convert("RGB")

        # ----------------------------------------------------
        # RESIZE
        # ----------------------------------------------------

        image = image.resize(
            IMAGE_SIZE,
            Image.Resampling.BILINEAR
        )

        # ----------------------------------------------------
        # NUMPY
        # ----------------------------------------------------

        image_array = np.asarray(
            image,
            dtype=np.float32
        )

        # ----------------------------------------------------
        # VERIFY IMAGE
        # ----------------------------------------------------

        if image_array.shape != (
            300,
            300,
            3
        ):

            raise ValueError(
                f"Invalid image shape: "
                f"{image_array.shape}"
            )

        # ----------------------------------------------------
        # BATCH DIMENSION
        # ----------------------------------------------------

        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        return image_array

    # ========================================================
    # GET COUNTRY BY CLASS ID
    # ========================================================

    def get_country(self, class_id):

        class_id = int(class_id)

        country = self.countries.get(class_id)

        if country is None:
            raise ValueError(
                f"Unknown class ID: {class_id}"
            )

        return country

    # ========================================================
    # PREDICTION
    # ========================================================

    def predict(self, image):

        # ----------------------------------------------------
        # PREPARE IMAGE
        # ----------------------------------------------------

        image_array = self.prepare_image(image)

        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        predictions = self.model.predict(
            image_array,
            verbose=0
        )[0]

        # ----------------------------------------------------
        # VERIFY OUTPUT
        # ----------------------------------------------------

        if predictions.shape != (
            NUM_CLASSES,
        ):

            raise ValueError(
                "\nUnexpected model prediction shape.\n"
                f"Expected: ({NUM_CLASSES},)\n"
                f"Found   : {predictions.shape}"
            )

        # ----------------------------------------------------
        # TOP PREDICTION
        # ----------------------------------------------------

        best_index = int(
            np.argmax(predictions)
        )

        # Model index is zero-based.
        # Country class_id is one-based.

        best_class_id = best_index + 1

        best_confidence = float(
            predictions[best_index]
        )

        best_country = self.get_country(
            best_class_id
        )

        # ----------------------------------------------------
        # TOP K
        # ----------------------------------------------------

        top_indices = np.argsort(
            predictions
        )[::-1][:TOP_K]

        top_predictions = []

        for index in top_indices:

            index = int(index)

            class_id = index + 1

            confidence = float(
                predictions[index]
            )

            country = self.get_country(
                class_id
            )

            top_predictions.append({

                "class_id": class_id,

                "country_name": country.get(
                    "country_name",
                    ""
                ),

                "confidence": confidence,

                "confidence_percent": round(
                    confidence * 100,
                    2
                )

            })

        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        return {

            "class_id": best_class_id,

            "country": best_country,

            "confidence": best_confidence,

            "confidence_percent": round(
                best_confidence * 100,
                2
            ),

            "top_predictions": top_predictions
        }

    # ========================================================
    # MODEL INFORMATION
    # ========================================================

    def info(self):

        return {

            "model": MODEL_PATH.name,

            "model_path": str(
                MODEL_PATH
            ),

            "input_shape": list(
                self.model.input_shape
            ),

            "output_shape": list(
                self.model.output_shape
            ),

            "classes": NUM_CLASSES,

            "image_size": [
                IMAGE_SIZE[0],
                IMAGE_SIZE[1]
            ],

            "metadata_file": COUNTRIES_PATH.name
        }


# ============================================================
# SINGLE PREDICTOR INSTANCE
# ============================================================

_predictor = None


def get_predictor():

    global _predictor

    if _predictor is None:
        _predictor = WorldFlagPredictor()

    return _predictor


# ============================================================
# SIMPLE FUNCTION FOR FLASK / STREAMLIT
# ============================================================

def predict_flag(image):

    predictor = get_predictor()

    return predictor.predict(image)