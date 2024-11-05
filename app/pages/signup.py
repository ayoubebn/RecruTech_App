# In your signup.py
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.models import Database, User

def signup_page():
    st.title("RecruTech - Inscription")
    
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        role = st.selectbox("Role", ["Recruteur", "Candidat"])
        submit = st.form_submit_button("S'inscrire")
        
        if submit:
            db = Database()
            user = User(db)
            if user.create_user(email, password, role):
                st.success("Compte créé avec succès!")
            else:
                st.error("Erreur lors de la création du compte, l'email pourrait déjà exister.")
