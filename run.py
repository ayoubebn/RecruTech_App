import streamlit as st
import sys
import os
from dotenv import load_dotenv
from app.models import Database, JobPosting
from app.pages.apply import apply_page
from app.pages.add_job_posting import add_job_posting_page  # Import the new page

# Load environment variables from .env file
load_dotenv()

# Set page configuration at the start
st.set_page_config(
    page_title="RecruTech",
    page_icon="👥",
    layout="wide"
)

# Add the root path to PYTHONPATH
sys.path.append(os.path.dirname(__file__))

# Importing required pages
try:
    from app.pages.login import login_page
    from app.pages.signup import signup_page
    from app.pages.recruiter.dashboard import recruiter_dashboard
    from app.pages.candidate.profile import candidate_profile
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# Placeholder function for the view_applications page
def view_applications():
    st.title("Analyse des Candidatures")
    st.write("Cette page est dédiée à l'analyse des candidatures.")

def job_postings_page():
    st.title("Offres de Stage")

    db = Database()
    job_posting = JobPosting(db)
    jobs = job_posting.get_all_jobs()

    for job in jobs:
        st.subheader(job['title'])
        st.write(job['description'])
        st.write(f"**Date de création:** {job['created_at']}")
        
        # Link to the application page
        if st.button(f"Postuler pour {job['title']}", key=job['id']):
            st.session_state.job_id = job['id']  # Store job_id in session state
            st.experimental_rerun()  # Refresh to navigate to application page

def main():
    # Navigation management
    page = st.sidebar.selectbox(
        "Navigation",
        ["Connexion", "Inscription", "Dashboard Recruteur", 
         "Analyse Candidatures", "Offres de Stage", "Ajouter une Offre de Stage", "Profil Candidat"]
    )

    # Check if job_id is set in session state for application
    if 'job_id' in st.session_state:
        job_id = st.session_state.job_id
        apply_page(job_id)  # Call the apply page function
    else:
        # Page rendering based on selection
        if page == "Analyse Candidatures":
            view_applications()
        elif page == "Connexion":
            login_page()
        elif page == "Inscription":
            signup_page()
        elif page == "Dashboard Recruteur":
            recruiter_dashboard()
        elif page == "Profil Candidat":
            candidate_profile()
        elif page == "Offres de Stage":
            job_postings_page()  # Job postings page
        elif page == "Ajouter une Offre de Stage":
            add_job_posting_page()  # New page for adding job postings

if __name__ == "__main__":
    main()
