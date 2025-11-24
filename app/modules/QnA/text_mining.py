# app/modules/nlp_engine.py
import math
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Initialize models (Cached to prevent reloading)
stemmer = StemmerFactory().create_stemmer()
sentiment_pipeline = pipeline("sentiment-analysis", model="w11wo/indonesian-roberta-base-sentiment-classifier")
# Using a multilingual model for Indonesian support
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def analyze_sentiment(text):
    """
    Returns a score between -1 (Negative) and 1 (Positive).
    """
    try:
        result = sentiment_pipeline(text)[0]
        label = result['label']
        score = result['score']
        
        if label == 'positive':
            return score
        elif label == 'negative':
            return -score
        else:
            return 0.0
    except:
        return 0.0

def calculate_relevance(answer, question_context=""):
    """
    Calculates semantic similarity between answer and context (or ideal answer).
    Since we don't have 'ideal answers' stored, we compute self-coherence 
    or keyword relevance. For this prototype, we assume the question implies keywords.
    """
    # In a real system, you'd compare 'answer' vs 'key_answer'.
    # Here, we check if the answer is relevant to the question context.
    
    sentences = [question_context, answer]
    embeddings = embedding_model.encode(sentences)
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return score

def grading_formula(sentiment_score, relevance_score):
    """
    Implements: Layak = (avg(Skor Jawaban) + (Skor Sentimen + 1)/2) / 2
    Note: 'Skor Jawaban' is essentially the Relevance Score here.
    """
    # Normalize sentiment (-1 to 1) to (0 to 1)
    normalized_sentiment = (sentiment_score + 1) / 2
    
    # Final Grade
    final_grade = (relevance_score + normalized_sentiment) / 2
    return final_grade

def extract_keywords(text_list, top_n=3):
    """Simple frequency-based keyword extraction using Sastrawi stemmer"""
    from collections import Counter
    import re
    
    all_text = " ".join(text_list)
    clean_text = re.sub(r'[^\w\s]', '', all_text).lower()
    words = clean_text.split()
    stemmed_words = [stemmer.stem(w) for w in words if len(w) > 3]
    
    counter = Counter(stemmed_words)
    return counter.most_common(top_n)

__all__ = [
    "analyze_sentiment",
    "calculate_relevance",
    "grading_formula",
    "extract_keywords",
]