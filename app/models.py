import sqlite3
import pickle
import re
from config import Config

class Database:
    def get_connection(self):
        return sqlite3.connect(Config.SQLITE_DB_PATH)

class User:
    def __init__(self, db):
        self.db = db

    def create_user(self, email, password, role):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                (email, password, role)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:  # Handle unique constraint violation
            print("L'email existe déjà. Veuillez en choisir un autre.")
            return False
        except Exception as e:
            print(f"Erreur: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

class CVAnalyzer:
    def evaluate_cv(self, cv_text, job_requirements):
        score = 0
        evaluation_details = {}
        required_keywords = [kw.strip().lower() for kw in job_requirements.split(",")]
        
        for keyword in required_keywords:
            occurrences = len(re.findall(r'\b' + re.escape(keyword) + r'\b', cv_text.lower()))
            evaluation_details[keyword] = occurrences
            score += occurrences
            
        max_score = len(required_keywords)
        final_score = (score / max_score) * 100 if max_score > 0 else 0
        
        return {
            "score": final_score,
            "details": evaluation_details
        }

class JobPosting:
    def __init__(self, db):
        self.db = db

    def create_job(self, title, description, requirements):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO job_postings 
                   (title, description, requirements) 
                   VALUES (?, ?, ?)""",
                (title, description, requirements)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def get_all_jobs(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM job_postings")
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

class Application:
    def __init__(self, db):
        self.db = db
        self.cv_analyzer = CVAnalyzer()

    def submit_application(self, user_id, job_id, cv_text):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT requirements FROM job_postings WHERE id = ?",
                (job_id,)
            )
            job_requirements = cursor.fetchone()[0]
            evaluation = self.cv_analyzer.evaluate_cv(cv_text, job_requirements)
            cursor.execute(
                """INSERT INTO applications 
                   (user_id, job_id, cv_text, score, evaluation_details) 
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, job_id, cv_text, evaluation['score'], 
                 pickle.dumps(evaluation))
            )
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    def get_applications_for_job(self, job_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT a.*, u.email, j.title as job_title
                FROM applications a
                JOIN users u ON a.user_id = u.id
                JOIN job_postings j ON a.job_id = j.id
                WHERE a.job_id = ?
                ORDER BY a.score DESC
            """, (job_id,))
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
