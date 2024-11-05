import streamlit as st
import sys
import os
from app.models import Database, User


# Ajout du chemin racine au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.models import Database, User

def login_page():
    st.title("RecruTech - Connexion")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")
        
        if submit:
            db = Database()
            user = User(db)  # Make sure User class is defined to take db as an argument
            # Here you should implement the login logic (e.g., verifying email and password)
            st.success("Connexion réussie!")

# In your User class, implement the method to get user by email
class User:
    # existing methods...

    def get_user_by_email(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            return cursor.fetchone()  # Returns a single record or None
        finally:
            cursor.close()
            conn.close()
