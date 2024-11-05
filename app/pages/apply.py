import streamlit as st
import sys
import os

# Add the root path to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.models import Database, Application, JobPosting

def apply_page(job_id):
    st.title("Postuler pour un Stage")
    
    # Connect to the database and fetch job details
    db = Database()
    job_posting = JobPosting(db)
    job_details = job_posting.get_all_jobs()

    # Find the specific job by job_id
    job = next((job for job in job_details if job['id'] == job_id), None)

    if job:
        st.subheader(job['title'])
        st.write(job['description'])
        
        # Create the application form
        with st.form("application_form"):
            cv_text = st.text_area("Votre CV (texte)", height=200)
            submit = st.form_submit_button("Postuler")
            
            if submit:
                application = Application(db)
                user_id = st.session_state.user_id  # Assuming user_id is stored in session state
                
                if application.submit_application(user_id, job_id, cv_text):
                    st.success("Votre candidature a été soumise avec succès!")
                else:
                    st.error("Erreur lors de la soumission de la candidature.")
    else:
        st.error("Offre de stage introuvable.")

# Example usage
if __name__ == "__main__":
    job_id = 1  # Example job_id; replace with dynamic value as needed
    apply_page(job_id)
