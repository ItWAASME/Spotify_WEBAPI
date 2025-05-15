"""
Spotify Search Module

This module handles searching for songs on Spotify.
"""

import spotipy
from typing import List, Dict, Any

def search_songs(sp: spotipy.Spotify, songs: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Search for songs on Spotify.
    
    Args:
        sp: Authenticated Spotify client
        songs: List of dictionaries with song_title and artist
        
    Returns:
        List of search results with track information
    """
    print("Searching for songs on Spotify...")
    print("Press Ctrl+C at any time to stop searching and create a playlist with songs found so far.")
    
    results = []
    
    try:
        for i, song in enumerate(songs):
            song_title = song.get("song_title", "")
            artist = song.get("artist", "")
            
            if not song_title:
                continue
            
            print(f"\nSearching {i+1}/{len(songs)}: {song_title} by {artist}")
            
            try:
                # Try multiple search strategies
                track = None
                
                # Strategy 1: Search with track and artist
                if artist:
                    query = f"track:{song_title} artist:{artist}"
                    search_result = sp.search(query, type="track", limit=5)
                    if search_result and search_result["tracks"]["items"]:
                        track = search_result["tracks"]["items"][0]
                
                # Strategy 2: Search with just the track name if strategy 1 failed
                if not track:
                    query = f"track:{song_title}"
                    search_result = sp.search(query, type="track", limit=5)
                    if search_result and search_result["tracks"]["items"]:
                        track = search_result["tracks"]["items"][0]
                
                # Strategy 3: Try a more general search without field specifiers
                if not track:
                    # For Indian songs, sometimes the film name is included in the title
                    # Try to extract just the song name without "Film:" part
                    if "Film:" in song_title:
                        clean_title = song_title.split("Film:")[0].strip()
                    else:
                        clean_title = song_title
                    
                    # Remove any parentheses content which might be confusing the search
                    if "(" in clean_title:
                        clean_title = clean_title.split("(")[0].strip()
                    
                    print(f"Trying simplified search: {clean_title}")
                    query = clean_title
                    search_result = sp.search(query, type="track", limit=5)
                    if search_result and search_result["tracks"]["items"]:
                        # Try to find the best match among the results
                        best_match = None
                        highest_score = 0
                        
                        for item in search_result["tracks"]["items"]:
                            # Simple scoring system - count matching words
                            title_words = set(clean_title.lower().split())
                            result_words = set(item["name"].lower().split())
                            common_words = title_words.intersection(result_words)
                            score = len(common_words) / max(len(title_words), 1)
                            
                            # If artist is specified, boost score for matching artists
                            if artist:
                                artist_words = set(artist.lower().split())
                                for spotify_artist in item["artists"]:
                                    result_artist_words = set(spotify_artist["name"].lower().split())
                                    common_artist_words = artist_words.intersection(result_artist_words)
                                    artist_score = len(common_artist_words) / max(len(artist_words), 1)
                                    score += artist_score
                            
                            if score > highest_score:
                                highest_score = score
                                best_match = item
                        
                        if best_match and highest_score > 0.3:  # Threshold for accepting a match
                            track = best_match
                
                # Check if we found a match with any strategy
                if track:
                    # Create result object
                    result = {
                        "original_query": {
                            "song_title": song_title,
                            "artist": artist
                        },
                        "found": True,
                        "track_id": track["id"],
                        "track_name": track["name"],
                        "artist_name": track["artists"][0]["name"],
                        "album_name": track["album"]["name"],
                        "preview_url": track["preview_url"],
                        "external_url": track["external_urls"]["spotify"]
                    }
                    print(f"Found match: {track['name']} by {track['artists'][0]['name']}")
                else:
                    # No match found
                    result = {
                        "original_query": {
                            "song_title": song_title,
                            "artist": artist
                        },
                        "found": False,
                        "message": "No matching track found on Spotify"
                    }
                    print(f"No match found for: {song_title}")
                
                results.append(result)
                
            except Exception as e:
                print(f"Error searching for {song_title}: {str(e)}")
                results.append({
                    "original_query": {
                        "song_title": song_title,
                        "artist": artist
                    },
                    "found": False,
                    "message": f"Error: {str(e)}"
                })
                
            # After each song, print a progress update
            found_so_far = sum(1 for r in results if r.get("found", False))
            print(f"Progress: Found {found_so_far} out of {i+1} songs processed ({len(songs)} total)")
            
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user!")
        print("Proceeding with playlist creation using songs found so far...")
    
    # Print summary
    found_count = sum(1 for r in results if r.get("found", False))
    print(f"\nSearch complete or interrupted. Found {found_count} out of {len(results)} songs on Spotify")
    
    return results