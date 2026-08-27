from pathlib import Path
import json
import numpy as np
import tensorflow as tf
from PIL import Image


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model" / "World_Flag_AI_final.keras"
COUNTRIES_PATH = BASE_DIR / "country_data" / "countries.json"


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 70)
print("WORLD FLAG AI — MODEL + METADATA TEST")
print("=" * 70)

print("\nLoading model...")
model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

print("✅ Model loaded")

print("\nModel input :", model.input_shape)
print("Model output:", model.output_shape)


# ============================================================
# CHECK MODEL SHAPE
# ============================================================

assert model.input_shape == (None, 300, 300, 3), (
    f"Unexpected model input shape: {model.input_shape}"
)

assert model.output_shape == (None, 194), (
    f"Unexpected model output shape: {model.output_shape}"
)

print("✅ Input = 300 × 300 × 3")
print("✅ Output = 194 classes")


# ============================================================
# LOAD COUNTRY METADATA
# ============================================================

print("\nLoading country metadata...")

with open(COUNTRIES_PATH, "r", encoding="utf-8") as f:
    countries = json.load(f)

print("Metadata entries:", len(countries))

assert len(countries) == 194, (
    f"Expected 194 countries, found {len(countries)}"
)

print("✅ 194 country records found")


# ============================================================
# CHECK CLASS IDS
# ============================================================

class_ids = [
    int(country["class_id"])
    for country in countries
]

expected_ids = list(range(1, 195))

assert class_ids == expected_ids, (
    "Class IDs are not sequential 1 → 194"
)

print("✅ Class IDs = 1 → 194")


# ============================================================
# CHECK PALESTINE
# ============================================================

names = [
    country["country_name"].strip().lower()
    for country in countries
]

assert "palestine" in names, "Palestine is missing"

assert "israel" not in names, "Israel must not be present"

print("✅ Palestine included")
print("✅ Israel absent")


# ============================================================
# CREATE CLASS LOOKUP
# ============================================================

country_by_class = {
    int(country["class_id"]): country
    for country in countries
}

assert len(country_by_class) == 194

print("✅ Class lookup created")


# ============================================================
# TEST RANDOM MODEL INPUT
# ============================================================

print("\nRunning model forward pass...")

dummy_image = np.zeros(
    (1, 300, 300, 3),
    dtype=np.float32
)

prediction = model.predict(
    dummy_image,
    verbose=0
)

print("Prediction shape:", prediction.shape)

assert prediction.shape == (1, 194)

print("✅ Forward pass successful")


# ============================================================
# TEST PREDICTION → COUNTRY
# ============================================================

predicted_index = int(np.argmax(prediction[0]))

# Model output index is normally 0-based.
# Your metadata class_id is 1-based.
predicted_class_id = predicted_index + 1

country = country_by_class[predicted_class_id]

confidence = float(prediction[0][predicted_index])

print("\nTest prediction:")
print("-" * 70)
print("Output index :", predicted_index)
print("Class ID     :", predicted_class_id)
print("Country      :", country["country_name"])
print("Confidence   :", f"{confidence:.4f}")

print("\n" + "=" * 70)
print("✅ MODEL + METADATA TEST PASSED")
print("=" * 70)