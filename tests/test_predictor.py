import sys
from pathlib import Path

from PIL import Image


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT
# ============================================================

from core.predictor import WorldFlagPredictor


# ============================================================
# TEST IMAGE
# ============================================================

if len(sys.argv) > 1:
    IMAGE_PATH = Path(sys.argv[1])
else:
    IMAGE_PATH = PROJECT_ROOT / "tests" / "test_flag.jpg"


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("WORLD FLAG AI — REAL IMAGE PREDICTION TEST")
print("=" * 70)


# ============================================================
# CHECK IMAGE
# ============================================================

if not IMAGE_PATH.exists():

    raise FileNotFoundError(
        f"\nTest image not found:\n"
        f"{IMAGE_PATH}\n\n"
        f"Usage:\n"
        f"python tests\\test_predictor.py "
        f"\"path\\to\\flag.jpg\""
    )


print("\nTest image:")
print(IMAGE_PATH)


# ============================================================
# LOAD PREDICTOR
# ============================================================

print("\nLoading World Flag AI predictor...")

predictor = WorldFlagPredictor()


# ============================================================
# LOAD IMAGE
# ============================================================

print("\nLoading image...")

image = Image.open(IMAGE_PATH).convert("RGB")

print("Original image size :", image.size)
print("Original image mode :", image.mode)


# ============================================================
# PREPROCESSING TEST
# ============================================================

prepared = predictor.prepare_image(image)

print("\nPrepared image shape :", prepared.shape)
print("Prepared image dtype :", prepared.dtype)
print(
    "Pixel range          : "
    f"{prepared.min():.2f} → {prepared.max():.2f}"
)


if prepared.shape != (1, 300, 300, 3):

    raise ValueError(
        f"Wrong prepared image shape: {prepared.shape}"
    )


print("✅ Image preprocessing passed")


# ============================================================
# PREDICTION
# ============================================================

print("\nRunning prediction...")

result = predictor.predict(image)


# ============================================================
# RESULT
# ============================================================

print("\n" + "=" * 70)
print("PREDICTION RESULT")
print("=" * 70)

print(f"Country    : {result['country']}")
print(
    f"Confidence : "
    f"{result['confidence_percent']:.2f}%"
)


# ============================================================
# TOP 5
# ============================================================

print("\nTop 5 predictions:")
print("-" * 70)

for position, item in enumerate(
    result["top_predictions"],
    start=1
):

    print(
        f"{position}. "
        f"{item['country_name']:<30} "
        f"{item['confidence_percent']:>7.2f}%"
    )


# ============================================================
# MODEL INFO
# ============================================================

print("\n" + "=" * 70)
print("MODEL INFORMATION")
print("=" * 70)

info = predictor.info()

print(f"Model       : {info['model']}")
print(f"Input       : {info['input_shape']}")
print(f"Output      : {info['output_shape']}")
print(f"Classes     : {info['classes']}")
print(f"Image size  : {info['image_size']}")


# ============================================================
# SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("✅ REAL IMAGE PREDICTION TEST PASSED")
print("=" * 70)