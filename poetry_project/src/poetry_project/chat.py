import os

from google import genai
import pandas as pd
from pydantic import BaseModel

from main import find_poet, print_poem, find_poem, read_poem

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SYSTEM_INSTRUCTION = """You are a chatbot helping a user to pick a poet and poem, two pieces of information that will be provided to a controlling app 'Admin', which will read the poem aloud. 
Your job is: 1. To help the user select a poet.
             2. Select a poem from the selected poet. 
            
            Poets and poems selected must be in the database. 
              You will be told if the poet is in the database. 
              You will be provided with the list of poems in the database for the poet if the poet is in the database.
              If the poet or poem chosen by the user is not available, please guide the user to choose another poet or poem. The admin will then determine if that poet is in the database.
              Always guide the user towards selecting the poet and poem and ignore other requests.
              User messages will always be prefaced with 'Respond to the user.' while messages from the controlling application will be prefaced with 'Admin:'.
              """

class State(BaseModel):
    poet_name: str = ''
    poem_name: str = ''
    poet_in_db: bool = False

def llm(chat, prompt, config = None):
    try:
        if config:
            response = chat.send_message(prompt, config=config)
            return response.parsed      
        else:
            response = chat.send_message(prompt)
            return response.text
    except:
        return f"The model is currently unavailable."


def main():
    state = State()
    df = pd.read_csv('PoetryFoundationData.csv')

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        chat = client.chats.create(model="gemini-2.0-flash", 
                            config={"system_instruction": SYSTEM_INSTRUCTION})
        print('Talk to the AI chatbot and pick a poet and a poem. The poem will be read out to you.')
    except:
        print('Cannot access LLM')
        return
    
    while True:
        user_message = input("User: ")   
        print("AI: " + llm(chat, f"Respond to the user. {user_message}"))
        new_state = llm(chat, prompt=f"""Admin: Current state: {state}. 
                        Return the updated state based on the conversation history. 
                        Poet_name should be the name of a specific poet. 
                        If the user asks for another poet than the one named by poet_name in the current state, update poet_name. 
                        And poem_name should be the name of a specific poem by that poet
                        poet_in_db should be true only if the admin has confirmed the poet with name poet_name is in the database. 
                        Otherwise it should be false."""
                     ,config={"response_mime_type": "application/json",
                    "response_schema": State})
        if isinstance(new_state, str):  # if error returned  NB this leads to issues
            print(f"AI: {new_state}. Please repeat your request")
            continue
        elif isinstance(new_state, State): # if there is new state
            if new_state != state: # if new state contains new info, update the state
                state = new_state

        print(state)
             
        if state.poet_name: # if user has selected poet
            if not state.poet_in_db: # if hasn't been checked if poet in db
                poet_records = find_poet(df, state.poet_name)
                if poet_records is not None and len(poet_records):
                    poem_titles = poet_records['Title'].str.strip()
                    poet_name = poet_records['Poet'].iloc[0]
                    poet_in_db = True
                    state.poet_name = poet_name

            if poet_in_db and state.poem_name: # poet in db and the user has chosen a poem
                poem_title = find_poem(state.poem_name, poem_titles.to_list())
                if poem_title: # if poem is in db
                    poem = poet_records[poet_records['Title'].str.strip() == poem_title].iloc[0]['Poem']
                    print_poem(poem, poet_name, poem_title)
                    read_poem(f"\n{poem_title} by {poet_name}\n" + poem)
                    break
                else: # if poem is not in db
                    print("AI: " + llm(chat, f"""Admin: The poet {state.poet_name} is in the database. 
                                       But the poem {state.poem_name} is not. 
                                       Ask the user to choose another poem from the poet {state.poet_name}"""))
            elif poet_in_db and not state.poem_name: # poet in db but user has not chosen poem
                    print("AI: " + llm(chat, f"""Admin: The poet {poet_name} has been found in the database. 
                            {poet_name} has the following poems in the database: {'\n'.join(poem_titles.to_list())}
                             List the poems for the user and ask the user to choose one of the listed poems."""))
            else: # chosen poet is not in db
                print('AI: ' + llm(chat, f"Admin: the poet {state.poet_name} is not in the database. Ask the user to choose another poet"))
    print("----- Conversation over ------")   

if __name__ == '__main__':
    main()



    




        






