import streamlit as st
import pandas as pd

def recruiter_dashboard():
    st.title("Tableau de bord Recruteur")
    
    # Statistiques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Offres actives", "5")
    with col2:
        st.metric("Candidatures reçues", "25")
    with col3:
        st.metric("Entretiens planifiés", "3")
    
    # Liste des offres
    st.subheader("Vos offres d'emploi")
    job_data = {
        "Titre": ["Développeur Python", "Data Scientist", "DevOps Engineer"],
        "Candidatures": [12, 8, 5],
        "Status": ["Active", "Active", "En pause"]
    }
    df = pd.DataFrame(job_data)
    st.dataframe(df)