#Pages - fSpotify
#---
#Define different pages for the fSpotify app.

#import modules
import os
import time
import hashlib
import streamlit as st
import helpers


#Pages
#---
#initialize password manager
password_manager = helpers.PasswordManager()

def password_setup_page():
    """
    Password setup page.
    """
    st.subheader("Set a password")
    password = st.text_input("Enter password", type = "password")
    confirm_password = st.text_input("Confirm password", type = "password")
    
    if st.button("Set Password") or password and confirm_password:
        if password == confirm_password:
            password_manager.save_password(password)      
            st.success("Password set successfully! Logging in...")
            time.sleep(1)
            st.session_state.page = "Login"
            st.rerun()
        else:
            st.error("Passwords do not match.")


def login_page():
    """
    Login page.
    """
    st.subheader("Login")
    password_input = st.text_input("Enter password", type = "password")
    
    if st.button("Login") or password_input:
        if password_manager.authenticate(password_input):
            st.session_state.authenticated = True
            st.success("Login successful!")
            time.sleep(1)
            st.session_state.page = "Main App"
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")


def main_app_page(spotify_client_id, spotify_client_secret, save_path):
    #create a form for the query input
    with st.form(key = 'my_form', clear_on_submit = False):
        song_search = st.text_input('Search song', placeholder = 'Example: Saskatchewan in 1881')
        submit_button = st.form_submit_button(label = 'Search')
    
    if submit_button or song_search:
        #obtain the song name, artist, and Spotify URL
        song_choices = helpers.get_spotify_link(song_search, spotify_client_id, spotify_client_secret)
        
        if song_choices:
            for idx, (song_name, artist, spotify_link, cover_art_url) in enumerate(song_choices, start = 1):
                #display the song choice
                st.markdown(f"{idx}. {song_name} by {artist}")
                
                #display the songs image
                st.image(cover_art_url, width = 100)
                
                #make each songs image clickeable
                if st.button("Download", key = idx):
                    #update the user
                    st.info(f"Downloading {song_name} by {artist}...")
                    
                    #define the path to save the song
                    save_dir = f"{save_path}/{artist}"
                    file_name = f"{song_name}.mp3"
                    
                    #intialize the downloader
                    downloader = helpers.SpotifyDownloader(spotify_link, save_dir, file_name)
                    
                    #download the song
                    if downloader.download_song():
                        st.success("Download successful!")
                    else:
                        st.error("Download Failed! Please try again.")
        else:
            st.warning("No songs found.")
    elif not song_search:
        st.warning("Please enter a song name.")

