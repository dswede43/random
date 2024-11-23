#fSpotify app
#---
#Script to run the GUI for fSpotify allowing users to search for a song by name
#and download it to a specified directory.

#import modules
import os
from PIL import Image
import streamlit as st
import helpers
import pages

#define global variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID") #spotify client id
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET") #spotify client secret key
SAVE_PATH = "/app/songs" #path to saved songs


#Web page UI
#---
def main():
    #set page customizations
    im = Image.open("static/favicon-16x16.png")
    st.set_page_config(
        page_title = "fSpotify",
        page_icon = im)
    
    #set the web app title
    st.header('fSpotify', divider = 'green')
    
    #add text to explain app
    st.write("Convert any Spotify song to MP3 and save to your local machine!")
    
    #initialize session state variables
    if "page" not in st.session_state:
        st.session_state.page = "Setup Password" if not helpers.load_password() else "Login"
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    #display the appropriate page based on state
    if st.session_state.page == "Setup Password" and not helpers.load_password():
        pages.password_setup_page()
    elif st.session_state.page == "Login" and not st.session_state.authenticated:
        pages.login_page()
    elif st.session_state.page == "Main App" and st.session_state.authenticated:
        pages.main_app_page(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SAVE_PATH)
    else:
        st.session_state.page = "Login"
        st.rerun()

if __name__ == "__main__":
    main()

