RecruTech/
│
├── __pycache__/               
│
├── app/                       
│   ├── __pycache__/           
│   ├── ml/                    
│   │   └── model.py           
│   ├── pages/                 
│   │   ├── __pycache__/       
│   │   ├── candidate/         
│   │   │   ├── __init__.py    
│   │   │   └── profile.py      
│   │   └── recruiter/         
│   │   │   ├── __init__.py    
│   │   │   ├── applications.py  
│   │   │   └── dashboard.py 
│   │   │   
│   │   ├── __init__.py           
│   │	 ├── add_job_posting.py     
│   │	 ├── apply.py               
│   │	 ├── login.py               
│   │	 └── signup.py              
│   ├── __init__.py            
│   └── models.py
├── newenv/
│              
├── config.py              
├── db_setup.py            
├── recrutech.db           
├── requirements.txt       
└── run.py           


1- python -m venv newenv             
2- newenv\Scripts\activate  
3- pip install pandas numpy spacy h5py
4- pip install python-dotenv                                
5- pip install -r requirements.txt  
6- python -m spacy download fr_core_news_sm
7- python db_setup.py
8- streamlit run run.py 

