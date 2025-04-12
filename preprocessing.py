import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)
