#!/usr/bin/python3

#Spotify artists
#---
#Script to obtain a list of my most popular Spotify artists for import into Lidarr.

#import libraries
import os
import json
from glob import glob
import pandas as pd
import matplotlib.pyplot as plt

#define global variables
DIR = "/path/to/spotify/data" #working directory
STREAM_CUTOFF = 5 #stream count cutoff


#Functions
#---
def load_streaming_history(dir_path):
    """
    Load all Spotify streaming history.
    """
    #define the dictionary to store combined data
    combined_data = []
    
    #obtain all streaming history file names
    files = glob(os.path.join(dir_path, '*StreamingHistory_music*.json'))
    
    #combine file contents
    for file_path in files:
        with open(file_path, 'r') as file:
            #load JSON data
            data = json.load(file)
            
            #store the results
            combined_data.append(data)
    
    return combined_data

def popular_artists(json_data):
    """
    Obtain the most popular artists streamed.
    """
    #define the column names
    columns = ['endTime','artistName','trackName','msPlayed']
    
    #define empty data frame to store streaming history
    streams_df = pd.DataFrame(columns = columns)
    for i in range(len(json_data)):
        #create data frame of streaming history
        stream_df = pd.DataFrame(json_data[i])
        streams_df = pd.concat([streams_df, stream_df])
    
    #count the number of streams for each unique artist
    artists = streams_df['artistName'].value_counts()
    
    return artists

def visualize_stream_counts(artists, stream_cutoff = 25, stream_range = 25):
    """
    Visualize the number of artists across stream count cutoffs.
    """
    #define the range of stream count cutoffs
    if stream_range > stream_cutoff:
        r1, r2 = [0, stream_cutoff + stream_range]
    else:
        r1, r2 = [stream_cutoff - stream_range, stream_cutoff + stream_range] 
    stream_cutoffs = [i for i in range(r1, r2 + 1)]
    
    #obtain the number of artists for each stream cutoff
    artists_lens = []
    for i in stream_cutoffs:
        artists_len = len(artists[artists >= i])
        artists_lens.append(artists_len)
    
    return stream_cutoffs, artists_lens


#Most popular Spotify artists
#---
#load in the Spotify streaming history
print("Loading user stream history...")
spot_streams = load_streaming_history(DIR)

#obtain the most popular artists
print("Count the number of streams per artist...")
artists = popular_artists(spot_streams)

#visualize the results
print("Creating visualization...")
stream_cutoffs, artists_lens = visualize_stream_counts(artists)
artist_len = len(artists[artists >= STREAM_CUTOFF])
plt.plot(stream_cutoffs, artists_lens)
plt.axvline(x = STREAM_CUTOFF, color = 'r', linestyle = '--', label = f"chosen stream count cutoff = {STREAM_CUTOFF}")
plt.axhline(y = artist_len, color = 'g', linestyle = '--', label = f"number of artists = {artist_len}")
plt.title("Artist stream count cutoffs")
plt.xlabel("stream count cutoff")
plt.ylabel("number of unique artists")
plt.legend()
plt.savefig(f"{DIR}/artist_stream_cutoffs.png")

#remove artists below the count cutoff
print("Removing artists below the chosen cutoff...")
artists = artists[artists >= STREAM_CUTOFF]
artists = list(artists.index)

#save the list of artist names
print("Saving the list of popular artists...")
with open(f"{DIR}/popular_artists.txt", 'w') as file:
    for artist in artists:
        file.write("%s\n" % artist)
print("Complete!")
