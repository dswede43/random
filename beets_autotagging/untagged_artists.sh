#!/bin/bash

#Monitor untagged artists
#---
#Script to monitor my music library for artists with newly added and untagged songs.

#define global variables
MUSIC_DIR="/mnt/sgdrive/music"
BEETS_DIR="/home/dan/docker/beets"


#Monitor new songs
#---
#create the output list file
> "${BEETS_DIR}/untagged_artists.txt"

#define an empty array to contain the names of artists with untagged songs
untagged_artists=()

#monitor for new folders containing .mp3 or .flac files
inotifywait -m -r -e create -e moved_to --format '%w%f' "$MUSIC_DIR" | while read NEW_ITEM; do
    #check if the new item is an .mp3 or .flac file
    if [[ -f "$NEW_ITEM" && "$NEW_ITEM" =~ \.(mp3|flac)$ ]]; then
        #get the parent directory of the new file
        PARENT_DIR=$(dirname "$NEW_ITEM")
        PARENT_DIR=$(basename "$PARENT_DIR")

        #append to the array
        untagged_artists+=("$PARENT_DIR")

        #save the array to the output list
        printf "%s\n" "${untagged_artists[@]}" > "${BEETS_DIR}/untagged_artists.txt"
    fi
done