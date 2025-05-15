"""
Spotify Setup Helper

This script helps users set up their Spotify API credentials.
"""

import os
import webbrowser
from dotenv import load_dotenv, set_key

def main():
    print("Spotify Setup Helper for Spotify Playlist Creator")
    print("===============================================")
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    
    if os.path.exists(env_file):
        load_dotenv(env_file)
    
    # Check if Spotify credentials are already set
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if client_id and client_secret and client_id != "your_client_id_here" and client_secret != "your_client_secret_here":
        print("Spotify credentials are already set up.")
        change = input("Do you want to change them? (y/n): ")
        
        if change.lower() != "y":
            print("Setup complete. You can now run the main script.")
            return
    
    # Open Spotify Developer Dashboard
    print("\nOpening Spotify Developer Dashboard in your browser...")
    webbrowser.open("https://developer.spotify.com/dashboard/")
    
    print("\nFollow these steps:")
    print("1. Log in with your Spotify account")
    print("2. Click on 'Create an App'")
    print("3. Fill in the app name (e.g., 'Playlist Creator') and description")
    print("4. Check the terms of service and click 'Create'")
    print("5. In your app dashboard, click 'Edit Settings'")
    print("6. Add 'http://127.0.0.1:8888/callback' as a Redirect URI and save")
    print("7. Note your Client ID and Client Secret (click 'Show Client Secret')")
    
    # Get credentials from user
    print("\nEnter your Spotify API credentials:")
    client_id = input("Client ID: ")
    client_secret = input("Client Secret: ")
    
    # Validate input
    if not client_id or not client_secret:
        print("Error: Client ID and Client Secret are required")
        return
    
    # Save to .env file
    if os.path.exists(env_file):
        # Update existing .env file
        set_key(env_file, "SPOTIFY_CLIENT_ID", client_id)
        set_key(env_file, "SPOTIFY_CLIENT_SECRET", client_secret)
        set_key(env_file, "SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
    else:
        # Create a new .env file
        with open(env_file, "w") as f:
            f.write(f"SPOTIFY_CLIENT_ID={client_id}\n")
            f.write(f"SPOTIFY_CLIENT_SECRET={client_secret}\n")
            f.write(f"SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback\n")
    
    print("\nSpotify credentials saved successfully!")
    print("You can now run the main script with:")
    print("python main.py")

if __name__ == "__main__":
    main()