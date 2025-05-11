#!/usr/bin/env python3
"""
Simple Flask app to demonstrate saving YouTube transcripts to text files.
This app doesn't require the YouTube scraping functionality, just demonstrates
the transcript saving feature.
"""

import os
import re
import datetime as dt
import json
from pathlib import Path
from flask import Flask, request, jsonify, make_response

# Import the transcript saving function
from text_demo import save_transcript_to_file

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # Preserve order in JSON responses

# Global variables to store job status and results
last_job_status = None
last_job_result = None
current_job = None

@app.route('/')
def index():
    return 'YouTube Transcript Saver API'

@app.route('/api/save/transcript', methods=["POST"])
def save_transcript():
    """Endpoint to save a transcript."""
    global current_job, last_job_status, last_job_result
    
    # Get data from request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data"}), 400
    
    # Extract required fields
    video_id = data.get("video_id")
    title = data.get("title")
    transcript_text = data.get("transcript_text")
    
    if not video_id or not title or not transcript_text:
        return jsonify({"error": "Missing required fields: video_id, title, transcript_text"}), 400
    
    # Create a video data dictionary
    video_data = {
        "video_id": video_id,
        "title": title,
        "channel_name": data.get("channel_name", "Unknown Channel"),
        "channel_id": data.get("channel_id", ""),
        "upload_date": data.get("upload_date", ""),
        "url": data.get("url", f"https://www.youtube.com/watch?v={video_id}"),
        "language": data.get("language", "en"),
        "duration_seconds": data.get("duration_seconds", 0),
        "transcript_text": transcript_text
    }
    
    # Save the transcript to a file
    file_path = save_transcript_to_file(video_data)
    
    if file_path:
        result = {
            "status": "success",
            "message": "Transcript saved successfully",
            "file_path": file_path,
            "video_data": video_data
        }
        return jsonify(result), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to save transcript"
        }), 500

# Enable CORS for all routes
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

# Handle OPTIONS requests for CORS preflight
@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

if __name__ == '__main__':
    # Create transcripts directory if it doesn't exist
    transcripts_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'transcripts'))
    transcripts_dir.mkdir(exist_ok=True)
    print(f"Transcripts will be saved to: {transcripts_dir}")
    
    port = int(os.getenv('FLASK_PORT', 5000))
    debug_mode = True
    
    print(f"Starting YouTube Transcript Saver API on port {port}, debug={debug_mode}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
