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
    login_url = auth_manager.get_authorize_url()
    st.markdown(f"[🎵 Tap here to log in with Spotify]({login_url})", unsafe_allow_html=True)
    st.stop()

# ========== MAIN FUNCTIONALITY ==========
sp = spotipy.Spotify(auth=st.session_state.spotify_token)
vibe = st.text_input("Your current mood:", placeholder="e.g. chill night drive, gym pump")

if vibe:
    with st.spinner("Matching your vibe..."):
        try:
            results = sp.search(q=vibe, type='playlist', limit=5)
            playlists = results['playlists']['items']
            if not playlists:
                st.warning("No playlists found.")
            else:
                st.success(f"Playlists for: **{vibe}**")
                for i, p in enumerate(playlists):
                    name = p["name"]
                    url = p["external_urls"]["spotify"]
                    st.markdown(f"{i+1}. [{name}]({url})")
        except Exception as e:
            st.error("Something went wrong.")
            st.code(str(e))
