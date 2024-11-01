#!/user/bin/python3

#Share Spotify song link
#---
#Script to search Spotify for a song and obtain the songs shareable URL link

#import libraries
import os
from PIL import Image
import streamlit as st
import helpers

#define global variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID") #spotify client id
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET") #spotify client secret key
SAVE_PATH = "/app/songs"


#Web page UI
#---
def main():
    #set page customizations
    im = Image.open("static/favicon-16x16.png")
    st.set_page_config(
        page_title = "Spotify Down",
        page_icon = im)

    #set the web app title
    st.header('Spotify Down', divider = 'green')

    #add text to explain app
    st.write("Automatically download a song to your local machine using [Spotify Down](https://spotifydown.com)!")

    #create a form for the query input
    with st.form(key = 'my_form', clear_on_submit = False):
        song_search = st.text_input('Song search', placeholder = 'Saskatchewan in 1881')
        submit_button = st.form_submit_button(label = 'Search')

    if submit_button or song_search:
        #obtain the song name, artist, and Spotify URL
        song_choices = helpers.get_spotify_link(song_search, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

        if song_choices:
            for idx, (song_name, artist, spotify_link, cover_art_url) in enumerate(song_choices, start = 1):
                #display the song choice
                st.markdown(f"{idx}. {song_name} by {artist}")

                #display the songs image
                st.image(cover_art_url, width = 100)

                #make each songs image clickeable
                if st.button(f"Select", key = idx):
                    #update the user
                    st.write(f"Downloading {song_name} by {artist}...")

                    #define the path to save the song
                    save_dir = f"{SAVE_PATH}/{artist}"
                    file_name = f"{song_name}.mp3"

                    #download the song
                    helpers.download_song(spotify_link, save_dir, file_name)

                    #update the user
                    st.write("Download successful!")

        else:
            st.warning("No songs found.")
    else:
        st.warning("Please enter a song name to search.")

if __name__ == "__main__":
    main()

