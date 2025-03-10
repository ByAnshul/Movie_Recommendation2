import streamlit as st
import requests
import random
from login_module import login_ui
from database import initialize_db

initialize_db()

# Set page configuration
st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# API Key for TMDB
API_KEY = "82efcebe55225281776f08ab5ee37fe2"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# Display Login or Skip
if not st.session_state.logged_in:
    login_ui()
else:
    
    # Movie Recommendation System starts here
    st.markdown(f"<h1 style='text-align: center; color: #FF6347;'>Welcome, {st.session_state.username}!</h1>", unsafe_allow_html=True)

    # CSS for custom styling
    st.markdown("""
        <style>
        .title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            color: #FF6347;
        }
        .stButton > button {
            background-color: red;
            color: white;
            border: none;
            padding: 8px 16px;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
        }
        .movie-poster-container img:hover {
            transform: scale(1.05);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .column-content {
            text-align: center;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display title
    st.markdown('<div class="title">Movie Recommendation System</div>', unsafe_allow_html=True)

    # Function to fetch a random movie
    def fetch_random_movie():
        random_id = random.randint(1, 100000)
        random_movie_url = f"https://api.themoviedb.org/3/movie/{random_id}?api_key={API_KEY}&append_to_response=videos"
        response = requests.get(random_movie_url)
        if response.status_code == 200:
            return response.json()
        return None

    # Initialize session states
    if 'selected_movie' not in st.session_state:
        st.session_state['selected_movie'] = None
    if 'show_recommendations' not in st.session_state:
        st.session_state['show_recommendations'] = False

    # Combined input box for movie search and selection
    query = st.text_input("Enter or Select a Movie:", value="")
    if query:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
        search_response = requests.get(search_url)

        if search_response.status_code == 200:
            movie_data = search_response.json().get('results', [])
        else:
            st.error("Error fetching movie data.")
            movie_data = []

        # Dropdown to select a movie from search results
        if movie_data:
            selected_title = st.selectbox("Select a movie", movie_data, format_func=lambda x: x['title'])
            st.session_state['selected_movie'] = selected_title

        # Random movie button
        if st.button("Random Movie"):
            random_movie = fetch_random_movie()
            if random_movie:
                st.session_state['selected_movie'] = random_movie
            else:
                st.error("Error fetching a random movie.")

    # Display selected movie details
    if st.session_state['selected_movie']:
        selected_movie = st.session_state['selected_movie']
        movie_id = selected_movie['id']
        movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=videos"
        movie_detail_response = requests.get(movie_detail_url)

        if movie_detail_response.status_code == 200:
            movie_detail = movie_detail_response.json()

            # Display movie details
            st.subheader(movie_detail.get('title', 'Movie Title'))
            st.subheader(movie_detail.get('tagline', 'Movie Tagline'))

            poster_url = f"https://image.tmdb.org/t/p/w500{movie_detail.get('poster_path', '')}"
            st.markdown(f'<div class="movie-poster-container"><img src="{poster_url}" width="300" /></div>', unsafe_allow_html=True)

            st.write(f"**Overview:** {movie_detail.get('overview', 'Overview not available.')}")
            st.write(f"**Genres:** {', '.join([genre['name'] for genre in movie_detail.get('genres', [])])}")
            st.write(f"**Release Date:** {movie_detail.get('release_date', 'N/A')}")
            st.write(f"**Runtime:** {movie_detail.get('runtime', 'N/A')} minutes")
            st.write(f"**Vote Average:** {movie_detail.get('vote_average', 'N/A')} ({movie_detail.get('vote_count', 0)} votes)")

            # Videos section
            videos = movie_detail.get('videos', {}).get('results', [])
            if videos:
                st.write("**Videos/Trailers:**")
                for video in videos:
                    video_link = f"https://www.youtube.com/watch?v={video['key']}"
                    st.markdown(f"- [{video['name']}]({video_link})")
            else:
                st.write("No videos available for this movie.")

        # Recommendations button
        if st.button("Show Recommendations"):
            st.session_state['show_recommendations'] = True

        # Display recommendations
        if st.session_state['show_recommendations']:
            recommendations_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}"
            recommendations_response = requests.get(recommendations_url)

            if recommendations_response.status_code == 200:
                recommendations_data = recommendations_response.json().get('results', [])
            else:
                st.error("Error fetching recommendations.")
                recommendations_data = []

            if recommendations_data:
                st.write("### Movie Recommendations:")
                cols = st.columns(3)
                for idx, movie in enumerate(recommendations_data):
                    with cols[idx % 3]:
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
                        st.markdown(f'<div class="movie-poster-container"><img src="{poster_url}" width="150" /></div>', unsafe_allow_html=True)
                        st.write(f"**{movie.get('title', 'N/A')}**")
                        st.write(f"Release Date: {movie.get('release_date', 'N/A')}")
                        st.write(f"Rating: {movie.get('vote_average', 'N/A')}")
                        st.write(f"Overview: {movie.get('overview', 'N/A')[:100]}...")
            else:
                st.write("No recommendations available.")
    else:
        st.write("Please enter a movie name to search.")
