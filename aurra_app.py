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

# ========== INIT AUTH ==========
auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,
    show_dialog=False
)

# ========== HANDLE REDIRECT ==========
query_params = st.query_params
if "code" in query_params and "spotify_token" not in st.session_state:
    code = query_params["code"]
    token_info = auth_manager.get_access_token(code, check_cache=False)
    st.session_state.spotify_token = token_info["access_token"]
    st.query_params.clear()
    st.rerun()

# ========== LOGIN FLOW ==========
if "spotify_token" not in st.session_state:
    login_url = auth_manager.get_authorize_url()
    st.markdown(f"[🔐 Log in to Spotify]({login_url})", unsafe_allow_html=True)
    st.stop()

# ========== MAIN FUNCTION ==========
sp = spotipy.Spotify(auth=st.session_state.spotify_token)
vibe = st.text_input("Your current mood:", placeholder="e.g. chill sunrise, hype gym, heartbreak")

if vibe:
    with st.spinner("Matching your vibe..."):
        try:
            results = sp.search(q=vibe, type="playlist", limit=5)
            playlists = results.get("playlists", {}).get("items", [])
            if not playlists:
                st.warning("No playlists found.")
            else:
                st.success(f"Top playlists for: **{vibe}**")
                for i, p in enumerate(playlists):
                    name = p.get("name", "Unnamed Playlist")
                    url = p.get("external_urls", {}).get("spotify", "#")
                    st.markdown(f"{i+1}. [{name}]({url})")
        except Exception as e:
            st.error("Something went wrong while searching playlists.")
            st.code(str(e))
