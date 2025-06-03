import os

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import pandas as pd
from rapidfuzz import fuzz, process, utils




def find_poet(df, poet_name, threshold=90):
    """
    Find rows where the poet name fuzzy matches the given name.
    
    Args:
        df: pandas DataFrame
        poet_name: string to match against
        threshold: minimum similarity score (0-100)
    
    Returns:
        DataFrame with best name match
    """
    # Get unique poet names
    unique_poets = df['Poet'].unique()
    
    # Find matches using rapidfuzz
    match = process.extractOne(
            poet_name,
            unique_poets,
            scorer=fuzz.partial_ratio,
            score_cutoff=threshold,
            processor=utils.default_process
        )
    # Extract matched name
    if match:
        matched_name = match[0]
    else:
        return None
    
    # Return rows with matched name
    return df[df['Poet'] == matched_name]


def find_poem(poem, poems, threshold=70):
    """Find closest fuzzy match for poem in poems"""
    match = process.extractOne(
            poem,
            poems,
            scorer=fuzz.partial_ratio,
            score_cutoff=threshold,
            processor=utils.default_process
        )
    # Extract matched name
    if match:
        return match[0]
    else:
        return None



def print_poem(poem, poet_name, poem_title):
    """
    Print a poem with proper formatting.
    
    Args:
        poem: string containing the poem
        poet_name: name of the poet
    """
    # Print a separator line
    print("\n" + "="*50)
    
    # Print the poem title and poet
    print(f"\n{poem_title} by {poet_name}\n")
    
    # Print the poem with preserved formatting
    print(poem)
    
    # Print a separator line
    print("\n" + "="*50 + "\n")



def read_poem(poem):
    load_dotenv()
    try:
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
        
    except Exception as e:
        print(e)
        print('Cannot read poem right now')
        return



def main():
    df = pd.read_csv('PoetryFoundationData.csv')

    while True:
        poet_input = input('Name a poet: ')
        poet_records = find_poet(df, poet_input)
        if poet_records is not None and len(poet_records) != 0:
            poem_titles = poet_records['Title']
            poet_name = poet_records['Poet'].iloc[0]
            print('\n'.join(poem_titles.to_list()))
            poem_title = input('Choose one of the above poems: ')
            while True:
                if poem_title in poem_titles.str.strip().values:
                    poem = poet_records[poet_records['Title'].str.strip() == poem_title].iloc[0]['Poem']
                    print_poem(poem, poet_name, poem_title)  
                    read_poem(f"\n{poem_title} by {poet_input}\n" + poem)
                    break
                poem_title = input(f'{poem_title} was not found. Please choose another title: ')
            break
        else:
            print(f'{poet_input} cannot be found. ')


if __name__ == '__main__':
    main()