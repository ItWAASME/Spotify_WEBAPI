"""
Spotify Authentication Module

This module handles authentication with the Spotify API.
"""

import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def authenticate_spotify() -> spotipy.Spotify:
    """
    Authenticate with Spotify API.
    
    Returns:
        Authenticated Spotify client
    """
    print("Authenticating with Spotify...")
    
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
    
    if not client_id or not client_secret:
        print("Error: Spotify client ID and client secret are required")
        print("Please set them in your .env file")
        sys.exit(1)
    
    try:
        # Set up authentication
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-private playlist-modify-public"
        )
        
        # Create Spotify client
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # Test the connection
        user_info = sp.current_user()
        print(f"Successfully authenticated as {user_info['display_name']} (ID: {user_info['id']})")
        
        return sp
        
    except Exception as e:
        print(f"Error authenticating with Spotify: {str(e)}")
        sys.exit(1)