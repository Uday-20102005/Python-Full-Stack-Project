import streamlit as st
import requests

# Your backend URLs (update URLs if deployed elsewhere)
RECOMMENDATION_API = "http://localhost:8000/recommendations"  # POST user_id, top_n
MOVIE_DETAILS_API = "http://localhost:8000/movies"             # GET /movies/{id} assumed

def fetch_recommendations(user_id: int, top_n: int = 10):
    payload = {"user_id": user_id, "top_n": top_n}
    resp = requests.post(RECOMMENDATION_API, json=payload)
    if resp.status_code == 200:
        return resp.json()
    else:
        st.error(f"Failed to fetch recommendations: {resp.text}")
        return []

def fetch_movie_details(movie_id: int):
    resp = requests.get(f"{MOVIE_DETAILS_API}/{movie_id}")
    if resp.status_code == 200:
        return resp.json()
    else:
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
                    score = rec["score"]

                    # Get movie info to show friendly details
                    details = fetch_movie_details(movie_id)
                    title = details.get("title", "Unknown Title")
                    genres = details.get("genres", "Unknown Genres")
                    year = details.get("year", "Unknown Year")

                    st.markdown(f"**{title} ({year})**")
                    st.markdown(f"*Genres:* {genres}")
                    st.markdown(f"*Recommendation Score:* {score:.2f}")
                    st.markdown("---")  # separator
            else:
                st.warning("No recommendations found.")
        else:
            st.warning("Please enter a valid User ID.")

if __name__ == "__main__":
    main()
