import numpy as np
import pandas as pd
from typing import List, Dict
from src.db import get_user_ratings, get_movie_ratings, get_all_movies

def build_user_item_matrix():
    """Fetch ratings from DB and build user-item rating matrix."""
    all_movies = get_all_movies().data
    movie_ids = [m["id"] for m in all_movies]
    
    # Gather all ratings, aggregated by user
    ratings_rows = []
    # This simulates fetching all ratings; in a real system you'd fetch all in one query or paginate queries
    for movie_id in movie_ids:
        ratings_for_movie = get_movie_ratings(movie_id).data
        for r in ratings_for_movie:
            ratings_rows.append(r)

    # Convert to DataFrame
    df = pd.DataFrame(ratings_rows)
    
    if df.empty:
        return pd.DataFrame()
    
    # Create user-item matrix with missing ratings as 0
    user_item_matrix = df.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
    return user_item_matrix

def cosine_similarity(vec1: np.array, vec2: np.array) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def item_similarity_matrix(user_item_matrix: pd.DataFrame) -> pd.DataFrame:
    """Compute similarity matrix for items (movies)."""
    movie_ids = user_item_matrix.columns
    similarity_matrix = pd.DataFrame(index=movie_ids, columns=movie_ids)
    
    for i in movie_ids:
        for j in movie_ids:
            if i == j:
                similarity_matrix.loc[i, j] = 1.0
            else:
                sim = cosine_similarity(user_item_matrix[i].values, user_item_matrix[j].values)
                similarity_matrix.loc[i, j] = sim
    return similarity_matrix.astype(float)

def get_recommendations_for_user(user_id: int, top_n: int = 10) -> List[Dict]:
    """Generate top-N movie recommendations for a user."""
    user_item_matrix = build_user_item_matrix()
    if user_item_matrix.empty or user_id not in user_item_matrix.index:
        return []
    
    similarity_matrix = item_similarity_matrix(user_item_matrix)
    
    user_ratings = user_item_matrix.loc[user_id]
    
    scores = {}
    for movie in similarity_matrix.columns:
        if user_ratings[movie] == 0:  # Only recommend movies not rated by the user
            # Weighted sum of similarities * user ratings for other movies
            sim_scores = similarity_matrix[movie]
            weighted_sum = (sim_scores * user_ratings).sum()
            sim_sum = sim_scores[user_ratings > 0].sum()
            if sim_sum != 0:
                scores[movie] = weighted_sum / sim_sum
            else:
                scores[movie] = 0.0
    
    # Sort movies by predicted rating descending
    recommended_movies = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [{"movie_id": movie, "score": score} for movie, score in recommended_movies]
