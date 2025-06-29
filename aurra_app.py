import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# ========== CONFIG ==========
SPOTIFY_CLIENT_ID = "5b5562cb2f5c4bb2bb0c9d3ce594d1c7"
SPOTIFY_CLIENT_SECRET = "8d0d748dc2524ae29c2917fe7f341b3d"
SPOTIFY_REDIRECT_URI = "https://aw4bcndwzmcvhkv3uymwnh.streamlit.app"
SCOPE = "playlist-read-private"

# ========== UI ==========
st.set_page_config(page_title="Aurra", layout="centered")
st.title("🎧 Aurra")
st.caption("Describe your mood. Get matching Spotify playlists.")

# ========== AUTH ==========
auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,
    open_browser=False,
    show_dialog=True
)

# Handle login manually
if "token_info" not in st.session_state:
    try:
        code = st.query_params.get("code")
        if code:
            token_info = auth_manager.get_access_token(code, check_cache=False)
            st.session_state.token_info = token_info
            st.query_params.clear()
            st.rerun()
        else:
            login_url = auth_manager.get_authorize_url()
            st.markdown(f"[🔐 Log in with Spotify]({login_url})", unsafe_allow_html=True)
            st.stop()
    except Exception as e:
        st.error("Spotify login failed.")
        st.code(str(e))
        st.stop()

# ========== MAIN ==========
sp = spotipy.Spotify(auth=st.session_state.token_info['access_token'])
vibe = st.text_input("Your current mood:", placeholder="e.g. moody night drive")

if vibe:
    with st.spinner("Finding playlists..."):
        try:
            results = sp.search(q=vibe, type="playlist", limit=5)

            raw_items = results.get("playlists", {}).get("items", [])
            playlists = [p for p in raw_items if p is not None]

            if not playlists:
                st.warning("No playlists found. Try something else.")
            else:
                st.success(f"Top playlists for: **{vibe}**")
                for i, playlist in enumerate(playlists):
                    name = playlist.get("name", "Untitled")
                    url = playlist.get("external_urls", {}).get("spotify", "#")
                    st.markdown(f"{i+1}. [{name}]({url})")

        except Exception as e:
            st.error("Search failed.")
            st.code(str(e))
