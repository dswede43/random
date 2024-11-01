#Helper functions - Spotify Down app
#---
#Helper functions to automate song downloading from Spotify

#Functions
#---
#get_spotify_link: obtain the Spotify shareable link for a given song name
#download_song: download the Spotify song from https://spotifydown.com

#import libraries
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from playwright.sync_api import sync_playwright

#get_spotify_link
#---
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
        return "No track found."


#download_song
#---
def download_song(song_link, save_dir, file_name):
    #create directory for download
    os.makedirs(save_dir, exist_ok = True)

    with sync_playwright() as p:
        #launch a browser instance with a temporary download directory
        browser = p.firefox.launch(headless = True)
        context = browser.new_context(accept_downloads = True)
        page = context.new_page()

        #navigate to the target URL
        page.goto("https://spotifydown.com")

        #navigate to download page
        page.get_by_placeholder("https://open.spotify.com/..../").click()
        page.get_by_placeholder("https://open.spotify.com/..../").fill(song_link)
        page.get_by_role("button", name = "Download").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name = "Download").click()

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

                #define the path to save the file
                download_path = os.path.join(save_dir, file_name)

                #save the downloaded file to the desired directory with the custom name
                download.save_as(download_path)
                print(f"Song downloaded and saved as: {download_path}")

                #exit the loop once download succeeds
                break

            except Exception as e:
                #eait 3 seconds before trying again
                page.wait_for_timeout(3000)
                retries += 1

        else:
            return "Failed to download song :("

        #close the browser
        browser.close()

