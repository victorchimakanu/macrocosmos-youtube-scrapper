#!/usr/bin/env python3
"""
Test script for the PDF generation functionality.
This script demonstrates how to use the PDF generation functions to save YouTube transcripts.
"""

import sys
import os
from pathlib import Path
import json

# Import the PDF generation functions from pdf_demo.py
from pdf_demo import save_transcript_to_file, save_transcript_to_pdf

def main():
    """Main function to run the tests."""
    if len(sys.argv) < 2:
        print("Usage: python test_pdf.py [video_id] [title] [transcript_text]")
        print("Example: python test_pdf.py dQw4w9WgXcQ 'Never Gonna Give You Up' 'This is the transcript text'")
        
        # Use a sample video data if no arguments are provided
        video_id = "sample123"
        title = "Sample Video Title"
        transcript_text = "This is a sample transcript.\n\nIt has multiple paragraphs.\n\nEach paragraph will be formatted nicely in the PDF."
    else:
        video_id = sys.argv[1]
        title = sys.argv[2] if len(sys.argv) > 2 else "Untitled Video"
        transcript_text = sys.argv[3] if len(sys.argv) > 3 else "No transcript available."
    
    # Create a sample video data dictionary
    sample_video_data = {
        "video_id": video_id,
        "title": title,
        "channel_name": "Sample Channel",
        "channel_id": "UC123456789",
        "upload_date": "2023-05-09",
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "language": "en",
        "duration_seconds": 300,
        "transcript_text": transcript_text
    }
    
    print(f"\n=== Testing PDF generation for video: {title} ({video_id}) ===")
    
    # Save to text file
    text_file_path = save_transcript_to_file(sample_video_data)
    if text_file_path:
        print(f"\nText file saved to: {text_file_path}")
        
        # Display the content of the text file
        print("\nText file content:")
        print("-" * 50)
        with open(text_file_path, 'r', encoding='utf-8') as f:
            print(f.read())
        print("-" * 50)
    else:
        print("\nFailed to save text file.")
    
    # Save to PDF file
    pdf_file_path = save_transcript_to_pdf(sample_video_data)
    if pdf_file_path:
        print(f"\nPDF file saved to: {pdf_file_path}")
    else:
        print("\nFailed to save PDF file.")
    
    # List all files in the transcripts directory
    transcripts_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'transcripts'))
    print(f"\nAll files in {transcripts_dir}:")
    for file_path in transcripts_dir.glob('*'):
        print(f"  - {file_path.name}")

if __name__ == "__main__":
    main()
