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
STREAM_CUTOFF = 5 #cutoff for the stream count of each artist
UNIQUE_SONG_CUTOFF = 3 #cutoff for the number of unique songs per artist
DIR = os.getcwd() #working directory


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
    stream_count = streams_df['artistName'].value_counts().reset_index()
    stream_count.columns = ['artistName','nStreams']
    
    #count the number of unique songs streamed for each artist
    song_count = streams_df.groupby('artistName')['trackName'].nunique().reset_index()
    song_count.columns = ['artistName','nUniqueSongs']
    
    #join both data frames together
    artists = stream_count.merge(song_count, how = 'inner', on = 'artistName')
    
    return artists

def visualize_stream_counts(artists, stream_cutoff = 25):
    """
    Visualize the number of artists across stream count cutoffs.
    """
    #define the range of stream count cutoffs
    r1, r2 = [1, stream_cutoff + 50]
    stream_cutoffs = [i for i in range(r1, r2 + 1)]
    
    #define the range of unique song cutoffs
    unique_song_cutoffs = range(1,7)
    
    #obtain the number of artists for each stream cutoff
    artists_lens = {}
    idx = 0
    for i in unique_song_cutoffs:
        for j in stream_cutoffs:
            artists_len = len(artists[(artists['nUniqueSongs'] >= i) & (artists['nStreams'] >= j)])
            artists_lens[idx] = [i, j, artists_len]
            idx += 1
    
    #transform to data frame
    artists_lens = pd.DataFrame(artists_lens).T
    artists_lens.columns = ['nUniqueSongs','nStreams','nArtists']
    
    return artists_lens


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
artists_lens = visualize_stream_counts(artists, stream_cutoff = STREAM_CUTOFF)

#define figure for plotting
fig, axes = plt.subplots(nrows = 3, ncols = 2, figsize = (8,8), sharex = True, sharey = True)
fig.suptitle("My most popular Spotify artists")
axes = axes.flatten()

#obtain the unique song counts
unique_songs = artists_lens['nUniqueSongs'].unique()

for i, unique_count in enumerate(unique_songs):
    #filter for the current 'unique_song' count
    data = artists_lens[artists_lens['nUniqueSongs'] == unique_count]
    
    #determine the number of artists based on the cutoff
    artist_len = len(artists[(artists['nStreams'] >= STREAM_CUTOFF) & (artists['nUniqueSongs'] >= unique_count)])
    
    #plot the data
    axes[i].plot(data['nStreams'], data['nArtists'])
    axes[i].set_title(f"{unique_count} unique songs")
    axes[i].axvline(x = STREAM_CUTOFF, color = 'r', linestyle = '--', label = f"chosen stream count cutoff = {STREAM_CUTOFF}")
    axes[i].axhline(y = artist_len, color = 'g', linestyle = '--', label = f"number of artists = {artist_len}")
    axes[i].legend()

#save the subplots
fig.supxlabel("stream count cutoff")
fig.supylabel("number of artists")
fig.tight_layout()
fig.savefig(f"{DIR}/popular_artists.png", format = 'png')

#remove artists below the count cutoff
print("Removing artists below the chosen cutoff...")
artists = artists[(artists['nStreams'] >= STREAM_CUTOFF) & (artists['nUniqueSongs'] >= UNIQUE_SONG_CUTOFF)]
artists = list(artists['artistName'])

#save the list of artist names
print("Saving the list of popular artists...")
with open(f"{DIR}/popular_artists.txt", 'w') as file:
    for artist in artists:
        file.write("%s\n" % artist)
print("Complete!")
