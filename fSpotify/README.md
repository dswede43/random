# fSpotify
Fed up with relying on major streaming platforms like Spotify and facing constant subscription price hikes?
Self-hosting your own music library is a powerful alternative! Though setting it up may seem daunting,
fSpotify simplifies the process with a user-friendly web application that automates song downloads from Spotify,
making it easier than ever to manage and enjoy your own music collection.

Self-hosting my music collection has become much easier with tools like Lidarr, which helps organize and monitor
new releases. However, Lidarr has limitations, particularly when it comes to finding singles and EPs. Obtaining
these often requires configuring custom [Metadata Profiles](https://wiki.servarr.com/lidarr/faq) to get the
desired tracks.

But what if you’re after a rare track that’s slow to find or simply unavailable through Lidarr? Enter fSpotify!
This user-friendly web application allows you to search for songs by name and returns a list of download options.
Simply click “Download,” and the song will be saved directly to the directory you set up during Docker installation.

fSpotify works by searching Spotify’s catalog through its API using Python’s `spotipy` module to retrieve the
song’s URL. This URL is then processed by [Spotify Down](https://spotifydown.com) or [Spowload](https://spowload.com),
where the song is downloaded in headless mode via the `playwright` module. Within minutes, an .mp3 file appears in your designated directory, ready to stream through self-hosted music players like [Navidrome](https://www.navidrome.org).
Now, with full control over your library, you can enjoy your music free from subscriptions and price hikes.

## Installation
### Docker
A docker image of this application can be pulled from my Docker Hub
[repository](https://hub.docker.com/repository/docker/dswede43/fspotify/general).

#### docker run
Obtain your own ***SPOTIFY_CLIENT_ID*** and ***SPOTIFY_CLIENT_SECRET*** through
[Spotify's Web API](https://developer.spotify.com/documentation/web-api).

```
docker run -d --name fspotify \
    -p 5004:5004 \
    -e SPOTIFY_CLIENT_ID='YOUR_SPOTIFY_CLIENT_ID' \
    -e SPOTIFY_CLIENT_SECRET='YOUR_SPOTIFY_CLIENT_SECRET' \
    -v "$(pwd)":/app/songs \
    -v "$(pwd)/security":/app/security \
    dswede43/fspotify:latest
```
