# Poetry Project

A Python application that allows users to search and read poems from the Poetry Foundation dataset. The application uses fuzzy matching to find poems and poets, and can read poems aloud using ElevenLabs text-to-speech.

## Features

- Search for poets using fuzzy matching
- Browse poems by selected poets
- Read poems aloud using ElevenLabs text-to-speech
- Clean and intuitive command-line interface

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

4. Create a `.env` file in the project root and add your ElevenLabs API key:
```
ELEVENLABS_API_KEY=your_api_key_here
```

5. Run the application:
```bash
poetry run python src/poetry_project/main.py
```

## Requirements

- Python 3.x
- Poetry for dependency management
- ElevenLabs API key for text-to-speech functionality

## Data

The project uses the Poetry Foundation dataset, which should be placed in the project root as `PoetryFoundationData.csv`. 