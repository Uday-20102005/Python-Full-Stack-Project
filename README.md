# 🎬 Movie Recommendation System (Python + Supabase + FastAPI + Streamlit)

## Overview
A personalized movie recommendation system using collaborative filtering.  
Built with **Python, Supabase, FastAPI, and Streamlit**.

## Features
- Stores movies, users, and ratings in Supabase (Postgres).
- Trains an item-based collaborative filtering model.
- Precomputes recommendations and stores them in Supabase.
- FastAPI backend to serve recommendations.
- Streamlit frontend for interactive movie discovery.

## Project Structure


 MOVIE-RECOMMENDATION-SYSTEM/
│
├── api/                 
│   └── main.py          # FastAPI backend (API layer)
│
├── frontend/            
│   └── app.py           # Streamlit frontend (UI layer)
│
├── src/                 
│   ├── db.py            # Supabase database connection
│   └── logic.py         # Recommendation logic (ML + helper functions)
│
├── .env                 # Supabase keys (ignored in git)
├── requirements.txt     
└── README.md            

## Quick Start

### Prerequisites

- python 3.8 or higher
- A Supabase account
- Git(push,cloning)

### 1.clone or Download the project 
# option 1: clone with Git
git clone <repository-url>

# option 2:Download and extract the ZIP file

###  2.Insatll Dependencies 
 
# Install all required python packages 
pip install -r requirements.txt

### 3.set up supabase Database

1.create a Supabase project:

2.create the Tasks Table:

-GO to the SQL Editor in your Supabase dashboard
-run this SQL command:

```sql


3. **Get your credentials:

### 4. configure Environment variables

!.create a .env file in the project root 
2.add supabase credentials to .env :

### 5. Run the Application

### Stremlit Frontend
streamlit run frontend/app.py

The app will openin your browser at `http://localhost:8501`

## FastAPI Backend

cd api
python main.py

The API will be available at `http://loacalhoat:8000`

## How to use

## Techinical Details

##Technologies used

-**FRontend**:stremlit(python web framework)
--**Backend**:FastAPI(python REst API framework)
-**Datbase**:supabase(postgreSQL-based backend-as-a-service)
-**Language**:python 3.8+

### key components

1. **`src/db.py`**:Database operations - Handles all CRUD Operations with SupaBase
2.**`src/logic.py`**:Business logic -Task validation and processing

## Troubleshooting

## common Issues

1. **"Module not found" errors**
 -make sure you've installed all dependencies:`pip install -r requirements.txt

 ## Future Enhancements 

 Ideas for extending this project :

 -*user Authentication**:
 -**Task Categories**:
 -**Notifications**:
 -**FIle Attachments**:
 -**Collaboration**:
 -**Mobile App**:
 -**Date Export**:
 -**Task Templates**:

 ## support

 if you encounter any issue or have questions:
