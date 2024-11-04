# Self-hosting music
Create a list of your most popular Spotify artists for import into Lidarr for self-hosting music.

## Instructions
1. Request your data from Spotify under ***Security and privacy > Account privacy > Download your data***.
2. Run the ***Spotify_popular_artists.py*** script in the same directory as your downloaded Spotify data.
3. Check the ***artist_stream_cutoffs.png*** image and adjust the artist stream count cutoff accordingly via
the ***STREAM_CUTOFF*** global variable in the ***Spotify_popular_artists.py*** script.
4. Repeat steps 2-4 until the you are satisfied with the number of Spotify artists.

This will result in a ***popular_artist.txt*** file containing your most popular artists from Spotify.
This list can be imported into Lidarr to monitor and manage your library of self-hosted music.