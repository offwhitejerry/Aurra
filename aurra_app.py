import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ========== CONFIG ==========

SPOTIFY_CLIENT_ID = "5b5562cb2f5c4bb2bb0c9d3ce594d1c7"
SPOTIFY_CLIENT_SECRET = "8d0d748dc2524ae29c2917fe7f341b3d"
SPOTIFY_REDIRECT_URI = "https://aw4bcndwzmcvhkv3uymwnh.streamlit.app"

# ========== SPOTIFY SETUP ==========

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private"
    ))

# ========== AURRA UI ==========

st.set_page_config(page_title="Aurra", page_icon="🎧", layout="centered")
st.markdown("<style>h1, h2, h3 { color: #62AEBB; }</style>", unsafe_allow_html=True)

st.title("🎧 Aurra")
st.subheader("Find the perfect playlist for your mood.")

vibe_input = st.text_input("What are you feeling right now?", placeholder="e.g. confident sunrise, soft nostalgia")

if st.button("✨ Match My Mood"):
    if vibe_input.strip() == "":
        st.warning("Type your vibe before hitting the button.")
    else:
        st.write(f"🔍 Searching Spotify for: **{vibe_input}**")
        try:
            sp = get_spotify_client()
            results = sp.search(q=vibe_input, type='playlist', limit=6)
            playlists = results['playlists']['items']

            if not playlists:
                st.error("No matching playlists found.")
            else:
                for playlist in playlists:
                    name = playlist.get("name", "[Untitled Playlist]")
                    url = playlist["external_urls"]["spotify"]
                    image = playlist['images'][0]['url'] if playlist['images'] else None

                    if image:
                        st.image(image, width=300)
                    st.markdown(f"[**{name}**]({url})", unsafe_allow_html=True)
                    st.markdown("---")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
