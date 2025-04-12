# 🎵 Music Recommender System

This is a Python-based music recommendation system that suggests songs based on user preferences and data analysis.

## 🚀 Features

| Feature               | Description                                                  |
|----------------------|--------------------------------------------------------------|
| 🎧 Music Recommendations | Suggests songs using audio features and similarity analysis |
| 🔐 Token-Based Access    | Secure access with token generation                         |
| 🧼 Data Preprocessing     | Handles and processes raw music data                        |
| 🌐 Web Interface         | Simple web UI using Flask, HTML, and CSS                    |

## 📁 Project Structure

| Folder/File        | Purpose                            |
|--------------------|------------------------------------|
| `app.py`           | Main Flask application             |
| `main.py`          | Driver script for recommender      |
| `get_token.py`     | Token generation logic             |
| `preprocessing.py` | Data cleaning and feature handling |
| `recommendation.py`| Recommendation engine              |
| `requirements.txt` | Python dependencies                |
| `templates/`       | HTML frontend                      |
| `static/`          | CSS/JS frontend assets             |
| `data/`            | Music dataset or model files       |

## 📦 Setup Instructions

```bash
# Clone the repository
git clone https://github.com/vartikaU001/music-recommender.git
cd music-recommender

# Create and activate virtual environment
python -m venv env
env\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
