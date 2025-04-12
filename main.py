import pandas as pd
from recommendation import get_feature_matrix, recommend_songs

data = pd.read_csv('data/music_dataset.csv')
print("Columns in the dataset:", data.columns)

feature_matrix, vectorizer = get_feature_matrix(data)

user_input = "Enter a description or keywords related to your music preference here."
recommendations = recommend_songs(user_input, data, feature_matrix, vectorizer)

print("Recommended songs:")
print(recommendations[['song', 'artist', 'text']])
