#Helper functions - fSpotify
#---
#Helper functions to automate song downloading from Spotify

#import modules
import os
import re
import hashlib

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from playwright.sync_api import sync_playwright


#Functions and classes
#---
class PasswordManager:
    """Functions to manage a single user password."""
    def __init__(self, file_path = "security/password.txt"):
        self.file_path = file_path
    
    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_password(self):
        """Load the stored password hash if it exists."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return f.read().strip()
        return None
    
    def save_password(self, password):
        """Save a new password hash to the file."""
        with open(self.file_path, "w") as f:
            f.write(self.hash_password(password))
    
    def authenticate(self, password_input):
        """Authenticate the user by comparing input hash to stored hash."""
        stored_password = self.load_password()
        return self.hash_password(password_input) == stored_password


def get_spotify_link(song_search, spotify_client_id, spotify_client_secret):
    """Search for a song on Spotify and return multiple song choices."""
    #authenticate with Spotify
    try:
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id = spotify_client_id,
            client_secret = spotify_client_secret))
    except Exception as e:
        return f"Authentication failed: {e}"
    
    #define the query
    query = f"track:{song_search}"
    
    #query the Spotify API for the song information
    try:
        results = spotify.search(q = query, type = 'track', limit = 5)
    except Exception as e:
        return f"Error during search: {e}"
    
    #define the song track
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        #create empty list to hold song choices
        song_choices = []
        for track in tracks:
            song_name = track['name']
            artist = track['album']['artists'][0]['name']
            spotify_link = track['external_urls']['spotify']
            cover_art_url = track['album']['images'][0]['url']
            song_choices.append((song_name, artist, spotify_link, cover_art_url))
        
        #return the song choices
        return song_choices
    else:
        return False


class SpotifyDownloader:
    """Functions to convert Spotify songs to MP3."""
    def __init__(self, song_link, save_dir, file_name):
        self.song_link = song_link
        self.save_dir = save_dir
        self.file_name = file_name
    
    def spotifydown(self):
        """Convert a song to MP3 using Spotify Down (https://spotifydown.com)."""
        with sync_playwright() as p:
            #launch a browser instance with a temporary download directory
            browser = p.firefox.launch(headless = True)
            context = browser.new_context(accept_downloads = True)
            page = context.new_page()
            
            #navigate to the target URL
            page.goto("https://spotifydown.com")
            
            #navigate to download page
            try:
                page.wait_for_load_state("networkidle")
                page.get_by_placeholder("https://open.spotify.com/..../").click()
                page.get_by_placeholder("https://open.spotify.com/..../").fill(self.song_link)
                page.get_by_role("button", name = "Download").click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name = "Download").click()
            except Exception as e:
                browser.close()
                return False
            
            #attempt to click the "Download MP3" button until successful
            max_retries = 10  #set a maximum retry count to avoid infinite loop
            retries = 0
            
            while retries < max_retries:
                try:
                    #wait for the loading bar to disappear and "Download MP3" to appear
                    page.wait_for_selector("a.transition:nth-child(1)", timeout=5000)
                    
                    #try to click the "Download MP3" button
                    with page.expect_download() as download_info:
                        page.locator("a.transition:nth-child(1)").click()
                    download = download_info.value
                    
                    #create directory for download
                    os.makedirs(self.save_dir, exist_ok = True)
                    
                    #define the path to save the file
                    download_path = os.path.join(self.save_dir, self.file_name)
                    
                    #save the downloaded file to the desired directory with the custom name
                    download.save_as(download_path)
                    
                    #exit the loop once download succeeds
                    break
                
                except Exception as e:
                    #eait 3 seconds before trying again
                    page.wait_for_timeout(1000)
                    retries += 1
            
            else:
                browser.close()
                return False
            
            #close the browser
            browser.close()
            return True
    
    def spowload(self):
        """Convert a song to MP3 using Spowload (https://spowload.com)."""
        #obtain the songs track id
        match = re.search(r'(?<=track/)(.*?)(?=\?si=)', self.song_link)
        if not match:
            match = re.search(r'(?<=track/).*', self.song_link)
        track_id = match.group(0)
        
        with sync_playwright() as p:
            #launch a browser instance with a temporary download directory
            browser = p.firefox.launch(headless = True)
            context = browser.new_context(accept_downloads = True)
            page = context.new_page()
            
            #navigate to the target URL
            page.goto("https://spowload.com")
            
            #navigate to download page
            try:
                page.get_by_placeholder("Paste your link here...").click()
                page.get_by_placeholder("Paste your link here...").fill(self.song_link)
                page.get_by_role("button", name = "Start").click()
                page.goto(f"https://spowload.com/spotify/track-{track_id}")
                page.get_by_role("button", name="Convert", exact=True).click()
            except Exception as e:
                browser.close()
                return False
            
            #attempt to click the "Download" button until successful
            max_retries = 5  #set a maximum retry count to avoid infinite loop
            retries = 0
            
            while retries < max_retries:
                try:
                    #try to click the "Download MP3" button
                    with page.expect_download() as download_info:
                        page.get_by_role("link", name = "Download", exact = True).click()
                    download = download_info.value
                    
                    #create directory for download
                    os.makedirs(self.save_dir, exist_ok = True)
                    
                    #define the path to save the file
                    download_path = os.path.join(self.save_dir, self.file_name)
                    
                    #save the downloaded file to the desired directory with the custom name
                    download.save_as(download_path)
                    
                    #exit the loop once download succeeds
                    break
                
                except Exception as e:
                    #wait before trying again
                    page.wait_for_timeout(500)
                    retries += 1
            
            else:
                browser.close()
                return False
            
            #close the browser
            browser.close()
            return True
    
    def spotifymp3(self):
        """Convert a song to MP3 using SpotifyMP3 (https://spotifymp3.com)."""    
        with sync_playwright() as p:
            #launch a browser instance with a temporary download directory
            browser = p.firefox.launch(headless = True)
            context = browser.new_context(accept_downloads = True)
            page = context.new_page()
            
            #navigate to the target URL
            page.goto("https://spotifymp3.com")
            
            #navigate to download page
            try:
                page.wait_for_load_state("networkidle")
                page.get_by_placeholder("https://open.spotify.com/").click()
                page.get_by_placeholder("https://open.spotify.com/").fill(self.song_link)
                page.get_by_role("button", name = "Download").click()
                page.wait_for_timeout(2000)
                page.get_by_role("button", name = " Get Download", exact = True).click()
            except Exception as e:
                browser.close()
                return False
            
            #attempt to click the "Download" button until successful
            max_retries = 5  #set a maximum retry count to avoid infinite loop
            retries = 0
            
            while retries < max_retries:
                try:
                    #try to click the "Download MP3" button
                    with page.expect_download() as download_info:
                        page.get_by_role("link", name = "Download MP3", exact = True).click()
                    download = download_info.value
                    
                    #create directory for download
                    os.makedirs(self.save_dir, exist_ok = True)
                    
                    #define the path to save the file
                    download_path = os.path.join(self.save_dir, self.file_name)
                    
                    #save the downloaded file to the desired directory with the custom name
                    download.save_as(download_path)
                    
                    #exit the loop once download succeeds
                    break
                
                except Exception as e:
                    #wait before trying again
                    page.wait_for_timeout(500)
                    retries += 1
            
            else:
                browser.close()
                return False
            
            #close the browser
            browser.close()
            return True
    
    def download_song(self):
        """Download the song given its Spotify URL."""
        if self.spotifymp3():
            return True
        if self.spowload():
            return True
        if self.spowloadnet():
            return True
        else:
            return False

