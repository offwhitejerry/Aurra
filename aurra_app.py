import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# ========== CONFIG ==========
SPOTIFY_CLIENT_ID = "5b5562cb2f5c4bb2bb0c9d3ce594d1c7"
SPOTIFY_CLIENT_SECRET = "8d0d748dc2524ae29c2917fe7f341b3d"
SPOTIFY_REDIRECT_URI = "https://aw4bcndwzmcvhkv3uymwnh.streamlit.app"
SCOPE = "playlist-read-private"

# ========== INIT ==========
st.set_page_config(page_title="Aurra", layout="centered")
st.title("🎧 Aurra")
st.caption("Match your mood to the perfect Spotify playlists.")

# ========== SESSION CHECK ==========
if "spotify_token" not in st.session_state:
    st.session_state.spotify_token = None

auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,
    show_dialog=False
)

# Try to get token if redirected back
token_info = auth_manager.get_cached_token()
if token_info and not st.session_state.spotify_token:
    st.session_state.spotify_token = token_info["access_token"]
    st.experimental_rerun()

# ========== LOGIN FLOW ==========
if not st.session_state.spotify_token:
    st.warning("You need to log in to Spotify to use Aurra.")
    login_url = auth_manager.get_authorize_url()
    st.markdown(f"[🎵 Tap here to log in with Spotify]({login_url})", unsafe_allow_html=True)
    st.stop()

# ========== MAIN FUNCTIONALITY ==========
sp = spotipy.Spotify(auth=st.session_state.spotify_token)
vibe = st.text_input("Describe your current mood:", placeholder="e.g. mellow morning, dark club energy")

if vibe:
    with st.spinner("Searching playlists..."):
        try:
            results = sp.search(q=vibe, type='playlist', limit=5)
            playlists = results["playlists"]["items"]
            if not playlists:
                st.info("No matching playlists found.")
            else:
                st.success(f"Top playlists for: **{vibe}**")
                for i, p in enumerate(playlists):
                    name = p["name"]
                    url = p["external_urls"]["spotify"]
                    st.markdown(f"{i+1}. [{name}]({url})")
        except Exception as e:
            st.error("Something went wrong.")
            st.text(str(e))
