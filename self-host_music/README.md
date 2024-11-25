# Self-hosting music
Create a list of your most popular Spotify artists to create self-hosted music library via Lidarr.

## Instructions
1. Request your data from Spotify under ***Security and privacy > Account privacy > Download your data***.
2. Run the ***Spotify_popular_artists.py*** script in the same directory as your downloaded Spotify data.
This script will create a list of your most popular artists based on two criterion:
	* (1) number of times you streamed a song from a given artist (variable name ***STREAM_CUTOFF***)
	* (2) number of unique songs played from each artist (variable name ***UNIQUE_SONG_CUTOFF***)
3. Check the line plots from the ***popular_artists.png*** and adjust these two criterion accordingly through
the ***STREAM_CUTOFF*** and ***UNIQUE_SONG_CUTOFF*** variables in the ***Spotify_popular_artists.py*** script.
4. Repeat steps 2-4 until the you are satisfied with the number of Spotify artists.

This will result in a ***popular_artist.txt*** file containing your most popular artists from Spotify.
Each artists from this list can be added in Lidarr to monitor and manage your library of self-hosted music.