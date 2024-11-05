import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import re
import spacy
import os
import h5py

class CVAnalyzer:
    def __init__(self):
        try:
            # Charger spaCy pour le traitement du texte en français
            self.nlp = spacy.load('fr_core_news_sm')
        except:
            # Si le modèle n'est pas installé, on le télécharge
            os.system('python -m spacy download fr_core_news_sm')
            self.nlp = spacy.load('fr_core_news_sm')
        
        self.vectorizer = TfidfVectorizer(
            stop_words='french',
            ngram_range=(1, 2),
            max_features=5000
        )
        self.scaler = MinMaxScaler()

    def preprocess_text(self, text):
        # Nettoyage basique du texte
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Traitement avec spaCy
        doc = self.nlp(text)
        # Garder seulement les tokens pertinents
        tokens = [token.lemma_ for token in doc 
                 if not token.is_stop and not token.is_punct]
        
        return ' '.join(tokens)

    def extract_skills(self, text):
        # Liste prédéfinie de compétences techniques
        technical_skills = {
            'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css',
            'react', 'angular', 'vue', 'node', 'django', 'flask',
            'machine learning', 'deep learning', 'ai', 'data science',
            'docker', 'kubernetes', 'aws', 'azure', 'git'
        }
        
        # Extraction des compétences du texte
        text_lower = text.lower()
        found_skills = []
        
        for skill in technical_skills:
            if skill in text_lower:
                found_skills.append(skill)
                
        return found_skills

    def calculate_experience_score(self, cv_text):
        # Recherche des années d'expérience
        experience_patterns = [
            r'(\d+)\s*ans?\s*d\'?expérience',
            r'expérience\s*:?\s*(\d+)\s*ans?',
            r'(\d+)\s*années?\s*d\'?expérience'
        ]
        
        max_years = 0
        for pattern in experience_patterns:
            matches = re.findall(pattern, cv_text.lower())
            if matches:
                years = max([int(match) for match in matches])
                max_years = max(max_years, years)
        
        # Score normalisé (maximum 15 ans pour 1.0)
        return min(max_years / 15.0, 1.0)

    def evaluate_cv(self, cv_text, job_requirements):
        """Évalue un CV par rapport aux exigences du poste"""
        # Prétraitement
        processed_cv = self.preprocess_text(cv_text)
        processed_req = self.preprocess_text(job_requirements)
        
        # Vectorisation
        tfidf_matrix = self.vectorizer.fit_transform([processed_req, processed_cv])
        
        # Calcul de similarité
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Extraction des compétences
        required_skills = set(self.extract_skills(job_requirements))
        cv_skills = set(self.extract_skills(cv_text))
        
        # Score des compétences
        if required_skills:
            skills_score = len(cv_skills.intersection(required_skills)) / len(required_skills)
        else:
            skills_score = 0.5
        
        # Score d'expérience
        experience_score = self.calculate_experience_score(cv_text)
        
        # Score final (pondéré)
        final_score = (
            similarity * 0.4 +  # Similarité globale
            skills_score * 0.4 +  # Compétences correspondantes
            experience_score * 0.2  # Expérience
        )
        
        return {
            'score': final_score,
            'similarity': similarity,
            'skills_match': skills_score,
            'experience_score': experience_score,
            'matched_skills': cv_skills.intersection(required_skills),
            'missing_skills': required_skills - cv_skills
        }

    def save_to_h5(self, filename):
        """Sauvegarde le modèle dans un fichier HDF5"""
        with h5py.File(filename, 'w') as h5file:
            # Sauvegarde le vocabulaire du vectorizer
            h5file.create_dataset('vocabulary', data=list(self.vectorizer.vocabulary_.keys()))
            # Si nécessaire, ajoutez d'autres attributs ou paramètres à sauvegarder

    @classmethod
    def load_from_h5(cls, filename):
        """Charge le modèle à partir d'un fichier HDF5"""
        instance = cls()
        with h5py.File(filename, 'r') as h5file:
            vocabulary = list(h5file['vocabulary'][:])
            instance.vectorizer = TfidfVectorizer(vocabulary=vocabulary)
            # Reconstituez les autres paramètres si nécessaire...
        return instance
