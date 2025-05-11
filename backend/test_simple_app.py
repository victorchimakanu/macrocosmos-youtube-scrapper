#!/usr/bin/env python3
"""
Test script for the simple Flask app.
This script tests the transcript saving functionality.
"""

import requests
import json
import sys

# Base URL for the API
BASE_URL = "http://localhost:5000/api"

def test_save_transcript(video_id, title, transcript_text):
    """Test saving a transcript."""
    print(f"\n=== Testing transcript saving for video: {title} ({video_id}) ===")
    
    # Create the request data
    data = {
        "video_id": video_id,
        "title": title,
        "transcript_text": transcript_text,
        "channel_name": "Test Channel",
        "upload_date": "2023-05-09",
        "duration_seconds": 300
    }
    
    # Make the request to save the transcript
    response = requests.post(
        f"{BASE_URL}/save/transcript",
        json=data
    )
    
    # Print the response
    print(f"Status code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if "file_path" in result:
                print(f"\nTranscript saved to: {result['file_path']}")
                
                # Display the content of the saved file
                try:
                    with open(result['file_path'], 'r', encoding='utf-8') as f:
                        print("\nFile content:")
                        print("-" * 50)
                        print(f.read())
                        print("-" * 50)
                except Exception as e:
                    print(f"Error reading file: {str(e)}")
    except Exception as e:
        print(f"Error parsing response: {str(e)}")
        print(f"Response text: {response.text}")
    
    return response

def main():
    """Main function to run the tests."""
    if len(sys.argv) < 3:
        print("Usage: python test_simple_app.py [video_id] [title] [transcript_text]")
        print("Example: python test_simple_app.py dQw4w9WgXcQ 'Never Gonna Give You Up' 'This is the transcript text'")
        
        # Use default values if not enough arguments are provided
        video_id = "test123"
        title = "Test Video"
        transcript_text = "This is a test transcript.\n\nIt has multiple paragraphs.\n\nEach paragraph will be saved to the text file."
    else:
        video_id = sys.argv[1]
        title = sys.argv[2]
        transcript_text = sys.argv[3] if len(sys.argv) > 3 else "No transcript available."
    
    # Test saving a transcript
    test_save_transcript(video_id, title, transcript_text)

if __name__ == "__main__":
    main()
