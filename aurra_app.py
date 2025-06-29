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

# ========== AUTH SETUP ==========
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
    try:
        code = query_params["code"]
        token_info = auth_manager.get_access_token(code, check_cache=False)
        access_token = token_info.get("access_token") if token_info else None
        if access_token:
            st.session_state.spotify_token = access_token
            st.query_params.clear()
            st.rerun()
        else:
            st.error("Failed to retrieve Spotify token.")
            st.stop()
    except Exception as e:
        st.error("Spotify login failed.")
        st.code(str(e))
        st.stop()

# ========== LOGIN ==========
if "spotify_token" not in st.session_state:
    login_url = auth_manager.get_authorize_url()
    st.markdown(f"[🔐 Log in to Spotify]({login_url})", unsafe_allow_html=True)
    st.stop()

# ========== MAIN FUNCTION ==========
sp = spotipy.Spotify(auth=st.session_state.spotify_token)
vibe = st.text_input("Your current mood:", placeholder="e.g. mellow morning, rage gym, heartbreak")

if vibe:
    with st.spinner("Finding playlists..."):
        try:
            results = sp.search(q=vibe, type="playlist", limit=5)

            playlists = []
            if results and isinstance(results, dict):
                if "playlists" in results and isinstance(results["playlists"], dict):
                    items = results["playlists"].get("items")
                    if items and isinstance(items, list):
                        playlists = items

            if not playlists:
                st.warning("No playlists found. Try a different mood.")
            else:
                st.success(f"Top playlists for: **{vibe}**")
                for i, playlist in enumerate(playlists):
                    name = playlist.get("name", "Untitled")
                    url = playlist.get("external_urls", {}).get("spotify", "#")
                    st.markdown(f"{i+1}. [{name}]({url})")

        except Exception as e:
            st.error("Something went wrong while searching.")
            st.code(str(e))
