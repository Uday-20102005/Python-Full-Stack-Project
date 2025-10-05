import numpy as np
import pandas as pd
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity

from src.db import get_user_ratings, get_movie_ratings, get_all_movies

def build_user_item_matrix() -> pd.DataFrame:
    """Fetch ratings from DB and build user-item rating matrix."""
    all_movies = get_all_movies()
    movie_ids = [m["id"] for m in all_movies]

    # Gather all ratings
    ratings_rows = []
    for movie_id in movie_ids:
        ratings_for_movie = get_movie_ratings(movie_id)
        ratings_rows.extend(ratings_for_movie)

    df = pd.DataFrame(ratings_rows)
    if df.empty:
        return pd.DataFrame()

    # Pivot into user-item matrix
    user_item_matrix = df.pivot(index="user_id", columns="movie_id", values="rating").fillna(0)
    return user_item_matrix


def get_recommendations_for_user(user_id: int, top_n: int = 10) -> List[Dict]:
    """Generate top-N movie recommendations for a user using item-based CF."""
    user_item_matrix = build_user_item_matrix()
    if user_item_matrix.empty:
        return []

    if user_id not in user_item_matrix.index:
        # Cold start fallback → recommend top popular movies
        counts = (user_item_matrix > 0).sum().sort_values(ascending=False)
        top_movies = counts.head(top_n).index.tolist()
        return [{"movie_id": int(mid), "score": None} for mid in top_movies]

    # Compute item-item similarity (vectorized)
    sim_matrix = cosine_similarity(user_item_matrix.T)
    similarity_df = pd.DataFrame(sim_matrix, index=user_item_matrix.columns, columns=user_item_matrix.columns)

    user_ratings = user_item_matrix.loc[user_id]
    scores = {}

    for movie in similarity_df.columns:
        if user_ratings[movie] == 0:  # not yet rated
            sim_scores = similarity_df[movie]
            weighted_sum = (sim_scores * user_ratings).sum()
            sim_sum = sim_scores[user_ratings > 0].sum()
            scores[movie] = float(weighted_sum / sim_sum) if sim_sum != 0 else 0.0

    # Sort by predicted rating
    recommended_movies = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [{"movie_id": int(mid), "score": float(score)} for mid, score in recommended_movies]
