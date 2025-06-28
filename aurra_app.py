import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ========== CONFIG ==========

SPOTIFY_CLIENT_ID = "5b5562cb2f5c4bb2bb0c9d3ce594d1c7"
SPOTIFY_CLIENT_SECRET = "8d0d748dc2524ae29c2917fe7f341b3d"
SPOTIFY_REDIRECT_URI = "https://aw4bcndwzmcvhkv3uymwnh.streamlit.app"

# ========== STREAMLIT UI ==========

st.set_page_config(page_title="Aurra", layout="centered")
st.title("🎧 Aurra")
st.subheader("Match your mood to the perfect playlists.")

vibe = st.text_input("Describe your current mood:", placeholder="e.g. chill sunset, gym hype, breakup")

if vibe:
    try:
        auth_manager = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="playlist-read-private",
            show_dialog=True
        )

        auth_url = auth_manager.get_authorize_url()
        st.markdown(f"[🎵 Tap here to match your mood]({auth_url})", unsafe_allow_html=True)
        st.caption("This opens Spotify login — works better on mobile.")

        # OPTIONAL: once authorized, continue from callback handling...
        token_info = auth_manager.get_cached_token()
