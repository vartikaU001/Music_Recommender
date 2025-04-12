from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from preprocessing import clean_text
import requests
import base64
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load dataset
data = pd.read_csv('data/music_dataset.csv')

# Use a sample for faster processing
sample_size = int(0.1 * len(data))
data = data.sample(n=sample_size, random_state=1).reset_index(drop=True)

# Load credentials from environment variables
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

access_token = None
token_expires_at = 0

# Generate TF-IDF matrix for song text
def get_feature_matrix(data):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data['text'])
    return tfidf_matrix, vectorizer

# Fetch new Spotify access token
def fetch_access_token():
    global access_token, token_expires_at

    if time.time() < token_expires_at:
        return access_token  # Return cached token

    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("ascii")

    headers = {
        "Authorization": f"Basic {auth_header}"
    }
    data_form = {
        "grant_type": "client_credentials"
    }

    response = requests.post(auth_url, headers=headers, data=data_form)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        expires_in = token_data.get("expires_in", 3600)
        token_expires_at = time.time() + expires_in
        print("Access token fetched successfully")
        return access_token
    else:
        print("Error fetching access token:", response.json())
        return None

# Get album image using Spotify API
def get_album_image(song_name, artist_name):
    token = fetch_access_token()
    if not token:
        return "static/default_image.jpg"

    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'q': f'track:{song_name} artist:{artist_name}',
        'type': 'track',
        'limit': 1
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        tracks = response.json()['tracks']['items']
        if tracks:
            return tracks[0]['album']['images'][0]['url']
    else:
        print(f"Error fetching image for {song_name}: {response.json()}")

    return "static/default_image.jpg"

# Prepare the feature matrix
tfidf_matrix, vectorizer = get_feature_matrix(data)

# Home page
@app.route('/')
def index():
    song_titles = data['song'].tolist()[:10]
    return render_template('index.html', song_titles=song_titles)

# Recommendation route
@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['song']
    recommendations = recommend_songs(user_input, data, tfidf_matrix, vectorizer)

    for song in recommendations:
        song['image_url'] = get_album_image(song['song'], song['artist'])

    return render_template('index.html', song_titles=data['song'].tolist(), recommendations=recommendations, selected_song=user_input)

# Recommend songs using cosine similarity
def recommend_songs(user_input, data, tfidf_matrix, vectorizer):
    user_input_cleaned = clean_text(user_input)
    user_tfidf = vectorizer.transform([user_input_cleaned])
    cosine_similarities = linear_kernel(user_tfidf, tfidf_matrix).flatten()
    recommended_indices = cosine_similarities.argsort()[-6:][::-1]
    recommended_songs = data.iloc[recommended_indices]
    return recommended_songs[['artist', 'song']].to_dict(orient='records')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
