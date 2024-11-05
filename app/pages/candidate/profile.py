import streamlit as st

def candidate_profile():
    st.title("Profil Candidat")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Prénom")
            st.text_input("Email")
            st.text_area("Résumé")
        with col2:
            st.text_input("Nom")
            st.text_input("Téléphone")
            st.file_uploader("CV", type=["pdf", "doc", "docx"])
        
        st.multiselect("Compétences", ["Python", "Java", "JavaScript", "SQL", "Machine Learning"])
        submit = st.form_submit_button("Mettre à jour le profil")
