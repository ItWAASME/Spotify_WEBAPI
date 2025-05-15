# Spotify Playlist Creator

This project uses CrewAI to create a multi-agent system that extracts song information from a PDF file and creates a Spotify playlist.

## Features

- PDF extraction of song information (title, artist, movie)
- Spotify OAuth authentication
- Song search on Spotify
- Playlist creation and track addition
- Multi-agent system using CrewAI

## Setup

### Prerequisites

- Python 3.9+
- A Spotify account
- A PDF file containing song information

### Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on the `.env.template` file:

```bash
cp .env.template .env
```

4. Edit the `.env` file and add your PDF file path:

```
PDF_FILE_PATH=path/to/your/songs.pdf
```

### Setting up Spotify Developer Account

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account or create one if you don't have it
3. Click on "Create an App"
4. Fill in the app name (e.g., "Playlist Creator") and description
5. Check the terms of service and click "Create"
6. In your app dashboard, click "Edit Settings"
7. Add `http://127.0.0.1:8888/callback` as a Redirect URI and save
8. Note your Client ID and Client Secret (click "Show Client Secret")
9. Add these credentials to your `.env` file:

```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## Usage

Run the main script:

```bash
python main.py
```

The script will:
1. Extract song information from your PDF file
2. Open a browser window for Spotify authentication
3. Search for each song on Spotify
4. Create a playlist and add the found songs to it
5. Provide a link to your new playlist

## How It Works

This project uses CrewAI to create a multi-agent system:

1. **PDF Extraction Agent**: Extracts song information from the PDF file
2. **Spotify Authentication Agent**: Handles OAuth authentication with Spotify
3. **Music Search Agent**: Searches for songs on Spotify
4. **Playlist Creation Agent**: Creates a playlist and adds songs to it

Each agent has specific tools and goals, and they work together to complete the task.

## Customization

- Modify the PDF extraction patterns in `tools/pdf_extractor.py` to match your PDF format
- Adjust the playlist creation parameters in `tools/spotify_tools.py`
- Change the agent configurations in `main.py`

## Troubleshooting

- If authentication fails, ensure your Spotify credentials are correct
- If song extraction fails, check the PDF format and adjust the extraction patterns
- If songs aren't found, try adjusting the search query format

## License

This project is licensed under the MIT License - see the LICENSE file for details.