from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import sys
import os

# Add src directory to import path and import your modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import get_recommendations_for_user  # recommendation logic function
from src.db import get_user_recommendations, add_recommendation, clear_recommendations  # db functions

app = FastAPI(title="Movie Recommendation System API", version="1.0")

# Allow all origins for frontend (Streamlit/React)
app.add_middleware(
    CORSMiddleware,
    allow_origin=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request validation
class UserRequest(BaseModel):
    user_id: int
    top_n: int = 10

class Recommendation(BaseModel):
    movie_id: int
    score: float

# Health check
@app.get("/")
def home():
    return {"message": "Movie Recommendation System API is Running"}

# Endpoint to get recommendations for a user using precomputed or on-demand logic
@app.post("/recommendations", response_model=List[Recommendation])
def recommend(user_request: UserRequest):
    user_id = user_request.user_id
    top_n = user_request.top_n

    # Option 1: Fetch from precomputed recommendations table
    rec_response = get_user_recommendations(user_id, limit=top_n)
    data = rec_response.data
    if data:
        # Return stored recommendations if available
        return [Recommendation(movie_id=rec['movie_id'], score=rec['score']) for rec in data]

    # Option 2: If no precomputed, compute on-demand
    recommendations = get_recommendations_for_user(user_id, top_n=top_n)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")

    # Clear old recommendations for user, then insert new ones
    clear_recommendations()
    for rec in recommendations:
        add_recommendation(user_id, rec['movie_id'], rec['score'])

    return [Recommendation(movie_id=rec['movie_id'], score=rec['score']) for rec in recommendations]

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
