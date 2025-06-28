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

if st.button("🎵 Match My Mood") and vibe:
    try:
        # ========== SPOTIFY AUTH + SEARCH ==========
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="playlist-read-private",
            show_dialog=True
        ))

        results = sp.search(q=vibe, type='playlist', limit=5)
        playlists = results['playlists']['items']

        if not playlists:
            st.warning("No playlists found for that vibe.")
        else:
            st.success(f"Top playlists for: **{vibe}**")
            for i, playlist in enumerate(playlists):
                st.markdown(f"{i+1}. [{playlist['name']}]({playlist['external_urls']['spotify']})")

    except Exception as e:
        st.error("Something went wrong. Try refreshing or checking your Spotify login.")
        st.text(f"Error: {e}")
