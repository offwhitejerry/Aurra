import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ========== CONFIG ==========
SPOTIFY_CLIENT_ID = "5b5562cb2f5c4bb2bb0c9d3ce594d1c7"
SPOTIFY_CLIENT_SECRET = "8d0d748dc2524ae29c2917fe7f341b3d"
SPOTIFY_REDIRECT_URI = "https://aw4bcndwzmcvhkv3uymwnh.streamlit.app"
SCOPE = "playlist-read-private"

# ========== UI SETUP ==========
st.set_page_config(page_title="Aurra", layout="centered")
st.title("🎧 Aurra")
st.caption("Describe your vibe. Get the perfect Spotify playlists.")

# ========== SPOTIFY AUTH ==========
auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,
    show_dialog=False
)

# Try to get token from cache after redirect
token_info = auth_manager.get_cached_token()
if token_info and "spotify_token" not in st.session_state:
    st.session_state.spotify_token = token_info["access_token"]
    st.experimental_rerun()

# If not logged in, prompt login
if "spotify_token" not in st.session_state:
    st.warning("Login with Spotify to use Aurra.")
    login_url = au_
