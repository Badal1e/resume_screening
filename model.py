import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import clean_text

class ResumeRanker:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.df['cleaned'] = self.df['Resume_str'].apply(clean_text)

        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.resume_vectors = self.vectorizer.fit_transform(self.df['cleaned'])

    def rank_resumes(self, job_description):
        job_clean = clean_text(job_description)
        job_vector = self.vectorizer.transform([job_clean])

        scores = cosine_similarity(job_vector, self.resume_vectors)[0]
        self.df['score'] = scores

        ranked = self.df.sort_values(by='score', ascending=False)
        return ranked[['ID', 'Category', 'score']].head(10)