"""
Simple Spotify Playlist Creator - Main Script

This script extracts song information from a PDF file and creates a Spotify playlist.
It uses the `simple` package which contains functions for extracting songs from a PDF,
authenticating with Spotify, searching for songs on Spotify, and creating a playlist.
The script also handles exceptions and provides feedback to the user.
"""

import os
import sys
import traceback
from dotenv import load_dotenv

# Import modules from the simple package
from simple.pdf_extractor import extract_songs_from_pdf
from simple.spotify_auth import authenticate_spotify
from simple.spotify_search import search_songs
from simple.spotify_playlist import create_playlist

# Load environment variables
load_dotenv()

def main():
    """Main function to run the script."""
    print("=== Spotify Playlist Creator ===")
    print("You can press Ctrl+C during song search to stop and create a playlist with songs found so far.")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("Error: .env file not found")
        print("Please create a .env file with your Spotify API credentials")
        sys.exit(1)
    
    # Get PDF file path from .env or user input
    pdf_path = os.getenv("PDF_FILE_PATH")
    if not pdf_path or not os.path.exists(pdf_path):
        pdf_path = input("Enter the path to your PDF file: ")
    
    try:
        # Extract songs from PDF
        songs = extract_songs_from_pdf(pdf_path)
        
        if not songs:
            print("No songs found in the PDF. Please check the file format.")
            sys.exit(1)
        
        # Print found songs
        print(f"\nFound {len(songs)} songs in the PDF.")
        
        # Ask user how many songs to process
        max_songs = len(songs)
        print(f"\nHow many songs would you like to search for? (1-{max_songs}, default: all)")
        print("Enter a number or press Enter to search for all songs:")
        
        song_limit_input = input().strip()
        if song_limit_input and song_limit_input.isdigit():
            song_limit = min(int(song_limit_input), max_songs)
            if song_limit < max_songs:
                print(f"Will search for the first {song_limit} songs out of {max_songs}.")
                songs = songs[:song_limit]
        
        # Print songs that will be searched
        print("\nSearching for the following songs:")
        for i, song in enumerate(songs, 1):
            print(f"{i}. {song['song_title']} by {song['artist']}")
        
        # Authenticate with Spotify
        sp = authenticate_spotify()
        
        # Search for songs on Spotify
        search_results = search_songs(sp, songs)
        
        # Check if we have any found songs
        found_count = sum(1 for r in search_results if r.get("found", False))
        if found_count == 0:
            print("\nNo songs were found on Spotify. Cannot create a playlist.")
            print("Please try again with different songs or check the song information.")
            return
        
        # Create playlist
        playlist_name = input("\nEnter a name for your playlist: ")
        description = input("Enter a description for your playlist (optional): ")
        
        result = create_playlist(sp, search_results, playlist_name, description)
        
        if result["status"] == "success":
            print("\n=== Success! ===")
            print(f"Playlist '{result['playlist_info']['name']}' created successfully")
            print(f"URL: {result['playlist_info']['url']}")
            print(f"Added {result['tracks_added']} tracks to the playlist")
            
            if result["not_found"]:
                print("\nThe following songs were not found on Spotify:")
                for i, song in enumerate(result["not_found"], 1):
                    print(f"{i}. {song['song_title']} by {song['artist']}")
        else:
            print("\n=== Error ===")
            print(result["message"])
    
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n=== Unexpected Error ===")
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()