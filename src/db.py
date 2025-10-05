import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or KEY missing in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------- MOVIES -----------------
def add_movie(movie_id: int, title: str, year: int, genres: str):
    """Insert a new movie into movies table"""
    data = {"id": movie_id, "title": title, "year": year, "genres": genres}
    resp = supabase.table("movies").insert(data).execute()
    return _extract_data(resp)

def get_movie(movie_id: int):
    """Fetch a single movie as a dict"""
    resp = supabase.table("movies").select("*").eq("id", movie_id).single().execute()
    data = _extract_data(resp)
    return data[0] if isinstance(data, list) and data else data

def get_all_movies(limit: int = 50):
    """Fetch all movies (limited)"""
    resp = supabase.table("movies").select("*").limit(limit).execute()
    return _extract_data(resp)

# ----------------- RATINGS -----------------
def add_rating(user_id: int, movie_id: int, rating: float):
    """Insert a user rating"""
    data = {"user_id": user_id, "movie_id": movie_id, "rating": rating}
    resp = supabase.table("ratings").insert(data).execute()
    return _extract_data(resp)

def get_user_ratings(user_id: int):
    """Fetch all ratings for a user"""
    resp = supabase.table("ratings").select("*").eq("user_id", user_id).execute()
    return _extract_data(resp)

def get_movie_ratings(movie_id: int):
    """Fetch all ratings for a movie"""
    resp = supabase.table("ratings").select("*").eq("movie_id", movie_id).execute()
    return _extract_data(resp)

# ----------------- RECOMMENDATIONS -----------------
def add_recommendation(user_id: int, movie_id: int, score: float, method: str = "itemcf"):
    """Insert a recommendation result"""
    data = {"user_id": user_id, "movie_id": movie_id, "score": score, "method": method}
    resp = supabase.table("recommendations").insert(data).execute()
    return _extract_data(resp)

def get_user_recommendations(user_id: int, method: str = "itemcf", limit: int = 10):
    """Fetch recommendations for a user"""
    resp = (
        supabase.table("recommendations")
        .select("movie_id,score")
        .eq("user_id", user_id)
        .eq("method", method)
        .order("score", desc=True)
        .limit(limit)
        .execute()
    )
    return _extract_data(resp)

def clear_recommendations(user_id: int):
    """Delete recommendations for a specific user"""
    resp = supabase.table("recommendations").delete().eq("user_id", user_id).execute()
    return _extract_data(resp)

# ----------------- HELPER -----------------
def _extract_data(resp):
    """
    Extracts data safely from Supabase APIResponse object.
    Works with both old and new supabase-py versions.
    """
    # For new supabase client (v2.x)
    if isinstance(resp, dict):
        return resp.get("data", [])
    # For APIResponse-like object
    if hasattr(resp, "model_dump"):
        data = resp.model_dump()
        if isinstance(data, dict):
            return data.get("data", [])
    # For old-style response (v1.x)
    return getattr(resp, "data", [])
