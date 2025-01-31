from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
import torch
import os
import tensorflow as tf
import requests
from requests.auth import HTTPBasicAuth
import lyricsgenius
from retry import retry
import re
from collections import defaultdict
import pronouncing

print(tf.config.list_physical_devices())

# Function to obtain OAuth2 access token with retry
@retry(exceptions=requests.RequestException, tries=10, delay=3, backoff=1)
def get_access_token(client_id, client_secret):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post('https://api.genius.com/oauth/token', data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise ValueError(f"Failed to obtain access token. Status code: {response.status_code}")

# Function to fetch popular songs for an artist using `lyricsgenius` with retry
@retry(exceptions=requests.RequestException, tries=10, delay=3, backoff=1)
def fetch_popular_songs(access_token, artist_name, max_songs=100):
    genius = lyricsgenius.Genius(access_token)
    artist = genius.search_artist(artist_name, max_songs=max_songs)
    if artist:
        return artist.songs
    else:
        return []

# Function to fetch lyrics using `lyricsgenius` with access token and process them
@retry(exceptions=requests.RequestException, tries=10, delay=3, backoff=1)
def fetch_and_process_lyrics(access_token, artist_name, max_songs=100):
    songs = fetch_popular_songs(access_token, artist_name, max_songs)
    lyrics_list = []
    for song in songs:
        lyrics = song.lyrics
        intro_index = lyrics.find("[Intro]")
        if intro_index != -1:
            lyrics = lyrics[intro_index:]
        lyrics_list.append(lyrics.strip())
    return lyrics_list

# Example usage for multiple artists
artists = [
    "Tupac Shakur", "Nas", "Jay-Z", "Eminem", "Rakim", "Kendrick Lamar", "Andre 3000", "J. Cole", "Lil Wayne",
    "Ice Cube", "Scarface", "Snoop Dogg", "Big Daddy Kane", "Lauryn Hill", "KRS-One", "Black Thought", "MF Doom",
    "Common", "Q-Tip", "RZA", "Mos Def", "Redman", "Big Pun", "Busta Rhymes", "Drake", "Missy Elliott", "LL Cool J",
    "Talib Kweli", "DMX", "Big L", "Chuck D", "Ludacris", "Lupe Fiasco", "Method Man", "Raekwon", "Slick Rick",
    "Jadakiss", "Future", "Fabolous", "Kid Cudi", "Travis Scott", "Rick Ross", "T.I.", "Nate Dogg", "JID",
    "Denzel Curry", "Earl Sweatshirt", "Joey Bada$$", "Nipsey Hussle", "GZA", "Kool G Rap", "MC Lyte", "Queen Latifah",
    "Pusha T", "Big Boi", "Juice WRLD", "ASAP Rocky", "Tyler, The Creator", "Meek Mill", "2 Chainz", "YBN Cordae",
    "Joyner Lucas", "Lil Dicky", "Wale", "Freddie Gibbs", "Chance the Rapper", "Vic Mensa", "Chief Keef", "21 Savage",
    "Lil Baby", "Gunna", "Young Thug", "Rapsody", "Migos", "Ski Mask the Slump God", "Brockhampton", "Run the Jewels",
    "Logic", "Tech N9ne", "Yelawolf", "Action Bronson", "Danny Brown", "Vince Staples"
]

max_songs_per_artist = 50  # Maximum number of songs per artist

try:
    # Get OAuth2 access token using client ID and secret (replace with your own credentials)
    access_token = get_access_token('GENIUS_CLIENT_ID', 'GENIUS_CLIENT_SECRET')
    
    all_lyrics = []
    for artist in artists:
        try:
            print(f"Fetching and processing lyrics for {artist}...")
            artist_lyrics = fetch_and_process_lyrics(access_token, artist, max_songs_per_artist)
            all_lyrics.extend(artist_lyrics)
        except Exception as e:
            print(f"Failed to fetch lyrics for {artist}: {str(e)}")
            continue
    
    print(f"Total number of lyrics collected: {len(all_lyrics)}")
    # Save the processed lyrics to a text file (replace with your desired path)
    output_file = "rap_lyrics.txt"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n\n".join(all_lyrics))
    print(f"Processed lyrics saved to {output_file}")
except Exception as e:
    print(f"Error occurred: {str(e)}")

def preprocess_lyrics(input_file, output_file):
    """
    Preprocesses lyrics by lowercasing, removing punctuation, and adding special tokens 
    for the start and end of each line to optimize the text for lyric generation.
    Args:
        input_file (str): Path to the input text file containing raw lyrics.
        output_file (str): Path to the output text file to save the cleaned lyrics.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        lyrics = file.read()
    
    # Lowercase the text
    lyrics = lyrics.lower()
    # Remove punctuation but retain newlines
    lyrics = lyrics.translate(str.maketrans("", "", string.punctuation.replace("\n", "")))
    lines = lyrics.split('\n')
    cleaned_lines = []
    for line in lines:
        words = line.split()
        cleaned_line = "<SOS> " + ' '.join(words) + " <EOS>"
        cleaned_lines.append(cleaned_line)
    
    cleaned_lyrics = '\n'.join(cleaned_lines)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_lyrics)

# Example usage (replace with your desired paths)
input_file = "rap_lyrics.txt"
output_file = "new_rap_lyrics.txt"
words_to_remove = ["nigga", "kill", "gun", "intro", "chorus", "verse", "bridge", "refrain", "bitch", "murder", "drugs", "cocaine", "pills",
                   "ass", "titties", "cum", "fuck", "shit", "whore", "ho", "motherfucker", "cunt", "pussy", "bastard"] + artists

preprocess_lyrics(input_file, output_file)
print("Preprocessing complete. Cleaned lyrics saved to", output_file)

cleaned_file_path = "final_rap_lyrics.txt"
num_lines = 10

with open(cleaned_file_path, 'r', encoding='utf-8') as file:
    for i in range(num_lines):
        line = file.readline()
        if line:
            print(line.strip())
        else:
            break