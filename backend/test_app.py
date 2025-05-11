#!/usr/bin/env python3
"""
Test script for the YouTube scraper Flask app.
This script tests the basic functionality of the Flask app by making requests to the API endpoints.
"""

import requests
import json
import time
import sys

# Base URL for the API (default port is 5000, but can be changed via FLASK_PORT env var)
# Update this if you're using a different port
BASE_URL = "http://localhost:5000/api"


def test_scrape_video(video_id):
    """Test scraping a YouTube video by ID."""
    print(f"\n=== Testing video scraping for ID: {video_id} ===")

    # Make the request to scrape the video
    response = requests.post(
        f"{BASE_URL}/scrape/video",
        json={"video_id": video_id}
    )

    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 202:
        # Poll for the result
        print("\nPolling for results...")
        while True:
            status_response = requests.get(f"{BASE_URL}/scrape/status")
            status = status_response.json().get("status")
            print(f"Status: {status}")

            if status == "completed" or status == "failed":
                result_response = requests.get(f"{BASE_URL}/scrape/result")
                result_json = result_response.json()
                print(f"\nFinal result: {json.dumps(result_json, indent=2)}")

                # Display information about saved transcript files
                if "result" in result_json and "saved_transcript_files" in result_json["result"]:
                    saved_files = result_json["result"]["saved_transcript_files"]
                    if saved_files:
                        print(
                            f"\nSaved {len(saved_files)} transcript text files:")
                        for file_path in saved_files:
                            print(f"  - {file_path}")
                    else:
                        print("\nNo transcript text files were saved.")

                # Display information about saved PDF files
                if "result" in result_json and "saved_pdf_files" in result_json["result"]:
                    saved_pdf_files = result_json["result"]["saved_pdf_files"]
                    if saved_pdf_files:
                        print(
                            f"\nSaved {len(saved_pdf_files)} transcript PDF files:")
                        for file_path in saved_pdf_files:
                            print(f"  - {file_path}")
                    else:
                        print("\nNo transcript PDF files were saved.")

                return result_json

            time.sleep(2)  # Wait 2 seconds before polling again

    return None


def test_scrape_channel(channel_id, max_videos=3):
    """Test scraping videos from a YouTube channel by ID."""
    print(f"\n=== Testing channel scraping for ID: {channel_id} ===")

    # Make the request to scrape the channel
    response = requests.post(
        f"{BASE_URL}/scrape/channel",
        json={"channel_id": channel_id, "max_videos": max_videos}
    )

    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 202:
        # Poll for the result
        print("\nPolling for results...")
        while True:
            status_response = requests.get(f"{BASE_URL}/scrape/status")
            status = status_response.json().get("status")
            print(f"Status: {status}")

            if status == "completed" or status == "failed":
                result_response = requests.get(f"{BASE_URL}/scrape/result")
                result_json = result_response.json()
                print(f"\nFinal result: {json.dumps(result_json, indent=2)}")

                # Display information about saved transcript files
                if "result" in result_json and "saved_transcript_files" in result_json["result"]:
                    saved_files = result_json["result"]["saved_transcript_files"]
                    if saved_files:
                        print(
                            f"\nSaved {len(saved_files)} transcript text files:")
                        for file_path in saved_files:
                            print(f"  - {file_path}")
                    else:
                        print("\nNo transcript text files were saved.")

                # Display information about saved PDF files
                if "result" in result_json and "saved_pdf_files" in result_json["result"]:
                    saved_pdf_files = result_json["result"]["saved_pdf_files"]
                    if saved_pdf_files:
                        print(
                            f"\nSaved {len(saved_pdf_files)} transcript PDF files:")
                        for file_path in saved_pdf_files:
                            print(f"  - {file_path}")
                    else:
                        print("\nNo transcript PDF files were saved.")

                return result_json

            time.sleep(2)  # Wait 2 seconds before polling again

    return None


def main():
    """Main function to run the tests."""
    if len(sys.argv) < 2:
        print(
            "Usage: python test_app.py [video|channel] [id] [max_videos (optional)]")
        return

    test_type = sys.argv[1].lower()

    if test_type not in ["video", "channel"]:
        print("Invalid test type. Use 'video' or 'channel'.")
        return

    if len(sys.argv) < 3:
        print(
            f"Please provide a {'video' if test_type == 'video' else 'channel'} ID.")
        return

    identifier = sys.argv[2]

    if test_type == "video":
        test_scrape_video(identifier)
    else:  # channel
        max_videos = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        test_scrape_channel(identifier, max_videos)


if __name__ == "__main__":
    main()
