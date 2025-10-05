import streamlit as st
import requests

# Backend URLs
RECOMMENDATION_API = "http://localhost:8000/recommendations"  # POST user_id, top_n
MOVIE_DETAILS_API = "http://localhost:8000/movies"            # GET /movies/{id}

def fetch_recommendations(user_id: int, top_n: int = 10):
    payload = {"user_id": user_id, "top_n": top_n}
    try:
        resp = requests.post(RECOMMENDATION_API, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Failed to fetch recommendations: {e}")
        return []

def fetch_movie_details(movie_id: int):
    try:
        resp = requests.get(f"{MOVIE_DETAILS_API}/{movie_id}", timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return {"title": "Unknown", "genres": "Unknown", "year": "Unknown"}

def main():
    st.title("🎬 Movie Recommendation System")

    user_id = st.number_input("Enter your User ID", min_value=1, step=1)
    top_n = st.slider("Number of recommendations", 1, 20, 10)

    if st.button("Get Recommendations"):
        if user_id:
            recs = fetch_recommendations(user_id, top_n)
            if recs:
                st.subheader(f"Top {top_n} Recommendations for User {user_id}")
                for rec in recs:
                    movie_id = rec["movie_id"]
                    score = rec.get("score")

                    # Get movie info (requires backend support)
                    details = fetch_movie_details(movie_id)
                    title = details.get("title", "Unknown Title")
                    genres = details.get("genres", "Unknown Genres")
                    year = details.get("year", "Unknown Year")

                    st.markdown(f"**{title} ({year})**")
                    st.markdown(f"*Genres:* {genres}")
                    if score is not None:
                        st.markdown(f"*Recommendation Score:* {score:.2f}")
                    else:
                        st.markdown(f"*Recommendation Score:* N/A*")
                    st.markdown("---")  # separator
            else:
                st.warning("No recommendations found.")
        else:
            st.warning("Please enter a valid User ID.")

if __name__ == "__main__":
    main()
