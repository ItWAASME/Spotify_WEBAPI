"""
PDF Extractor Module

This module handles extracting song information from PDF files.
"""

import os
import PyPDF2
from typing import List, Dict, Any

def extract_songs_from_pdf(pdf_path: str) -> List[Dict[str, str]]:
    """
    Extract song information from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dictionaries with song_title and artist
    """
    print(f"Extracting songs from PDF: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return []
    
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        # Print a sample of the extracted text for debugging
        print("Sample of extracted text (first 500 chars):")
        print(text[:500])
        
        # Process the text to extract song information
        lines = text.split('\n')
        songs = []
        
        # Debug: Print first few lines
        print("\nFirst 15 lines from PDF:")
        for i, line in enumerate(lines[:15]):
            print(f"Line {i}: {line}")
        
        # Extract songs at specific intervals (0, 5, 10, etc.)
        # This assumes each song entry takes up exactly 5 lines
        for i in range(0, len(lines), 5):
            if i >= len(lines):
                break
                
            # Get the song title from the first line of each entry
            song_title = lines[i].strip()
            
            # Skip empty lines
            if not song_title:
                continue
                
            # Try to find artist information in the next few lines
            artist = "Unknown Artist"
            for j in range(i, min(i+5, len(lines))):
                if j >= len(lines):
                    break
                    
                line = lines[j].strip()
                if "Artistes:" in line:
                    artist_parts = line.split("Artistes:", 1)
                    if len(artist_parts) > 1:
                        artist = artist_parts[1].split("Lyricist:", 1)[0].strip()
                        break
            
            # Add the song if we have a title
            if song_title:
                songs.append({
                    "song_title": song_title,
                    "artist": artist
                })
                print(f"Extracted: {song_title} by {artist}")
        
        # If no songs found with the interval approach, try the original methods
        if not songs:
            print("No songs found with the interval approach. Trying alternative extraction...")
            
            # Process each song entry looking for "Film:" marker
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                    
                # Check if this line contains "Film:" which indicates it's part of a song entry
                if "Film:" in line:
                    # Extract song title (assuming it's the text before "Film:")
                    parts = line.split("Film:", 1)
                    song_title = parts[0].strip()
                    
                    # Extract artist information
                    artist = ""
                    if "Artistes:" in line:
                        artist_parts = line.split("Artistes:", 1)
                        if len(artist_parts) > 1:
                            artist = artist_parts[1].split("Lyricist:", 1)[0].strip()
                    
                    # If we couldn't find artist in the same line, check next line
                    if not artist and i+1 < len(lines) and "Artistes:" in lines[i+1]:
                        artist_parts = lines[i+1].split("Artistes:", 1)
                        if len(artist_parts) > 1:
                            artist = artist_parts[1].split("Lyricist:", 1)[0].strip()
                    
                    # Add the song if we have a title
                    if song_title:
                        songs.append({
                            "song_title": song_title,
                            "artist": artist if artist else "Unknown Artist"
                        })
                        print(f"Extracted (alt): {song_title} by {artist if artist else 'Unknown Artist'}")
        
        # If still no songs found, allow manual input
        if not songs:
            print("No songs automatically detected. The PDF format might not be recognized.")
            print("Would you like to manually enter some songs? (y/n)")
            if input().lower() == 'y':
                print("Enter songs in format 'Song Title - Artist' (enter empty line to finish):")
                while True:
                    entry = input().strip()
                    if not entry:
                        break
                    if ' - ' in entry:
                        parts = entry.split(' - ', 1)
                        song_title = parts[0].strip()
                        artist = parts[1].strip()
                        songs.append({
                            "song_title": song_title,
                            "artist": artist
                        })
                    else:
                        print("Invalid format. Please use 'Song Title - Artist'")
        
        print(f"Found {len(songs)} songs in the PDF")
        return songs
        
    except Exception as e:
        print(f"Error extracting songs from PDF: {str(e)}")
        print(f"Exception details: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return []