import streamlit as st
from app.models import Database, JobPosting

def add_job_posting_page():
    st.title("Ajouter une Offre de Stage")
    
    db = Database()
    job_posting = JobPosting(db)

    with st.form("add_job_form"):
        title = st.text_input("Titre de l'offre")
        description = st.text_area("Description")
        requirements = st.text_area("Exigences")

        submit_button = st.form_submit_button("Ajouter l'offre")

        if submit_button:
            if title and description and requirements:
                job_id = job_posting.create_job(title, description, requirements)
                if job_id:
                    st.success("L'offre a été ajoutée avec succès!")
                else:
                    st.error("Erreur lors de l'ajout de l'offre.")
            else:
                st.error("Veuillez remplir tous les champs.")

if __name__ == "__main__":
    add_job_posting_page()
