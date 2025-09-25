import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # use service key for inserts/updates

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or KEY missing in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------- MOVIES -----------------
def add_movie(movie_id: int, title: str, year: int, genres: str):
    """Insert a new movie into movies table"""
    data = {
        "id": movie_id,
        "title": title,
        "year": year,
        "genres": genres
    }
    return supabase.table("movies").insert(data).execute()

def get_movie(movie_id: int):
    """Fetch a movie by ID"""
    return supabase.table("movies").select("*").eq("id", movie_id).single().execute()

def get_all_movies(limit: int = 50):
    """Fetch all movies (limited)"""
    return supabase.table("movies").select("*").limit(limit).execute()


# ----------------- RATINGS -----------------
def add_rating(user_id: int, movie_id: int, rating: float):
    """Insert a user rating"""
    data = {
        "user_id": user_id,
        "movie_id": movie_id,
        "rating": rating
    }
    return supabase.table("ratings").insert(data).execute()

def get_user_ratings(user_id: int):
    """Fetch all ratings for a user"""
    return supabase.table("ratings").select("*").eq("user_id", user_id).execute()

def get_movie_ratings(movie_id: int):
    """Fetch all ratings for a movie"""
    return supabase.table("ratings").select("*").eq("movie_id", movie_id).execute()


# ----------------- RECOMMENDATIONS -----------------
def add_recommendation(user_id: int, movie_id: int, score: float, method: str = "itemcf"):
    """Insert a recommendation result"""
    data = {
        "user_id": user_id,
        "movie_id": movie_id,
        "score": score,
        "method": method
    }
    return supabase.table("recommendations").insert(data).execute()

def get_user_recommendations(user_id: int, method: str = "itemcf", limit: int = 10):
    """Fetch recommendations for a user"""
    return (
        supabase.table("recommendations")
        .select("movie_id,score")
        .eq("user_id", user_id)
        .eq("method", method)
        .order("score", desc=True)
        .limit(limit)
        .execute()
    )

def clear_recommendations():
    """Delete all old recommendations"""
    return supabase.table("recommendations").delete().neq("user_id", -1).execute()
