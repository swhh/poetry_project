import os
import pandas as pd
from rapidfuzz import fuzz, process

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

load_dotenv()

def find_poet_fuzzy(df, poet_name, threshold=80):
    """
    Find rows where the poet name fuzzy matches the given name.
    
    Args:
        df: pandas DataFrame
        poet_name: string to match against
        threshold: minimum similarity score (0-100)
    
    Returns:
        DataFrame with matching rows
    """
    # Get unique poet names
    unique_poets = df['Poet'].unique()
    
    # Find matches using rapidfuzz
    matches = process.extract(
        poet_name,
        unique_poets,
        scorer=fuzz.ratio,
        score_cutoff=threshold
    )
    
    # Extract matched names
    matched_names = [match[0] for match in matches]
    
    # Return rows with matched names
    return df[df['Poet'].isin(matched_names)]

def find_closest_poet(df, poet_name):
    """
    Find the single closest matching poet name.
    
    Args:
        df: pandas DataFrame
        poet_name: string to match against
    
    Returns:
        tuple of (closest_match, similarity_score)
    """
    unique_poets = df['Poet'].unique()
    best_match = process.extractOne(
        poet_name,
        unique_poets,
        scorer=fuzz.ratio
    )
    return best_match

def print_poem(poem, poet_name):
    """
    Print a poem with proper formatting.
    
    Args:
        poem: string containing the poem
        poet_name: name of the poet
    """
    # Print a separator line
    print("\n" + "="*50)
    
    # Print the poem title and poet
    print(f"\n{poet_name}\n")
    
    # Print the poem with preserved formatting
    print(poem)
    
    # Print a separator line
    print("\n" + "="*50 + "\n")

# Example usage:
df = pd.read_csv('PoetryFoundationData.csv')

# Find the closest matching poet
search_name = "Emily Dickenson"  # Note the misspelling
closest_match, score = find_closest_poet(df, search_name)
print(f"Searching for: {search_name}")
print(f"Closest match: {closest_match} (similarity score: {score})")

# Get poems by the closest matching poet
matching_poems = df[df['Poet'] == closest_match]
print(f"\nFound {len(matching_poems)} poems by {closest_match}")

# Get the first matching poem
if not matching_poems.empty:
    poem = matching_poems['Poem'].iloc[0]
    
    # Print the poem with proper formatting
    print_poem(poem, closest_match)
    
    load_dotenv()
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )
    audio = elevenlabs.text_to_speech.convert(
        text=poem,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    play(audio) 