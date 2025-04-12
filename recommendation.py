import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from preprocessing import clean_text  
import requests  

data = pd.read_csv('data/music_dataset.csv')

def get_feature_matrix(data):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data['text'])
    return tfidf_matrix, vectorizer

def get_album_image(song_name, artist_name, access_token):
    search_url = 'https://api.spotify.com/v1/search'
    
    headers = {
        'Authorization': f'Bearer {access_token}'
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
            
            album_image_url = tracks[0]['album']['images'][0]['url']
            return album_image_url
        else:
            return "No image found"
    else:
        print(f"Error fetching image for {song_name}: {response.json()}")
        return None

tfidf_matrix, vectorizer = get_feature_matrix(data)

def recommend_songs(user_input, data, tfidf_matrix, vectorizer, access_token):
    user_input_cleaned = clean_text(user_input)  
    user_tfidf = vectorizer.transform([user_input_cleaned])  
    cosine_similarities = linear_kernel(user_tfidf, tfidf_matrix).flatten()
    
    recommended_indices = cosine_similarities.argsort()[-5:][::-1]
    
    recommended_songs = data.iloc[recommended_indices]
    
    recommendations_with_images = []
    for index, row in recommended_songs.iterrows():
        image_url = get_album_image(row['song'], row['artist'], access_token)  
        recommendations_with_images.append({
            'artist': row['artist'],
            'song': row['song'],
            'image_url': image_url  
        })
    
    return recommendations_with_images
