`2.20.0`

````markdown
# 🌍 World Flag AI

<div align="center">

# 🌍 WORLD FLAG AI

### AI-Powered National Flag Recognition System

**Identify 194 national flags using Deep Learning + Computer Vision**

<br>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST_API-000000?style=for-the-badge&logo=flask&logoColor=white)
![Computer Vision](https://img.shields.io/badge/Computer-Vision-6A5ACD?style=for-the-badge)
![Deep Learning](https://img.shields.io/badge/Deep-Learning-8A2BE2?style=for-the-badge)

<br>

**Upload a flag → AI analyzes it → Country identified → Country information displayed**

</div>

---

# 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Project Goal](#-project-goal)
- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [Machine Learning Model](#-machine-learning-model)
- [Dataset](#-dataset)
- [Dataset Scraping](#-dataset-scraping)
- [Dataset Preparation](#-dataset-preparation)
- [Country Information](#-country-information)
- [Project Structure](#-project-structure)
- [Core Predictor](#-core-predictor)
- [Streamlit Application](#-streamlit-application)
- [Flask Application](#-flask-application)
- [API Endpoint](#-api-endpoint)
- [Testing](#-testing)
- [Installation](#-installation)
- [Running the Streamlit App](#-running-the-streamlit-app)
- [Running the Flask App](#-running-the-flask-app)
- [Example Workflow](#-example-workflow)
- [Applications](#-where-can-it-be-used)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)
- [Technologies](#-technologies-used)
- [Author](#-author)

---

# 🌎 About the Project

**World Flag AI** is an AI-powered computer vision application designed to recognize national flags from images.

The system uses a deep learning image classification model trained to recognize **194 different flag classes**.

After identifying a flag, the application retrieves information about the predicted country from a local country database.

The system can provide:

- Country name
- Official country name
- Capital
- Continent
- Region
- Subregion
- ISO Alpha-2 code
- ISO Alpha-3 code
- Independence date
- National day
- Currency
- Languages
- Flag description
- Short history
- Interesting facts
- Neighboring countries

The project provides **two interfaces**:

### 🖥️ Streamlit

A user-friendly graphical interface where users can upload a flag image and receive an AI prediction.

### 🔌 Flask

A REST API that allows other applications, websites, or services to send flag images and receive prediction results in JSON format.

---

# 🎯 Project Goal

The main goal of World Flag AI is to demonstrate how **Computer Vision, Deep Learning, Python, and Web Development** can be combined to create a practical AI application.

Instead of manually searching for a country's flag, the user can simply provide an image.

The AI performs:

```text
Image
   ↓
Image Preprocessing
   ↓
Deep Learning Model
   ↓
Class Prediction
   ↓
Class ID
   ↓
Country Database
   ↓
Country Information
   ↓
Final Result
````

---

# ✨ Key Features

## 🤖 AI Flag Recognition

Recognizes flags from **194 different classes**.

## 🖼️ Image Upload

Users can upload:

* JPG
* JPEG
* PNG
* WEBP

## 🎯 Confidence Score

The application displays the model's confidence for the predicted country.

Example:

```text
Mexico
United Mexican States

96.82% confidence
```

## 📊 Top-5 Predictions

The system also displays the five most likely predictions.

Example:

```text
1. Mexico       96.82%
2. Ecuador       1.42%
3. Colombia      0.73%
4. Peru          0.51%
5. Bolivia       0.31%
```

## 🌍 Country Information

After classification, the application uses the predicted class to retrieve country information.

## 🚩 Flag Description

Provides information describing the visual structure of the country's flag.

## 📖 Historical Information

Displays a short historical overview of the country.

## 💡 Interesting Facts

Provides an interesting fact about the predicted country.

## 🗺️ Neighboring Countries

Displays geographical neighbors where available.

## 🔌 REST API

Flask provides an API endpoint for programmatic predictions.

## 💾 Local Model

The trained Keras model is stored locally and loaded when the application starts.

---

# 🧠 Machine Learning Model

The project uses a TensorFlow/Keras image classification model.

### Model

```text
World_Flag_AI_final.keras
```

### Input

```text
300 × 300 × 3
```

The input represents:

```text
Height = 300
Width  = 300
Channels = 3
```

The three channels represent:

```text
RGB
```

### Output

```text
194 classes
```

Each output index corresponds to a country class.

The predictor converts the model's zero-based output index into the project's one-based `class_id`.

For example:

```text
Model index 0
      ↓
class_id 1

Model index 108
      ↓
class_id 109
```

---

# 📊 Dataset

The World Flag AI dataset contains flag images organized by country.

The project contains:

```text
194 country classes
```

The dataset was prepared as a country-based image classification dataset.

Each country has its own folder/class.

Example:

```text
dataset/
│
├── Afghanistan/
├── Albania/
├── Algeria/
├── Andorra/
├── Angola/
├── Argentina/
├── Australia/
├── Austria/
├── ...
├── Pakistan/
├── Palestine/
├── ...
└── Zimbabwe/
```

The project intentionally contains:

```text
Palestine
```

and does not contain:

```text
Israel
```

---

# 🔎 Dataset Scraping

The flag dataset was created using automated image searching/scraping.

The purpose of scraping was to collect multiple real-world examples of national flags instead of manually downloading every image.

The scraping workflow was:

```text
Country List
     ↓
Search Flag Images
     ↓
Download Images
     ↓
Validate Images
     ↓
Remove Invalid Images
     ↓
Organize by Country
     ↓
Create Dataset
```

The project used image search results to collect flag images for the different countries.

The dataset collection process was especially useful because national flags can appear in many different forms:

* Official flag images
* Different aspect ratios
* Photographs
* Flags displayed outdoors
* Flags displayed indoors
* Slightly different lighting
* Different resolutions
* Different backgrounds

This gives the model exposure to more realistic images.

---

# 🧹 Dataset Preparation

Before training, the dataset was organized into class folders.

The general structure was:

```text
Country
   ↓
Multiple Flag Images
   ↓
Image Validation
   ↓
Training / Validation Split
   ↓
Model Training
```

Images were resized during preprocessing to:

```text
300 × 300
```

The predictor also converts all images to RGB before prediction.

This ensures that grayscale, palette, or other image formats are converted into a consistent three-channel format.

---

# 🗂️ Country Information Database

The project uses:

```text
country_data/countries.json
```

This file maps each model class to a country.

Each country record contains information such as:

```json
{
    "class_id": 109,
    "country_name": "Mexico",
    "official_name": "United Mexican States",
    "capital": "Mexico City",
    "continent": "North America",
    "region": "North America",
    "subregion": "Central America",
    "iso_alpha_2": "MX",
    "iso_alpha_3": "MEX",
    "independence_date": "16 September 1810",
    "national_day": "16 September",
    "currency": "Mexican peso (MXN)",
    "languages": "Spanish and numerous Indigenous languages",
    "flag_description": "...",
    "short_history": "...",
    "interesting_fact": "...",
    "neighbors": "United States, Guatemala, Belize"
}
```

The important relationship is:

```text
Model class
     ↓
class_id
     ↓
countries.json
     ↓
Country information
```

This allows the AI model to focus on visual classification while the JSON database provides human-readable information.

---

# 🧩 Core Predictor

The main prediction logic is located at:

```text
core/predictor.py
```

The predictor performs several important tasks.

### 1. Load the country database

```text
countries.json
```

### 2. Validate country classes

It verifies that:

```text
194 records exist
```

and:

```text
class IDs = 1 → 194
```

### 3. Verify Palestine

The predictor checks that Palestine exists.

### 4. Verify Israel is absent

The predictor checks that Israel is not included.

### 5. Load the trained model

```text
World_Flag_AI_final.keras
```

### 6. Validate model input

```text
(None, 300, 300, 3)
```

### 7. Validate model output

```text
(None, 194)
```

### 8. Preprocess images

Images are:

```text
Converted to RGB
        ↓
Resized to 300 × 300
        ↓
Converted to NumPy
        ↓
Batch dimension added
```

### 9. Predict

The model produces probabilities for all 194 classes.

### 10. Select best prediction

The highest probability becomes the predicted country.

### 11. Generate Top-5

The predictor sorts the output probabilities and returns the five highest predictions.

---

# 🖥️ Streamlit Application

The Streamlit application is located at:

```text
streamlit_app/app.py
```

It provides the main user interface.

The application allows users to:

1. Open the application.
2. Upload a flag image.
3. Preview the image.
4. Run AI prediction.
5. View predicted country.
6. View confidence.
7. View country information.
8. View flag description.
9. View history.
10. View interesting facts.
11. View neighboring countries.
12. View Top-5 predictions.

The application uses the same predictor as the Flask API.

This prevents duplication of the machine learning logic.

---

# 🔌 Flask Application

The Flask application is located at:

```text
flask_app/
```

Main application:

```text
flask_app/app.py
```

Flask provides a web server and REST API.

The Flask application loads the model once:

```text
WorldFlagPredictor()
```

This prevents the model from being loaded for every request.

---

# 🌐 Flask API

The main prediction endpoint is:

```text
POST /api/predict
```

The request should contain an image using the field:

```text
image
```

Example request concept:

```text
POST /api/predict
Content-Type: multipart/form-data

image = flag.jpg
```

The API returns JSON containing:

```text
class_id
country
confidence
confidence_percent
top_predictions
country_info
```

---

# ❤️ Health Endpoint

The Flask application also provides:

```text
GET /health
```

This can be used to check whether the AI application is online.

It also provides model information such as:

```text
Model
Input shape
Output shape
Number of classes
Image size
Metadata file
```

Example:

```json
{
    "status": "online",
    "classes": 194,
    "image_size": [300, 300]
}
```

---

# 🧪 Testing

Testing files are located inside:

```text
tests/
```

The project contains prediction and model tests.

Example structure:

```text
tests/
│
├── test_model.py
├── test_predictor.py
└── test_images/
```

The test images were used to evaluate how the trained model behaves on individual country flags.

The project also performed class-by-class confusion analysis.

This helped identify difficult classes and visually similar flags.

Examples of difficult flag pairs/classes included:

```text
Congo
Democratic Republic of the Congo

Netherlands
Luxembourg

Austria
Monaco

Chad
Romania

Guinea
Benin

Côte d'Ivoire
Ireland

Italy
Monaco
```

These cases are challenging because several national flags have very similar colors, layouts, or patterns.

---

# 🧠 Confusion Analysis

A class-by-class evaluation was performed to understand model behavior.

For example:

```text
TRUE CLASS: Congo

Correct: 0
Wrong: 5

Predicted as:
Democratic_Republic_of_the_Congo → 5
```

This type of analysis is useful because overall accuracy alone does not explain which countries are difficult for the model.

It helps identify:

* Similar flags
* Weak classes
* Dataset problems
* Image quality problems
* Potential class imbalance
* Model confusion

---

# 📈 Model Improvement

The model evaluation showed significant improvements for several difficult classes.

Examples included:

```text
Luxembourg     40% → 100%
Libya          60% → 100%
Austria        20% → 60%
Bahrain        60% → 100%
Argentina      60% → 100%
Lesotho        60% → 100%
Namibia        60% → 100%
Honduras       60% → 100%
Australia      60% → 100%
Philippines    60% → 100%
Peru           60% → 100%
```

However, some classes became harder after the model changes.

Examples included:

```text
Congo          60% → 0%
Netherlands    60% → 0%
Italy          100% → 60%
Finland        100% → 60%
Bolivia         80% → 40%
Myanmar        100% → 60%
```

This demonstrates why class-by-class evaluation is important when improving a multi-class image classifier.

---

# 📁 Project Structure

```text
World_Flag_AI_App/
│
├── .gitignore
├── README.md
├── requirements.txt
├── generate_countries.py
├── enrich_countries.py
│
├── core/
│   ├── __init__.py
│   ├── predictor.py
│   └── country_info.py
│
├── country_data/
│   └── countries.json
│
├── country_info/
│   └── country information files
│
├── model/
│   └── World_Flag_AI_final.keras
│
├── flask_app/
│   ├── __init__.py
│   ├── app.py
│   ├── routes.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   │
│   │   └── js/
│   │       └── app.js
│   │
│   └── templates/
│       └── index.html
│
├── streamlit_app/
│   └── app.py
│
└── tests/
    ├── test_model.py
    ├── test_predictor.py
    └── test_images/
```

---

# 📄 Important Files

| File                                | Purpose                              |
| ----------------------------------- | ------------------------------------ |
| `core/predictor.py`               | Loads model and performs predictions |
| `core/country_info.py`            | Loads country information            |
| `country_data/countries.json`     | Country metadata                     |
| `model/World_Flag_AI_final.keras` | Trained AI model                     |
| `streamlit_app/app.py`            | Streamlit user interface             |
| `flask_app/app.py`                | Flask application                    |
| `flask_app/routes.py`             | Flask routes                         |
| `flask_app/templates/index.html`  | Flask frontend                       |
| `flask_app/static/css/style.css`  | Flask UI styling                     |
| `flask_app/static/js/app.js`      | Frontend JavaScript                  |
| `tests/test_model.py`             | Model tests                          |
| `tests/test_predictor.py`         | Predictor tests                      |
| `generate_countries.py`           | Country data generation              |
| `enrich_countries.py`             | Country information enrichment       |

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/World_Flag_AI_App.git
```

Enter the project:

```bash
cd World_Flag_AI_App
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 📦 Requirements

The project uses technologies including:

```text
Python
TensorFlow==2.20.0
Keras
NumPy
Pillow
Flask
Streamlit
```

The exact package versions are maintained in:

```text
requirements.txt
```

---

# 🚀 Run Streamlit

From the project root:

```bash
streamlit run streamlit_app/app.py
```

Streamlit will start the application locally.

Open the address shown in the terminal, normally:

```text
http://localhost:8501
```

---

# 🚀 Run Flask

From the project root:

```bash
python flask_app/app.py
```

The Flask application runs at:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/health
```

---

# 🖼️ Prediction Workflow

The complete prediction pipeline is:

```text
              USER
                │
                ▼
        Upload Flag Image
                │
                ▼
        Streamlit / Flask
                │
                ▼
        PIL Image Processing
                │
                ▼
          Convert to RGB
                │
                ▼
        Resize 300 × 300
                │
                ▼
      World Flag AI Model
                │
                ▼
        194 Class Scores
                │
                ▼
        Highest Prediction
                │
                ▼
             class_id
                │
                ▼
        countries.json
                │
                ▼
      Country Information
                │
                ▼
        Final AI Response
```

---

# 🌍 Where Can It Be Used?

World Flag AI can be used in several practical areas.

## 🎓 Education

Students can upload a flag and learn:

* Country name
* Capital
* History
* Geography
* Currency
* Languages
* Flag meaning

It can be used as an interactive geography learning tool.

---

## 🧳 Travel Applications

Travel applications could use the model to identify flags appearing in:

* Travel photographs
* Airports
* Hotels
* Tourist locations
* International events

---

## 🏫 Educational Games

The model can be integrated into:

* Flag quizzes
* Geography games
* Learning platforms
* Classroom applications

For example:

```text
Show flag
     ↓
User guesses country
     ↓
AI verifies answer
     ↓
Display country information
```

---

## 📱 Mobile Applications

The Flask API can serve as the backend for a mobile application.

A mobile application could:

```text
Take photo
    ↓
Send image to API
    ↓
AI identifies flag
    ↓
Receive JSON
    ↓
Display country information
```

---

## 🌐 Web Applications

The Flask REST API can be integrated into:

* Websites
* Educational portals
* Geography platforms
* Travel websites
* Online quizzes

---

## 🔬 Computer Vision Research

The project can also serve as an example of:

* Multi-class image classification
* Transfer learning
* Dataset creation
* Image preprocessing
* Model evaluation
* Confusion analysis
* AI deployment

---

# 🔐 Git & Large Files

The trained model is approximately:

```text
68.18 MB
```

Because trained models can be large, model files may be excluded from Git using:

```gitignore
model/*.keras
```

If the model is required for deployment, it can be hosted using an appropriate model/file hosting solution and downloaded by the deployment environment.

The `.gitignore` also excludes:

```text
.venv/
__pycache__/
.env
*.log
```

This keeps unnecessary and sensitive files out of the Git repository.

---

# ☁️ Streamlit Deployment

The Streamlit application can be deployed as a cloud application.

Typical deployment flow:

```text
GitHub Repository
       ↓
Streamlit Deployment
       ↓
Install requirements.txt
       ↓
Load Model
       ↓
Start Streamlit
       ↓
Public Web Application
```

Before deployment, make sure the deployment environment can access:

```text
World_Flag_AI_final.keras
```

and:

```text
country_data/countries.json
```

---

# ⚠️ Important Deployment Consideration

The Keras model is approximately:

```text
68.18 MB
```

Therefore, the model should be handled carefully when deploying.

The application requires:

```text
TensorFlow
Keras
NumPy
Pillow
```

and sufficient memory for loading the model.

---

# 🛑 Limitations

Although the system can recognize many flags accurately, image classification has limitations.

## Similar Flags

Some countries have extremely similar flags.

Examples:

```text
Congo
Democratic Republic of the Congo

Chad
Romania

Austria
Latvia

Netherlands
Luxembourg

Ireland
Côte d'Ivoire

Italy
Monaco
```

Small visual differences can be difficult for a neural network.

---

## Image Quality

Very low-quality images can reduce prediction accuracy.

Examples:

* Blurry images
* Extremely dark images
* Cropped flags
* Heavy compression
* Obstructed flags
* Flags with unusual backgrounds

---

## Non-Flag Images

The model is designed for the 194 trained classes.

It may still produce a country prediction when the uploaded image is not actually a flag.

This is because a standard classifier chooses one of its known classes even when the image is outside the training distribution.

---

# 🔮 Future Improvements

Possible future improvements include:

### 1. More Training Images

Increase the number and diversity of images per country.

### 2. Better Difficult-Class Data

Focus specifically on confusing classes.

For example:

```text
Congo
DR Congo
Chad
Romania
Austria
Latvia
Netherlands
Luxembourg
Italy
Monaco
```

### 3. Better Data Cleaning

Remove:

* Duplicates
* Incorrect flags
* Logos
* Maps
* Unrelated images
* Watermarked images

### 4. Confidence Threshold

Add an unknown/uncertain result:

```text
Confidence < threshold
        ↓
"Unable to confidently identify this flag."
```

### 5. Mobile Application

Create a mobile application that communicates with the Flask API.

### 6. Camera Support

Allow users to point a camera at a physical flag.

### 7. Improved Country Database

Expand country information with:

* Detailed history
* Population
* Area
* Time zones
* Government
* Geography
* National symbols
* Major cities
* Cultural information
* Famous landmarks

### 8. Country Information

After identifying a flag, the application displays detailed information about the predicted country, including:

- Country name
- Official name
- Capital
- Continent
- Region
- Subregion
- ISO country codes
- Currency
- Languages
- Independence date
- National day
- Flag description
- Short history
- Interesting facts
- Neighboring countries

> Multilingual country information can be added as a future enhancement.

Optimize the model for:

* Faster inference
* Lower memory usage
* Mobile deployment
* Edge devices

# 🏗️ Architecture

The project follows a modular architecture.

```text
                   ┌──────────────────┐
                   │   User Image     │
                   └────────┬─────────┘
                            │
                 ┌──────────▼──────────┐
                 │ Streamlit / Flask   │
                 └──────────┬──────────┘
                            │
                 ┌──────────▼──────────┐
                 │  Core Predictor     │
                 └──────────┬──────────┘
                            │
                 ┌──────────▼──────────┐
                 │ TensorFlow / Keras │
                 │   194 Classes      │
                 └──────────┬──────────┘
                            │
                       class_id
                            │
                 ┌──────────▼──────────┐
                 │   countries.json   │
                 └──────────┬──────────┘
                            │
                 ┌──────────▼──────────┐
                 │ Country Information │
                 └──────────┬──────────┘
                            │
                 ┌──────────▼──────────┐
                 │   Final Response    │
                 └─────────────────────┘
```

---

# 🛠️ Technologies Used

## Programming

```text
Python
```

## Machine Learning

```text
TensorFlow
Keras
NumPy
```

## Image Processing

```text
Pillow
```

## Frontend

```text
Streamlit
HTML
CSS
JavaScript
```

## Backend

```text
Flask
REST API
```

## Data

```text
JSON
Image Dataset
```

## Development Tools

```text
VS Code
Git
GitHub
Python Virtual Environment
```

---

# 📌 Project Highlights

```text
🌍 194 Country Classes
🤖 Deep Learning Image Classifier
🖼️ Image Upload
🎯 Confidence Prediction
📊 Top-5 Predictions
📖 Country History
🚩 Flag Description
💡 Interesting Facts
🗺️ Neighboring Countries
🖥️ Streamlit Interface
🔌 Flask REST API
🧪 Model Testing
📈 Class-by-Class Confusion Analysis
🗂️ Structured Country Database
```

---

# 🧪 Example

User uploads:

```text
mexico_flag.jpg
```

The system processes the image:

```text
Image
 ↓
RGB Conversion
 ↓
300 × 300 Resize
 ↓
AI Model
 ↓
Class ID
 ↓
Mexico
```

The application then displays:

```text
🇲🇽 Mexico

United Mexican States

Confidence: XX.XX%
```

followed by country information such as:

```text
Capital:
Mexico City

Continent:
North America

Region:
North America

Currency:
Mexican peso

Languages:
Spanish and Indigenous languages
```

---

# 🎓 Learning Outcomes

This project demonstrates practical experience with:

* Python programming
* Computer Vision
* Deep Learning
* Image Classification
* TensorFlow/Keras
* Dataset collection
* Dataset scraping
* Image preprocessing
* Model evaluation
* Confusion analysis
* JSON data management
* Flask REST APIs
* Streamlit applications
* Git/GitHub
* AI deployment

---

# 🚀 Final Project Workflow

```text
1. Collect country list
          ↓
2. Scrape flag images
          ↓
3. Validate dataset
          ↓
4. Organize country classes
          ↓
5. Train deep learning model
          ↓
6. Evaluate model
          ↓
7. Analyze class confusion
          ↓
8. Save trained Keras model
          ↓
9. Build predictor
          ↓
10. Connect country metadata
          ↓
11. Build Streamlit UI
          ↓
12. Build Flask API
          ↓
13. Test applications
          ↓
14. Deploy
```

---

# 📜 License

This project is intended for educational, research, and demonstration purposes.

Dataset images may have their own individual licenses and usage restrictions depending on their original sources.

Always verify image licensing before using the dataset or individual images commercially.

---

# 👨‍💻 Author

## Momin Butt

**Artificial Intelligence & Data Science Developer**

### Skills Demonstrated

```text
Python
Data Science
Machine Learning
Deep Learning
Computer Vision
TensorFlow
Keras
Flask
Streamlit
REST APIs
Git & GitHub
```

---

# ⭐ Project Summary

**World Flag AI** combines a deep learning image classifier with a structured country information database to create an interactive national flag recognition system.

The project demonstrates the complete AI development lifecycle:

```text
Dataset Collection
        ↓
Dataset Scraping
        ↓
Data Preparation
        ↓
Deep Learning
        ↓
Model Evaluation
        ↓
Prediction Pipeline
        ↓
Country Knowledge Database
        ↓
Web Application
        ↓
REST API
        ↓
Deployment
```

The result is a complete **AI-powered World Flag Recognition System** capable of recognizing **194 national flag classes** and presenting useful information about the predicted country.

---

<div align="center">
