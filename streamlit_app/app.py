from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

import sys

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from core.predictor import get_predictor


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="World Flag AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS — "World Atlas" navy / gold / sky-blue theme
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Poppins', sans-serif !important; }

    /* ---------- App background: night atlas ---------- */
    .stApp {
        background:
            radial-gradient(circle at 10% -8%, rgba(212, 175, 55, 0.10) 0%, transparent 40%),
            radial-gradient(circle at 92% 6%, rgba(56, 189, 248, 0.14) 0%, transparent 48%),
            radial-gradient(circle at 50% 108%, rgba(212, 175, 55, 0.06) 0%, transparent 55%),
            linear-gradient(160deg, #060a16 0%, #0a1226 45%, #06091a 100%);
        color: #eef2fb;
    }

    /* ---------- Hero header ---------- */
    .hero-wrap {
        padding: 1.9rem 2.4rem;
        border-radius: 22px;
        margin-bottom: 1.4rem;
        background: linear-gradient(120deg, #0b2545 0%, #144272 55%, #205295 100%);
        border: 1px solid rgba(212,175,55,0.20);
        box-shadow: 0 20px 45px rgba(6,20,50,0.45);
        position: relative;
        overflow: hidden;
    }

    .hero-wrap::after {
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 220px;
        height: 220px;
        background: rgba(212,175,55,0.10);
        border-radius: 50%;
    }

    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.5px;
    }

    .subtitle {
        font-size: 0.95rem;
        color: rgba(238,242,251,0.82);
        max-width: 700px;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 30% 0%, rgba(212,175,55,0.07), transparent 45%),
            radial-gradient(circle at 90% 40%, rgba(56,189,248,0.10), transparent 50%),
            linear-gradient(180deg, #081020 0%, #04070f 100%);
        border-right: 1px solid rgba(238,242,251,0.07);
    }

    section[data-testid="stSidebar"] * { color: #eef2fb !important; }

    .sb-logo-wrap { text-align: center; padding: 0.6rem 0 0.4rem 0; }

    .sb-logo-badge {
        width: 58px;
        height: 58px;
        margin: 0 auto 0.5rem auto;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.7rem;
        background: linear-gradient(135deg, #144272, #205295 55%, #d4af37);
        box-shadow: 0 10px 26px rgba(32,82,149,0.40);
    }

    .sb-title {
        font-size: 1.15rem;
        font-weight: 800;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 0.1rem;
    }

    .sb-subtitle {
        font-size: 0.68rem;
        color: rgba(238,242,251,0.5) !important;
        letter-spacing: 1.4px;
        text-transform: uppercase;
    }

    .sb-section-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 0.5rem 0 0.5rem 0;
        color: #ffffff !important;
    }

    .sb-section-label .icon-chip-sm {
        width: 24px;
        height: 24px;
        min-width: 24px;
        border-radius: 7px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        background: linear-gradient(135deg, rgba(212,175,55,0.28), rgba(56,189,248,0.28));
        border: 1px solid rgba(238,242,251,0.12);
    }

    .sb-status-chip {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        background: rgba(56,189,248,0.10);
        border: 1px solid rgba(56,189,248,0.35);
        border-radius: 12px;
        padding: 0.6rem 0.85rem;
        margin-bottom: 0.6rem;
        font-size: 0.86rem;
        font-weight: 600;
        color: #93d9f8 !important;
    }

    .sb-card {
        background: rgba(238,242,251,0.045);
        border: 1px solid rgba(238,242,251,0.10);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }

    .sb-card p { margin: 0.25rem 0; font-size: 0.85rem; color: rgba(238,242,251,0.85) !important; }
    .sb-card b { color: #d4af37 !important; }

    /* ---------- Section headers in main body ---------- */
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        color: #ffffff;
        margin: 1.6rem 0 0.8rem 0;
    }

    /* ---------- Upload card ---------- */
    div[data-testid="stFileUploaderDropzone"] {
        background:
            radial-gradient(circle at 20% 15%, rgba(56,189,248,0.09), transparent 55%),
            radial-gradient(circle at 80% 85%, rgba(212,175,55,0.08), transparent 55%),
            rgba(238,242,251,0.03);
        border: 2px dashed rgba(56,189,248,0.45);
        border-radius: 16px;
    }

    div[data-testid="stFileUploaderDropzone"]:hover {
        border-color: rgba(212,175,55,0.6);
    }

    div[data-testid="stFileUploaderDropzone"] button {
        background: linear-gradient(120deg, #144272, #205295) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* ---------- Prediction result block ---------- */
    .result-card {
        background: linear-gradient(155deg, rgba(16,185,129,0.14), rgba(212,175,55,0.08));
        border: 1px solid rgba(16,185,129,0.30);
        border-radius: 20px;
        padding: 1.5rem 1.7rem;
        box-shadow: 0 14px 34px rgba(0,0,0,0.35);
        height: 100%;
    }

    .country-name {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }

    .official-name {
        font-size: 16px;
        margin-top: 6px;
        color: rgba(238,242,251,0.72);
    }

    .confidence {
        display: inline-block;
        font-size: 14px;
        margin-top: 14px;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        background: rgba(16,185,129,0.16);
        border: 1px solid rgba(16,185,129,0.4);
        color: #6ee7b7;
        font-weight: 700;
    }

    /* ---------- Info boxes ---------- */
    .info-box {
        background: rgba(238,242,251,0.045);
        border: 1px solid rgba(238,242,251,0.10);
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 8px 22px rgba(0,0,0,0.25);
        height: 100%;
    }

    .info-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: rgba(238,242,251,0.5);
        margin-bottom: 0.25rem;
    }

    .info-value {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* ---------- Progress bars ---------- */
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #205295, #38bdf8, #d4af37) !important;
    }

    /* ---------- Dataframe / expander / info boxes native ---------- */
    div[data-testid="stExpander"] {
        background: linear-gradient(165deg, rgba(238,242,251,0.04), rgba(238,242,251,0.01));
        border: 1px solid rgba(238,242,251,0.09);
        border-radius: 14px;
    }

    hr { border-color: rgba(238,242,251,0.10) !important; }

    /* ---------- Footer ---------- */
    .footer {
        text-align: center;
        color: rgba(238,242,251,0.45);
        font-size: 0.82rem;
        padding: 2rem 0 0.6rem 0;
        line-height: 1.7;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD PREDICTOR
# ============================================================

@st.cache_resource
def load_predictor():
    return get_predictor()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero-wrap">
        <div class="main-title">🌍 World Flag AI</div>
        <div class="subtitle">Upload a flag image and let the AI identify the country.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sb-logo-wrap">
            <div class="sb-logo-badge">🌍</div>
            <div class="sb-title">World Flag AI</div>
            <div class="sb-subtitle">Global Flag Recognition</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="sb-section-label"><span class="icon-chip-sm">⚙️</span> Model Information</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sb-status-chip">● AI Model Online</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sb-card">
            <p>🧠 <b>Model:</b> World_Flag_AI_final.keras</p>
            <p>📐 <b>Input:</b> 300 × 300 × 3</p>
            <p>🌍 <b>Classes:</b> 194 countries</p>
            <p>⚙️ <b>Framework:</b> TensorFlow / Keras</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption(
        "World Flag AI identifies national flags "
        "using a deep learning image classifier."
    )


# ============================================================
# LOAD MODEL
# ============================================================

try:

    predictor = load_predictor()

except Exception as error:

    st.error("Unable to load the AI model.")

    st.exception(error)

    st.stop()


# ============================================================
# UPLOAD IMAGE
# ============================================================

st.markdown(
    '<div class="section-title">📤 Upload Flag</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Choose a flag image",
    type=["jpg", "jpeg", "png", "webp"],
    help="Upload a clear image of a national flag.",
)


# ============================================================
# PREDICTION
# ============================================================

if uploaded_file is not None:

    try:

        image = Image.open(uploaded_file)

        image = image.convert("RGB")

        col_image, col_result = st.columns(
            [1, 1.2],
            gap="large",
        )

        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        with col_image:

            st.markdown(
                '<div class="section-title">🖼️ Flag Image</div>',
                unsafe_allow_html=True,
            )

            st.image(
                image,
                use_container_width=True,
            )

            st.caption(
                f"Image size: {image.size[0]} × {image.size[1]}"
            )

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        with st.spinner("Analyzing flag..."):

            result = predictor.predict(image)

        country = result["country"]

        country_name = country.get(
            "country_name",
            "Unknown",
        )

        official_name = country.get(
            "official_name",
            "",
        )

        confidence = result.get(
            "confidence_percent",
            0,
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        with col_result:

            st.markdown(
                '<div class="section-title">🎯 Prediction</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="result-card">'
                f'<div class="country-name">{country_name}</div>'
                f'<div class="official-name">{official_name}</div>'
                f'<div class="confidence">{confidence:.2f}% confidence</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.write("")

            st.progress(
                min(float(confidence) / 100, 1.0)
            )

        
        # ====================================================
        # COUNTRY INFORMATION
        # ====================================================

        st.markdown(
            '<div class="section-title">📋 Country Information</div>',
            unsafe_allow_html=True,
        )

        info1, info2, info3 = st.columns(3)

        with info1:

            st.markdown(
                f"""
                <div class="info-box">
                    <div class="info-label">Capital</div>
                    <div class="info-value">
                        {country.get("capital", "N/A")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with info2:

            st.markdown(
                f"""
                <div class="info-box">
                    <div class="info-label">Continent</div>
                    <div class="info-value">
                        {country.get("continent", "N/A")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with info3:

            st.markdown(
                f"""
                <div class="info-box">
                    <div class="info-label">Region</div>
                    <div class="info-value">
                        {country.get("region", "N/A")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        info4, info5, info6 = st.columns(3)

        with info4:

            st.markdown(
                f"""
                <div class="info-box">
                    <div class="info-label">Currency</div>
                    <div class="info-value">
                        {country.get("currency", "N/A")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with info5:

            st.markdown(
                f"""
                <div class="info-box">
                    <div class="info-label">Languages</div>
                    <div class="info-value">
                        {country.get("languages", "N/A")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with info6:

            st.markdown(
                f"""
                <div class="info-box">
                    <div class="info-label">Independence</div>
                    <div class="info-value">
                        {country.get("independence_date", "N/A")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ====================================================
        # FLAG DESCRIPTION
        # ====================================================

        st.markdown(
            '<div class="section-title">🚩 Flag Description</div>',
            unsafe_allow_html=True,
        )

        st.info(
            country.get(
                "flag_description",
                "No flag description available.",
            )
        )

        # ====================================================
        # HISTORY
        # ====================================================

        st.markdown(
            '<div class="section-title">📖 Short History</div>',
            unsafe_allow_html=True,
        )

        st.write(
            country.get(
                "short_history",
                "No history available.",
            )
        )

        # ====================================================
        # INTERESTING FACT
        # ====================================================

        st.markdown(
            '<div class="section-title">💡 Interesting Fact</div>',
            unsafe_allow_html=True,
        )

        st.success(
            country.get(
                "interesting_fact",
                "No interesting fact available.",
            )
        )

        # ====================================================
        # NEIGHBORS
        # ====================================================

        neighbors = country.get(
            "neighbors",
            "",
        )

        if neighbors:

            st.markdown(
                '<div class="section-title">🗺️ Neighbors</div>',
                unsafe_allow_html=True,
            )

            st.write(neighbors)

        # ====================================================
        # TOP 5
        # ====================================================

        st.markdown(
            '<div class="section-title">📊 Top 5 Predictions</div>',
            unsafe_allow_html=True,
        )

        top_predictions = result.get(
            "top_predictions",
            [],
        )

        for position, item in enumerate(
            top_predictions,
            start=1,
        ):

            name = item.get(
                "country_name",
                "Unknown",
            )

            score = item.get(
                "confidence_percent",
                0,
            )

            col1, col2 = st.columns(
                [4, 1],
            )

            with col1:

                st.write(
                    f"**{position}. {name}**"
                )

            with col2:

                st.write(
                    f"{score:.2f}%"
                )

            st.progress(
                min(float(score) / 100, 1.0)
            )


    except UnidentifiedImageError:

        st.error(
            "The uploaded file is not a valid image."
        )

    except Exception as error:

        st.error(
            "Prediction failed."
        )

        st.exception(error)


# ============================================================
# NO IMAGE
# ============================================================

else:

    st.info(
        "👆 Upload a flag image above to start prediction."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🌍 World Flag AI
        <br>
        194-Class Deep Learning Flag Recognition System
        <br>
        TensorFlow • Keras • Python • Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)