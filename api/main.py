from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os


# Add src directory to import path and import your modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import get_recommendations_for_user  # recommendation logic function
from src.db import get_user_recommendations, add_recommendation, clear_recommendations, get_movie # 👈 ADD get_movie IMPORT

app = FastAPI(title="Movie Recommendation System API", version="1.0")

# Allow all origins for frontend (Streamlit/React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserRequest(BaseModel):
    user_id: int
    top_n: int = 10

class Recommendation(BaseModel):
    movie_id: int
    score: Optional[float] = None

# 👇 ADD THIS NEW PYDANTIC MODEL FOR MOVIE DETAILS
class MovieDetails(BaseModel):
    id: int
    title: str
    year: int
    genres: str

@app.get("/")
def home():
    return {"message": "Movie Recommendation System API is Running"}

# 👇 ADD THIS ENTIRE ENDPOINT FUNCTION
@app.get("/movies/{movie_id}", response_model=MovieDetails)
def get_movie_details(movie_id: int):
    """
    Fetches details for a specific movie ID.
    """
    movie = get_movie(movie_id) # Use the function from db.py
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/recommendations", response_model=List[Recommendation])
def recommend(user_request: UserRequest):
    user_id = user_request.user_id
    top_n = user_request.top_n

    # 1) Fetch precomputed recommendations
    rec_response = get_user_recommendations(user_id, limit=top_n)

    # if get_user_recommendations returns list:
    data = rec_response if isinstance(rec_response, list) else rec_response.data

    if data:
        return [Recommendation(movie_id=rec['movie_id'], score=rec['score']) for rec in data]

    # 2) Compute on-demand
    recommendations = get_recommendations_for_user(user_id, top_n=top_n)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")

    # clear only this user's old recommendations
    clear_recommendations(user_id)

    for rec in recommendations:
        add_recommendation(user_id, rec['movie_id'], rec['score'])

    return [Recommendation(movie_id=rec['movie_id'], score=rec['score']) for rec in recommendations]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)