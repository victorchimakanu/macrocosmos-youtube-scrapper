#!/usr/bin/env python3
"""
Simple script to demonstrate saving YouTube transcripts to text files.
This script doesn't require any external dependencies.
"""

import os
import re
import datetime as dt
from pathlib import Path

def save_transcript_to_file(video_data):
    """
    Save the transcript of a YouTube video to a text file.
    
    Args:
        video_data (dict): Dictionary containing video information including transcript
    
    Returns:
        str: Path to the saved transcript file or None if saving failed
    """
    try:
        # Create transcripts directory if it doesn't exist
        transcripts_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'transcripts'))
        transcripts_dir.mkdir(exist_ok=True)
        
        # Extract video information
        video_id = video_data.get('video_id', 'unknown')
        title = video_data.get('title', 'Untitled')
        
        # Clean the title to make it suitable for a filename
        clean_title = re.sub(r'[\\/*?:"<>|]', '', title)  # Remove invalid filename characters
        clean_title = re.sub(r'\s+', '_', clean_title)    # Replace spaces with underscores
        
        # Create a timestamp
        timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create the filename
        filename = f"{clean_title}-{timestamp}-{video_id}.txt"
        filepath = transcripts_dir / filename
        
        # Get the transcript text
        transcript_text = video_data.get('transcript_text', '')
        
        if not transcript_text:
            print(f"No transcript available for video: {title} ({video_id})")
            return None
        
        # Write the transcript to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"URL: {video_data.get('url', '')}\n")
            f.write(f"Channel: {video_data.get('channel_name', '')}\n")
            f.write(f"Upload Date: {video_data.get('upload_date', '')}\n")
            f.write(f"Duration: {video_data.get('duration_seconds', 0)} seconds\n")
            f.write("\n" + "="*50 + "\n\nTRANSCRIPT:\n\n" + "="*50 + "\n\n")
            f.write(transcript_text)
        
        print(f"Transcript saved to: {filepath}")
        return str(filepath)
        
    except Exception as e:
        print(f"Error saving transcript: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test with a sample video data
    sample_video_data = {
        "video_id": "sample123",
        "title": "Sample Video Title",
        "channel_name": "Sample Channel",
        "channel_id": "UC123456789",
        "upload_date": "2023-05-09",
        "url": "https://www.youtube.com/watch?v=sample123",
        "language": "en",
        "duration_seconds": 300,
        "transcript_text": "This is a sample transcript.\n\nIt has multiple paragraphs.\n\nEach paragraph will be formatted nicely in the text file."
    }
    
    # Save to text file
    text_file_path = save_transcript_to_file(sample_video_data)
    print(f"Text file saved to: {text_file_path}")
    
    # Display the content of the text file
    if text_file_path:
        print("\nText file content:")
        print("-" * 50)
        with open(text_file_path, 'r', encoding='utf-8') as f:
            print(f.read())
        print("-" * 50)
    
    # List all files in the transcripts directory
    transcripts_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'transcripts'))
    print(f"\nAll files in {transcripts_dir}:")
    for file_path in transcripts_dir.glob('*'):
        print(f"  - {file_path.name}")
