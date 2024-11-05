import streamlit as st
import pandas as pd
import plotly.express as px
from app.models import Database, Application

def view_applications():
    st.title("Analyse des candidatures")
    
    db = Database()
    application_manager = Application(db)
    
    # Sélection du poste
    jobs = JobPosting(db).get_all_jobs()
    selected_job = st.selectbox(
        "Sélectionner un poste",
        options=jobs,
        format_func=lambda x: x['title']
    )
    
    if selected_job:
        applications = application_manager.get_applications_for_job(selected_job['id'])
        
        # Création du DataFrame pour l'affichage
        df = pd.DataFrame(applications)
        
        # Graphique de distribution des scores
        fig = px.histogram(
            df, 
            x='score',
            title="Distribution des scores des candidats",
            labels={'score': 'Score de correspondance', 'count': 'Nombre de candidats'},
            nbins=20
        )
        st.plotly_chart(fig)
        
        # Tableau des candidatures
        st.subheader("Candidatures reçues")
        
        # Formater les données pour l'affichage
        display_df = df[['email', 'score']].copy()
        display_df['Décision suggérée'] = df['score'].apply(
            lambda x: '✅ Accepté' if x >= 0.7 
            else ('⚠️ À considérer' if x >= 0.5 else '❌ Non retenu')
        )
        
        # Afficher le tableau avec mise en forme conditionnelle
        st.dataframe(
            display_df.style.apply(lambda x: [
                'background-color: #c6efce' if val >= 0.7
                else ('background-color: #ffeb9c' if val >= 0.5
                      else 'background-color: #ffc7ce')
                for val in x['score']
            ]),
            hide_index=True
        )
        
        # Détails des candidatures
        if st.checkbox("Voir les détails des évaluations"):
            for app in applications:
                with st.expander(f"Candidature de {app['email']}"):
                    eval_details = pickle.loads(app['evaluation_details'])
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Scores détaillés:**")
                        st.write(f"- Similarité globale: {eval_details['similarity']:.2%}")
                        st.write(f"- Match des compétences: {eval_details['skills_match']:.2%}")
                        st.write(f"- Score d'expérience: {eval_details['experience_score']:.2%}")
                    
                    with col2:
                        st.write("**Compétences:**")
                        st.write("Compétences correspondantes:", 
                                ", ".join(eval_details['matched_skills']))
                        st.write("Compétences manquantes:", 
                                ", ".join(eval_details['missing_skills']))