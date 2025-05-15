"""
Spotify Playlist Module

This module handles creating playlists and adding tracks to them on Spotify.
"""

import webbrowser
import spotipy
from typing import List, Dict, Any

def create_playlist(sp: spotipy.Spotify, search_results: List[Dict[str, Any]], playlist_name: str, description: str = "") -> Dict[str, Any]:
    """
    Create a Spotify playlist with the found tracks.
    
    Args:
        sp: Authenticated Spotify client
        search_results: List of search results from search_songs()
        playlist_name: Name of the playlist to create
        description: Description of the playlist
        
    Returns:
        Dictionary with playlist information
    """
    print(f"Creating playlist: {playlist_name}")
    
    try:
        # Get user ID
        user_id = sp.current_user()["id"]
        
        # Create a new playlist
        playlist = sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=False,
            description=description
        )
        
        # Get track IDs for found songs
        track_ids = [result["track_id"] for result in search_results if result.get("found", False)]
        
        # Add tracks to the playlist (in batches of 100 as per Spotify API limits)
        not_found = [result["original_query"] for result in search_results if not result.get("found", False)]
        
        if track_ids:
            # Add tracks in batches of 100
            for i in range(0, len(track_ids), 100):
                batch = track_ids[i:i+100]
                sp.playlist_add_items(playlist["id"], batch)
            
            print(f"Added {len(track_ids)} tracks to the playlist")
        else:
            print("No tracks found to add to the playlist")
        
        # Print playlist information
        print(f"Playlist created: {playlist['name']}")
        print(f"URL: {playlist['external_urls']['spotify']}")
        
        # Open the playlist in the browser
        webbrowser.open(playlist['external_urls']['spotify'])
        
        return {
            "status": "success",
            "message": f"Created playlist with {len(track_ids)} tracks",
            "playlist_info": {
                "id": playlist["id"],
                "name": playlist["name"],
                "url": playlist["external_urls"]["spotify"]
            },
            "tracks_added": len(track_ids),
            "not_found": not_found
        }
        
    except Exception as e:
        print(f"Error creating playlist: {str(e)}")
        return {
            "status": "error",
            "message": f"Error creating playlist: {str(e)}"
        }