from text_cleaning.bag_of_words import BagOfWords
from text_cleaning.tf_idf import TFIDF
from text_cleaning.word_embedding import WordEmbedding

# ====================================================
# 🧱 BAG OF WORDS
# ====================================================
print("\n=== Bag of Words ===")
bow = BagOfWords()
X_bow = bow.fit_transform(["this is a test", "this is another test"])
print("Features:", bow.get_feature_names())
print("BoW Matrix:\n", X_bow.toarray())

# ====================================================
# 🔢 TF-IDF
# ====================================================
print("\n=== TF-IDF ===")
tfidf = TFIDF()
X_tfidf = tfidf.fit_transform(["this is a test", "this is another test"])
print("TF-IDF Matrix:\n", X_tfidf.toarray())

# ====================================================
# 🧠 WORD EMBEDDING
# ====================================================
print("\n=== Word Embedding ===")

# You can choose: "en_core_web_md", "xx_ent_wiki_sm", "id_core_news_md", etc.
embed = WordEmbedding(lang_model="xx_ent_wiki_sm")

sentences = [
    "AI interviewer project",
    "machine learning pipeline",
]

X_embed = embed.transform(sentences)
print("Embeddings shape:", X_embed.shape)
print("Sample embedding vector (first sentence):\n", X_embed[0][:10])  # preview first 10 dims

print("\n✅ All feature extraction tests completed successfully.")
