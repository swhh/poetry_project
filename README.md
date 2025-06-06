# Poetry Project

A Python application that allows users to search and read poems from the Poetry Foundation dataset. The application uses fuzzy matching to find poems and poets, and can read poems aloud using ElevenLabs text-to-speech. It can also allow the user to chat with an LLM through the command line to help select a poem. 

## Features

- Search for poets using fuzzy matching
- Browse poems by selected poets
- Read poems aloud using ElevenLabs text-to-speech
- Clean and intuitive command-line interface
- Ability to find poets and poems through a Gemini-powered chat interface.

## Setup

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:
```bash
git clone [your-repository-url]
cd poetry_project
```

3. Install dependencies:
```bash
poetry install
```

4. Create a `.env` file in the project root and add your ElevenLabs API key (Add a Gemini API key 'GEMINI_API_KEY' if you want to run chat.py as well):
```
ELEVENLABS_API_KEY=your_api_key_here
```

5. Run the application:
```bash
poetry run python src/poetry_project/main.py
```

You can also run the following to access poems through a Gemini chatbot:
```bash
poetry run python src/poetry_project/chat.py
```

## Requirements

- Python 3.x
- Poetry for dependency management
- ElevenLabs API key for text-to-speech functionality
- Gemini API key for chat interface

## Data

The project uses the Poetry Foundation dataset.