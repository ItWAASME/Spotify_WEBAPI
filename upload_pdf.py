"""
PDF Upload Helper

This script helps users upload their PDF file to the data directory.
"""

import os
import shutil
import sys
from dotenv import load_dotenv, set_key

def main():
    print("PDF Upload Helper for Spotify Playlist Creator")
    print("=============================================")
    
    # Check if a file path was provided as a command-line argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Ask the user for the PDF file path
        pdf_path = input("Enter the path to your PDF file: ")
    
    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return
    
    # Check if it's a PDF file
    if not pdf_path.lower().endswith('.pdf'):
        print("Error: The file must be a PDF file")
        return
    
    # Create the data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Copy the file to the data directory
    filename = os.path.basename(pdf_path)
    destination = os.path.join(data_dir, filename)
    
    try:
        shutil.copy2(pdf_path, destination)
        print(f"File successfully copied to {destination}")
        
        # Update the .env file
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        
        if os.path.exists(env_file):
            # Load existing .env file
            load_dotenv(env_file)
            
            # Update the PDF_FILE_PATH variable
            set_key(env_file, "PDF_FILE_PATH", destination)
            print(f"Updated .env file with PDF_FILE_PATH={destination}")
        else:
            # Create a new .env file
            with open(env_file, "w") as f:
                f.write(f"PDF_FILE_PATH={destination}\n")
            print(f"Created .env file with PDF_FILE_PATH={destination}")
        
        print("\nYou can now run the main script with:")
        print("python main.py")
    
    except Exception as e:
        print(f"Error copying file: {str(e)}")

if __name__ == "__main__":
    main()