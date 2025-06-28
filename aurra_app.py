import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_page_config(page_title="Aurra Debug", layout="centered")
st.title("🔍 Aurra Debug Mode")

SPOTIFY_CLIENT_ID = "5b5562cb2f5c4bb2bb0c9d3ce594d1c7"
SPOTIFY_CLIENT_SECRET = "8d0d748dc2524ae29c2917fe7f341b3d"
SPOTIFY_REDIRECT_URI = "https://aw4bcndwzmcvhkv3uymwnh.streamlit.app"
SCOPE = "playlist-read-private"

# Show session state
st.subheader("Session State:")
st.json(dict(st.session_state))

# Init auth manager
auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True
)

# Try to load cached token
token_info = auth_manager.get_cached_token()
st.subheader("Token Info:")
st.json(token_info)

# Store in session
if token_info and "spotify_token" not in st.session_state:
    st.session_state.spotify_token = token_info["access_token"]
    st.experimental_rerun()

# Auth button
if "spotify_token" not in st.session_state:
    st.warning("You need to log in with Spotify.")
    login_url = auth_manager.get_authorize_url()
    st.markdown(f"[🔑 Login with Spotify]({login_url})", unsafe_allow_html=True)
    st.stop()

# If logged in
st.success("✅ You are logged in
