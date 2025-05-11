from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from flask import Flask, request, jsonify, make_response, send_file
import sys
import os
import threading
import asyncio
import datetime as dt
import json
import traceback
import re
from pathlib import Path

# Add the repo root to sys.path so `common` and `scraping` modules are importable:
here = os.path.dirname(__file__)
repo_root = os.path.abspath(os.path.join(here, '..'))
sys.path.insert(0, repo_root)

# Import PDF generation libraries
# Import YouTube scraper and related modules
from common.data import DataLabel
from common.date_range import DateRange
from scraping.youtube.youtube_custom_scraper import YouTubeTranscriptScraper


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # Preserve order in JSON responses
API_KEY = os.getenv("API_KEY")  # Optional API key for authentication

# Global variables to track job status
last_job_status = None
last_job_result = None
current_job = None

# Create a global scraper instance
scraper = YouTubeTranscriptScraper()


# Helper functions for YouTube video processing

def entity_to_dict(entity):
    """Convert a DataEntity to a JSON-serializable dictionary."""
    try:
        # Decode the content bytes to get the YouTubeContent object
        content_str = entity.content.decode("utf-8")
        content_json = json.loads(content_str)

        # Extract transcript text for easier consumption by frontend
        transcript_text = ""
        if "transcript" in content_json and content_json["transcript"]:
            transcript_text = " ".join(
                [chunk.get("text", "") for chunk in content_json["transcript"]])

        # Create a simplified dictionary with the most important information
        return {
            "video_id": content_json.get("video_id", ""),
            "title": content_json.get("title", ""),
            "channel_name": content_json.get("channel_name", ""),
            "channel_id": content_json.get("channel_id", ""),
            "upload_date": content_json.get("upload_date", ""),
            "url": content_json.get("url", ""),
            "language": content_json.get("language", ""),
            "duration_seconds": content_json.get("duration_seconds", 0),
            "transcript_text": transcript_text,
            "transcript_chunks": len(content_json.get("transcript", [])),
        }
    except Exception as e:
        return {
            "error": f"Failed to convert entity to dictionary: {str(e)}",
            "uri": entity.uri
        }


async def scrape_video_async(video_id):
    """Scrape a YouTube video by ID."""
    try:
        # Create a date range that includes all videos (very wide range)
        date_range = DateRange(
            start=dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc),
            end=dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)
        )

        # Scrape the video
        entities = await scraper._scrape_video_ids([video_id], date_range)

        # Log the result
        if entities:
            print(
                f"Successfully scraped video {video_id}, got {len(entities)} entities")
        else:
            print(f"No transcript found for video {video_id}")

        return entities
    except Exception as e:
        print(f"Error scraping video {video_id}: {str(e)}")
        traceback.print_exc()

        # Check if this is a VideoUnplayable error
        error_str = str(e)
        if "VideoUnplayable" in error_str or "Video unavailable" in error_str:
            # Create a placeholder entity with basic information
            print(f"Creating placeholder for unavailable video {video_id}")

            # Create a basic placeholder entity
            placeholder_content = {
                "video_id": video_id,
                "title": f"Unavailable Video ({video_id})",
                "channel_name": "Unknown",
                "channel_id": "Unknown",
                "upload_date": dt.datetime.now().isoformat(),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "language": "unknown",
                "duration_seconds": 0,
                "transcript": [],
                "error": "Video unavailable or unplayable"
            }

            # Create a DataEntity with the placeholder content
            from common.data import DataEntity, DataLabel
            placeholder_entity = DataEntity(
                uri=f"youtube:video:{video_id}",
                label=DataLabel.YOUTUBE_TRANSCRIPT,
                content=json.dumps(placeholder_content).encode('utf-8')
            )

            return [placeholder_entity]

        # Re-raise other exceptions to be handled by the caller
        raise


async def scrape_channel_async(channel_id, max_videos=5):
    """Scrape videos from a YouTube channel by ID."""
    try:
        # Create a date range for the past year
        date_range = DateRange(
            start=dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365),
            end=dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)
        )

        # Scrape the channel
        entities = await scraper._scrape_channels([channel_id], max_videos, date_range)

        # Log the result
        if entities:
            print(
                f"Successfully scraped channel {channel_id}, got {len(entities)} entities")
        else:
            print(f"No transcripts found for channel {channel_id}")

        return entities
    except Exception as e:
        print(f"Error scraping channel {channel_id}: {str(e)}")
        traceback.print_exc()
        # Re-raise the exception to be handled by the caller
        raise


def save_transcript_to_pdf(video_data):
    """
    Save the transcript of a YouTube video to a PDF file.

    Args:
        video_data (dict): Dictionary containing video information including transcript

    Returns:
        str: Path to the saved PDF file or None if saving failed
    """
    try:
        # Create transcripts directory if it doesn't exist
        transcripts_dir = Path(os.path.join(
            os.path.dirname(__file__), '..', 'transcripts'))
        transcripts_dir.mkdir(exist_ok=True)

        # Extract video information
        video_id = video_data.get('video_id', 'unknown')
        title = video_data.get('title', 'Untitled')

        # Clean the title to make it suitable for a filename
        # Remove invalid filename characters
        clean_title = re.sub(r'[\\/*?:"<>|]', '', title)
        # Replace spaces with underscores
        clean_title = re.sub(r'\s+', '_', clean_title)

        # Create a timestamp
        timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create the filename
        filename = f"{clean_title}-{timestamp}-{video_id}.pdf"
        filepath = transcripts_dir / filename

        # Get the transcript text
        transcript_text = video_data.get('transcript_text', '')

        if not transcript_text:
            print(f"No transcript available for video: {title} ({video_id})")

            # Create a PDF with metadata but note that transcript is unavailable
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            # Get styles
            styles = getSampleStyleSheet()
            title_style = styles['Title']
            heading_style = styles['Heading2']
            normal_style = styles['Normal']
            warning_style = ParagraphStyle(
                'WarningStyle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.red,
                spaceAfter=12
            )

            # Create document elements
            elements = []

            # Add title
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 0.25 * inch))

            # Add metadata table
            metadata = [
                ["Video ID:", video_id],
                ["URL:", video_data.get('url', '')],
                ["Channel:", video_data.get('channel_name', '')],
                ["Upload Date:", video_data.get('upload_date', '')],
                ["Duration:",
                    f"{video_data.get('duration_seconds', 0)} seconds"]
            ]

            # Create the table with metadata
            metadata_table = Table(metadata, colWidths=[1.5*inch, 4*inch])
            metadata_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))

            elements.append(metadata_table)
            elements.append(Spacer(1, 0.5 * inch))

            # Add warning about missing transcript
            elements.append(
                Paragraph("NO TRANSCRIPT AVAILABLE", warning_style))
            elements.append(Paragraph("This could be because:", normal_style))
            elements.append(
                Paragraph("1. The video owner has disabled transcripts", normal_style))
            elements.append(
                Paragraph("2. The video is not available or has been removed", normal_style))
            elements.append(Paragraph(
                "3. YouTube does not have automatic captions for this video", normal_style))

            # Build the PDF
            doc.build(elements)

            print(f"Info PDF without transcript saved to: {filepath}")
            return str(filepath)

        # Create a PDF document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Get styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']

        # Create a custom style for metadata
        metadata_style = ParagraphStyle(
            'MetadataStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )

        # Create document elements
        elements = []

        # Add title
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.25 * inch))

        # Add metadata table
        metadata = [
            ["Video ID:", video_id],
            ["URL:", video_data.get('url', '')],
            ["Channel:", video_data.get('channel_name', '')],
            ["Upload Date:", video_data.get('upload_date', '')],
            ["Duration:", f"{video_data.get('duration_seconds', 0)} seconds"]
        ]

        # Create the table with metadata
        metadata_table = Table(metadata, colWidths=[1.5*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        elements.append(metadata_table)
        elements.append(Spacer(1, 0.5 * inch))

        # Add transcript heading
        elements.append(Paragraph("TRANSCRIPT", heading_style))
        elements.append(Spacer(1, 0.25 * inch))

        # Add transcript text - split into paragraphs for better formatting
        paragraphs = transcript_text.split('\n\n')
        for para in paragraphs:
            if para.strip():
                elements.append(
                    Paragraph(para.replace('\n', '<br/>'), normal_style))
                elements.append(Spacer(1, 0.1 * inch))

        # Build the PDF
        doc.build(elements)

        print(f"Transcript PDF saved to: {filepath}")
        return str(filepath)

    except Exception as e:
        print(f"Error saving transcript to PDF: {str(e)}")
        traceback.print_exc()
        return None


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
        transcripts_dir = Path(os.path.join(
            os.path.dirname(__file__), '..', 'transcripts'))
        transcripts_dir.mkdir(exist_ok=True)

        # Extract video information
        video_id = video_data.get('video_id', 'unknown')
        title = video_data.get('title', 'Untitled')

        # Clean the title to make it suitable for a filename
        # Remove invalid filename characters
        clean_title = re.sub(r'[\\/*?:"<>|]', '', title)
        # Replace spaces with underscores
        clean_title = re.sub(r'\s+', '_', clean_title)

        # Create a timestamp
        timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create the filename
        filename = f"{clean_title}-{timestamp}-{video_id}.txt"
        filepath = transcripts_dir / filename

        # Get the transcript text
        transcript_text = video_data.get('transcript_text', '')

        if not transcript_text:
            print(f"No transcript available for video: {title} ({video_id})")

            # Create a file with metadata but note that transcript is unavailable
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write video metadata
                f.write(f"Title: {title}\n")
                f.write(f"Video ID: {video_id}\n")
                f.write(f"URL: {video_data.get('url', '')}\n")
                f.write(f"Channel: {video_data.get('channel_name', '')}\n")
                f.write(f"Upload Date: {video_data.get('upload_date', '')}\n")
                f.write(
                    f"Duration: {video_data.get('duration_seconds', 0)} seconds\n")
                f.write("\n" + "="*50 + "\n\n")
                f.write("NO TRANSCRIPT AVAILABLE FOR THIS VIDEO\n")
                f.write("This could be because:\n")
                f.write("1. The video owner has disabled transcripts\n")
                f.write("2. The video is not available or has been removed\n")
                f.write(
                    "3. YouTube does not have automatic captions for this video\n")

            print(f"Created info file without transcript: {filepath}")
            return str(filepath)

        # Write the transcript to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"URL: {video_data.get('url', '')}\n")
            f.write(f"Channel: {video_data.get('channel_name', '')}\n")
            f.write(f"Upload Date: {video_data.get('upload_date', '')}\n")
            f.write(
                f"Duration: {video_data.get('duration_seconds', 0)} seconds\n")
            f.write("\n" + "="*50 + "\n\nTRANSCRIPT:\n\n" + "="*50 + "\n\n")
            f.write(transcript_text)

        print(f"Transcript saved to: {filepath}")
        return str(filepath)

    except Exception as e:
        print(f"Error saving transcript: {str(e)}")
        traceback.print_exc()
        return None


def run_scrape_job(job_type, identifier, max_videos=5):
    """Run a scraping job in a background thread."""
    global last_job_status, last_job_result, current_job

    last_job_status = "running"
    last_job_result = None

    try:
        # Create an event loop for the thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if job_type == "video":
            # Scrape a video
            entities = loop.run_until_complete(scrape_video_async(identifier))
        elif job_type == "channel":
            # Scrape a channel
            entities = loop.run_until_complete(
                scrape_channel_async(identifier, max_videos))
        else:
            raise ValueError(f"Unknown job type: {job_type}")

        # Check if we got any results
        if not entities:
            last_job_status = "completed_with_warnings"
            last_job_result = {
                "job_type": job_type,
                "identifier": identifier,
                "count": 0,
                "data": [],
                "warning": "No transcripts found. This could be because the video is unavailable, has no transcript, or the transcript is disabled.",
                "saved_transcript_files": [],
                "saved_pdf_files": []
            }
            current_job = None
            return

        # Convert entities to dictionaries
        results = [entity_to_dict(entity) for entity in entities]

        # Check if we have placeholder entities for unavailable videos
        for result in results:
            if "error" in result and "Video unavailable" in result.get("error", ""):
                print(
                    f"Processing placeholder for unavailable video: {result.get('video_id')}")

                # Create basic video info for the placeholder
                result["title"] = f"Unavailable Video ({result.get('video_id')})"
                result["transcript_text"] = "This video is unavailable or cannot be played."

        # Save transcripts to files (both text and PDF)
        saved_files = []
        saved_pdf_files = []
        for result in results:
            # Save as text file
            file_path = save_transcript_to_file(result)
            if file_path:
                result['transcript_file'] = file_path
                saved_files.append(file_path)

            # Save as PDF file
            pdf_path = save_transcript_to_pdf(result)
            if pdf_path:
                result['transcript_pdf_file'] = pdf_path
                saved_pdf_files.append(pdf_path)

        last_job_result = {
            "job_type": job_type,
            "identifier": identifier,
            "count": len(results),
            "data": results,
            "saved_transcript_files": saved_files,
            "saved_pdf_files": saved_pdf_files
        }
        last_job_status = "completed"

    except Exception as e:
        error_message = str(e)
        error_traceback = traceback.format_exc()

        # Check for common YouTube transcript API errors
        if "VideoUnplayable" in error_traceback:
            last_job_status = "completed_with_error"
            last_job_result = {
                "job_type": job_type,
                "identifier": identifier,
                "error": "The video is unavailable or cannot be played.",
                "details": error_message,
                "suggestion": "Please check if the video ID is correct and the video is publicly available."
            }
        elif "TranscriptsDisabled" in error_traceback:
            last_job_status = "completed_with_error"
            last_job_result = {
                "job_type": job_type,
                "identifier": identifier,
                "error": "Transcripts are disabled for this video.",
                "details": error_message,
                "suggestion": "Try a different video that has transcripts enabled."
            }
        elif "NoTranscriptFound" in error_traceback:
            last_job_status = "completed_with_error"
            last_job_result = {
                "job_type": job_type,
                "identifier": identifier,
                "error": "No transcript found for this video.",
                "details": error_message,
                "suggestion": "Try a different video that has transcripts available."
            }
        else:
            last_job_status = "failed"
            last_job_result = {
                "job_type": job_type,
                "identifier": identifier,
                "error": error_message,
                "traceback": error_traceback
            }
    finally:
        current_job = None

# API Routes


@app.route("/", methods=["GET"])
def index():
    """Return basic information about the API."""
    return jsonify({
        "name": "YouTube Transcript Scraper API",
        "version": "1.0.0",
        "description": "API for scraping YouTube video transcripts and saving them as text and PDF files",
        "endpoints": {
            "POST /api/scrape/video": "Scrape a YouTube video by ID",
            "POST /api/scrape/channel": "Scrape videos from a YouTube channel by ID",
            "GET /api/scrape/status": "Get the status of the current or last scraping job",
            "GET /api/scrape/result": "Get the result of the last completed scraping job",
            "GET /api/download/text/{video_id}": "Download the transcript text file for a specific video",
            "GET /api/download/pdf/{video_id}": "Download the transcript PDF file for a specific video"
        }
    })


@app.route("/api/scrape/video", methods=["POST"])
def scrape_video():
    """Endpoint to scrape a YouTube video by ID."""
    global current_job

    # Check API key if configured
    if API_KEY and request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # Get video ID from request
    data = request.get_json()
    if not data or "video_id" not in data:
        return jsonify({"error": "Missing video_id parameter"}), 400

    video_id = data["video_id"].strip()

    # Extract video ID if a full URL was provided
    if len(video_id) > 11 and ('youtube.com' in video_id or 'youtu.be' in video_id):
        # Try to extract the video ID from the URL
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard URLs
            # Embed/short URLs
            r'(?:embed|v|vi|youtu\.be\/)([0-9A-Za-z_-]{11}).*',
        ]

        extracted_id = None
        for pattern in patterns:
            match = re.search(pattern, video_id)
            if match:
                extracted_id = match.group(1)
                break

        if extracted_id:
            video_id = extracted_id
            print(f"Extracted video ID from URL: {video_id}")
        else:
            return jsonify({"error": "Could not extract a valid video ID from the provided URL"}), 400

    # Validate video ID format (basic check)
    if not video_id or len(video_id) != 11:
        return jsonify({"error": "Invalid video_id format. Expected 11-character YouTube video ID"}), 400

    # Check if a job is already running
    if current_job:
        return jsonify({
            "status": "error",
            "message": "Another job is already running",
            "current_job": current_job
        }), 409

    # Start scraping in a background thread
    current_job = {"type": "video", "id": video_id}
    threading.Thread(
        target=run_scrape_job,
        args=("video", video_id),
        daemon=True
    ).start()

    return jsonify({
        "status": "started",
        "job_type": "video",
        "video_id": video_id
    }), 202


@app.route("/api/scrape/channel", methods=["POST"])
def scrape_channel():
    """Endpoint to scrape videos from a YouTube channel by ID."""
    global current_job

    # Check API key if configured
    if API_KEY and request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # Get channel ID from request
    data = request.get_json()
    if not data or "channel_id" not in data:
        return jsonify({"error": "Missing channel_id parameter"}), 400

    channel_id = data["channel_id"].strip()
    max_videos = int(data.get("max_videos", 5))

    # Limit max_videos to a reasonable range
    max_videos = max(1, min(10, max_videos))

    # Validate channel ID format (basic check)
    if not channel_id or len(channel_id) < 10:
        return jsonify({"error": "Invalid channel_id format. Expected YouTube channel ID"}), 400

    # Check if a job is already running
    if current_job:
        return jsonify({
            "status": "error",
            "message": "Another job is already running",
            "current_job": current_job
        }), 409

    # Start scraping in a background thread
    current_job = {"type": "channel",
                   "id": channel_id, "max_videos": max_videos}
    threading.Thread(
        target=run_scrape_job,
        args=("channel", channel_id, max_videos),
        daemon=True
    ).start()

    return jsonify({
        "status": "started",
        "job_type": "channel",
        "channel_id": channel_id,
        "max_videos": max_videos
    }), 202


@app.route("/api/scrape/status", methods=["GET"])
def get_status():
    """Get the status of the current or last scraping job."""
    # Check API key if configured
    if API_KEY and request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "status": last_job_status,
        "current_job": current_job
    })


@app.route("/api/scrape/result", methods=["GET"])
def get_result():
    """Get the result of the last completed scraping job."""
    # Check API key if configured
    if API_KEY and request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    if last_job_result is None:
        return jsonify({
            "status": last_job_status,
            "message": "No results available yet"
        })

    # Add download URLs to the results
    result_with_downloads = last_job_result.copy()

    if "data" in result_with_downloads:
        for item in result_with_downloads["data"]:
            video_id = item.get("video_id", "")
            if video_id:
                # Add download URLs
                item["text_download_url"] = f"/api/download/text/{video_id}"
                item["pdf_download_url"] = f"/api/download/pdf/{video_id}"

    return jsonify({
        "status": last_job_status,
        "result": result_with_downloads
    })


@app.route("/api/download/text/<video_id>", methods=["GET"])
def download_text(video_id):
    """Download the transcript text file for a specific video."""
    # Check API key if configured
    if API_KEY and request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # Find the transcript file for this video ID
    if last_job_result and "data" in last_job_result:
        for item in last_job_result["data"]:
            if item.get("video_id") == video_id:
                # Check if we have a transcript file
                if "transcript_file" in item:
                    file_path = item["transcript_file"]
                    try:
                        # Check if file exists
                        if os.path.exists(file_path):
                            # Get the filename from the path
                            filename = os.path.basename(file_path)

                            # Return the file as an attachment
                            return send_file(
                                file_path,
                                as_attachment=True,
                                download_name=filename,
                                mimetype="text/plain"
                            )
                        else:
                            return jsonify({"error": "File not found"}), 404
                    except Exception as e:
                        return jsonify({"error": f"Error downloading file: {str(e)}"}), 500
                else:
                    # If we don't have a transcript file but have video info, create one on-the-fly
                    try:
                        # Create transcripts directory if it doesn't exist
                        transcripts_dir = Path(os.path.join(
                            os.path.dirname(__file__), '..', 'transcripts'))
                        transcripts_dir.mkdir(exist_ok=True)

                        # Create a filename
                        title = item.get('title', 'Untitled')
                        clean_title = re.sub(r'[\\/*?:"<>|]', '', title)
                        clean_title = re.sub(r'\s+', '_', clean_title)
                        timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{clean_title}-{timestamp}-{video_id}.txt"
                        filepath = transcripts_dir / filename

                        # Create a file with metadata and error message
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(f"Title: {title}\n")
                            f.write(f"Video ID: {video_id}\n")
                            f.write(f"URL: {item.get('url', '')}\n")
                            f.write(
                                f"Channel: {item.get('channel_name', '')}\n")
                            f.write(
                                f"Upload Date: {item.get('upload_date', '')}\n")
                            f.write(
                                f"Duration: {item.get('duration_seconds', 0)} seconds\n")
                            f.write("\n" + "="*50 + "\n\n")

                            if "error" in item:
                                f.write(f"ERROR: {item['error']}\n\n")
                                f.write(
                                    "This video is unavailable or cannot be played.\n")
                            else:
                                f.write(
                                    "NO TRANSCRIPT AVAILABLE FOR THIS VIDEO\n")
                                f.write("This could be because:\n")
                                f.write(
                                    "1. The video owner has disabled transcripts\n")
                                f.write(
                                    "2. The video is not available or has been removed\n")
                                f.write(
                                    "3. YouTube does not have automatic captions for this video\n")

                        # Return the file as an attachment
                        return send_file(
                            filepath,
                            as_attachment=True,
                            download_name=filename,
                            mimetype="text/plain"
                        )
                    except Exception as e:
                        return jsonify({"error": f"Error creating transcript file: {str(e)}"}), 500

    return jsonify({"error": "Transcript not found for this video ID"}), 404


@app.route("/api/download/pdf/<video_id>", methods=["GET"])
def download_pdf(video_id):
    """Download the transcript PDF file for a specific video."""
    # Check API key if configured
    if API_KEY and request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # Find the PDF file for this video ID
    if last_job_result and "data" in last_job_result:
        for item in last_job_result["data"]:
            if item.get("video_id") == video_id:
                # Check if we have a PDF file
                if "transcript_pdf_file" in item:
                    file_path = item["transcript_pdf_file"]
                    try:
                        # Check if file exists
                        if os.path.exists(file_path):
                            # Get the filename from the path
                            filename = os.path.basename(file_path)

                            # Return the file as an attachment
                            return send_file(
                                file_path,
                                as_attachment=True,
                                download_name=filename,
                                mimetype="application/pdf"
                            )
                        else:
                            return jsonify({"error": "File not found"}), 404
                    except Exception as e:
                        return jsonify({"error": f"Error downloading file: {str(e)}"}), 500
                else:
                    # If we don't have a PDF file but have video info, create one on-the-fly
                    try:
                        # Create transcripts directory if it doesn't exist
                        transcripts_dir = Path(os.path.join(
                            os.path.dirname(__file__), '..', 'transcripts'))
                        transcripts_dir.mkdir(exist_ok=True)

                        # Create a filename
                        title = item.get('title', 'Untitled')
                        clean_title = re.sub(r'[\\/*?:"<>|]', '', title)
                        clean_title = re.sub(r'\s+', '_', clean_title)
                        timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{clean_title}-{timestamp}-{video_id}.pdf"
                        filepath = transcripts_dir / filename

                        # Create a PDF document
                        doc = SimpleDocTemplate(
                            str(filepath),
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72
                        )

                        # Get styles
                        styles = getSampleStyleSheet()
                        title_style = styles['Title']
                        heading_style = styles['Heading2']
                        normal_style = styles['Normal']
                        warning_style = ParagraphStyle(
                            'WarningStyle',
                            parent=styles['Normal'],
                            fontSize=12,
                            textColor=colors.red,
                            spaceAfter=12
                        )

                        # Create document elements
                        elements = []

                        # Add title
                        elements.append(Paragraph(title, title_style))
                        elements.append(Spacer(1, 0.25 * inch))

                        # Add metadata table
                        metadata = [
                            ["Video ID:", video_id],
                            ["URL:", item.get('url', '')],
                            ["Channel:", item.get('channel_name', '')],
                            ["Upload Date:", item.get('upload_date', '')],
                            ["Duration:",
                                f"{item.get('duration_seconds', 0)} seconds"]
                        ]

                        # Create the table with metadata
                        metadata_table = Table(
                            metadata, colWidths=[1.5*inch, 4*inch])
                        metadata_table.setStyle(TableStyle([
                            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 0), (-1, -1), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ]))

                        elements.append(metadata_table)
                        elements.append(Spacer(1, 0.5 * inch))

                        # Add warning about missing transcript
                        if "error" in item:
                            elements.append(
                                Paragraph("ERROR: VIDEO UNAVAILABLE", warning_style))
                            elements.append(Paragraph(item.get(
                                'error', 'This video is unavailable or cannot be played.'), normal_style))
                        else:
                            elements.append(
                                Paragraph("NO TRANSCRIPT AVAILABLE", warning_style))
                            elements.append(
                                Paragraph("This could be because:", normal_style))
                            elements.append(
                                Paragraph("1. The video owner has disabled transcripts", normal_style))
                            elements.append(
                                Paragraph("2. The video is not available or has been removed", normal_style))
                            elements.append(Paragraph(
                                "3. YouTube does not have automatic captions for this video", normal_style))

                        # Build the PDF
                        doc.build(elements)

                        # Return the file as an attachment
                        return send_file(
                            filepath,
                            as_attachment=True,
                            download_name=filename,
                            mimetype="application/pdf"
                        )
                    except Exception as e:
                        return jsonify({"error": f"Error creating PDF file: {str(e)}"}), 500

    return jsonify({"error": "PDF not found for this video ID"}), 404

# Enable CORS for all routes


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-API-KEY'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

# Handle OPTIONS requests for CORS preflight


@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-API-KEY'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response


if __name__ == '__main__':
    # Create transcripts directory if it doesn't exist
    transcripts_dir = Path(os.path.join(
        os.path.dirname(__file__), '..', 'transcripts'))
    transcripts_dir.mkdir(exist_ok=True)
    print(f"Transcripts will be saved to: {transcripts_dir}")

    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_secret_key')
    debug_mode = os.getenv(
        'FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    port = int(os.getenv('FLASK_PORT', 5001))

    print(f"Starting YouTube Scraper API on port {port}, debug={debug_mode}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)