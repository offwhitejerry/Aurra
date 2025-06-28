import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ========== CONFIG ==========

SPOTIFY_CLIENT_ID = "5b5562cb2f5c4bb2bb0c9d3ce594d1c7"
SPOTIFY_CLIENT_SECRET = "8d0d748dc2524ae29c2917fe7f341b3d"
SPOTIFY_REDIRECT_URI = "https://aw4bcndwzmcvhkv3uymwnh.streamlit.app"

# ========== UI SETUP ==========

st.set_page_config(page_title="Aurra", layout="centered")
st.title("🎧 Aurra")
st.subheader("Match your mood to the perfect playlists.")

vibe = st.text_input("Describe your current mood:", placeholder="e.g. chill sunset, gym hype, breakup")

# ========== SPOTIFY AUTH HANDLING ==========

def get_auth_manager():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private",
        show_dialog=True
    )

if "token_info" not in st.session_state:
    # Try to get token from cache
    auth_manager = get_auth_manager()
    token_info = auth_manager.get_cached_token()

    if token_info:
        st.session_state.token_info = token_info
        st.rerun()
    elif vibe:
        # Not logged in yet
        auth_url = auth_manager.get_authorize_url()
        st.markdown(f"[🎵 Tap here to match your mood]({auth_url})", unsafe_allow_html=True)
        st.caption("Login to Spotify to continue.")
else:
    try:
        sp = spotipy.Spotify(auth=st.session_state.token_info['access_token'])

        if vibe:
            results = sp.search(q=vibe, type='playlist', limit=5)
            playlists = results['playlists']['items']

            if not playlists:
                st.warning("No playlists found for that vibe.")
            else:
                st.success(f"Top playlists for: **{vibe}**")
                for i, playlist in enumerate(playlists):
                    st.markdown(f"{i+1}. [{playlist['name']}]({playlist['external_urls']['spotify']})")

    except Exception as e:
        st.error("Something went wrong while accessing Spotify.")
        st.code(str(e))
