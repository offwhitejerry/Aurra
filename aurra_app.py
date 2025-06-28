import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ========== CONFIG ==========

SPOTIFY_CLIENT_ID = "5b5562cb2f5c4bb2bb0c9d3ce594d1c7"
SPOTIFY_CLIENT_SECRET = "8d0d748dc2524ae29c2917fe7f341b3d"
SPOTIFY_REDIRECT_URI = "https://aw4bcndwzmcvhkv3uymwnh.streamlit.app"

# ========== UI ==========

st.set_page_config(page_title="Aurra", layout="centered")
st.title("🎧 Aurra")
st.subheader("Match your mood to the perfect playlists.")

vibe = st.text_input("Describe your current mood:", placeholder="e.g. road trip, sad rainy night")

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
        st.caption("This opens Spotify login. Works best on mobile too.")

        # ✅ Only attempt to search after token is available
        token_info = auth_manager.get_cached_token()
        if token_info:
            sp = spotipy.Spotify(auth=token_info['access_token'])
            results = sp.search(q=vibe, type='playlist', limit=5)
            playlists = results['playlists']['items']

            if not playlists:
                st.warning("No playlists found for that vibe.")
            else:
                st.success(f"Top playlists for: **{vibe}**")
                for i, playlist in enumerate(playlists):
                    st.markdown(f"{i+1}. [{playlist['name']}]({playlist['external_urls']['spotify']})")
        else:
            st.info("Login with Spotify first using the button above.")

    except Exception as e:
        st.error("Something went wrong.")
        st.code(f"{e}")
