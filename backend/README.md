# YouTube Scraper API

A Flask-based API for scraping YouTube videos and channels. This API allows you to extract video metadata and transcripts from YouTube videos by providing either a video ID or a channel ID.

## Features

- Scrape a single YouTube video by ID
- Scrape multiple videos from a YouTube channel by ID
- Extract video metadata (title, channel, upload date, etc.)
- Extract video transcripts
- Automatically save transcripts to both text and PDF files
- Asynchronous processing with status updates
- CORS support for frontend integration

## Prerequisites

- Python 3.7+
- Flask
- YouTube Transcript API
- Google API Client (for YouTube Data API)

## Environment Variables

The following environment variables can be set to configure the API:

- `YOUTUBE_API_KEY`: Your YouTube Data API key (required for channel scraping)
- `API_KEY`: Optional API key for securing the endpoints
- `FLASK_SECRET_KEY`: Secret key for Flask (default: 'dev_secret_key')
- `FLASK_DEBUG`: Set to 'true' to enable debug mode (default: 'False')
- `FLASK_PORT`: Port to run the API on (default: 5000)

## API Endpoints

### Scrape a YouTube Video

```
POST /api/scrape/video
```

Request body:

```json
{
  "video_id": "dQw4w9WgXcQ"
}
```

### Scrape a YouTube Channel

```
POST /api/scrape/channel
```

Request body:

```json
{
  "channel_id": "UCAuUUnT6oDeKwE6v1NGQxug",
  "max_videos": 5
}
```

### Get Scraping Status

```
GET /api/scrape/status
```

### Get Scraping Results

```
GET /api/scrape/result
```

## Transcript Files

When you scrape a YouTube video or channel, the API automatically saves the transcripts to both text and PDF files in the `transcripts` directory.

### Text Files

Text files are named using the following format:

```text
VideoTitle-Timestamp-VideoID.txt
```

For example:

```text
Rick_Astley_-_Never_Gonna_Give_You_Up-20250509_135421-dQw4w9WgXcQ.txt
```

Each text file contains:

- Video metadata (title, channel, upload date, etc.)
- The complete transcript text

### PDF Files

PDF files are named using the following format:

```text
VideoTitle-Timestamp-VideoID.pdf
```

For example:

```text
Rick_Astley_-_Never_Gonna_Give_You_Up-20250509_135421-dQw4w9WgXcQ.pdf
```

Each PDF file contains:

- A formatted title
- Video metadata in a table format
- The complete transcript text with proper formatting and pagination

## Running the API

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set the required environment variables:

   ```bash
   export YOUTUBE_API_KEY=your_youtube_api_key
   ```

3. Run the Flask app:
   ```bash
   python backend/app.py
   ```

The API will create a `transcripts` directory if it doesn't exist and will save all transcripts there.

## Testing

You can use the included test script to test the API:

```bash
# Test scraping a video
python backend/test_app.py video dQw4w9WgXcQ

# Test scraping a channel (with max 3 videos)
python backend/test_app.py channel UCAuUUnT6oDeKwE6v1NGQxug 3
```

## Example Response

```json
{
  "status": "completed",
  "result": {
    "job_type": "video",
    "identifier": "dQw4w9WgXcQ",
    "count": 1,
    "data": [
      {
        "video_id": "dQw4w9WgXcQ",
        "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
        "channel_name": "Rick Astley",
        "channel_id": "UCuAXFkgsw1L7xaCfnd5JJOw",
        "upload_date": "2009-10-25T06:57:33+00:00",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "language": "en",
        "duration_seconds": 212,
        "transcript_text": "We're no strangers to love...",
        "transcript_chunks": 15,
        "transcript_file": "/path/to/transcripts/Rick_Astley_-_Never_Gonna_Give_You_Up-20250509_135421-dQw4w9WgXcQ.txt",
        "transcript_pdf_file": "/path/to/transcripts/Rick_Astley_-_Never_Gonna_Give_You_Up-20250509_135421-dQw4w9WgXcQ.pdf"
      }
    ],
    "saved_transcript_files": [
      "/path/to/transcripts/Rick_Astley_-_Never_Gonna_Give_You_Up-20250509_135421-dQw4w9WgXcQ.txt"
    ],
    "saved_pdf_files": [
      "/path/to/transcripts/Rick_Astley_-_Never_Gonna_Give_You_Up-20250509_135421-dQw4w9WgXcQ.pdf"
    ]
  }
}
```

## Frontend Integration

The API includes CORS support, so you can easily integrate it with a frontend application. Here's an example of how to call the API from JavaScript:

```javascript
// Scrape a video
async function scrapeVideo(videoId) {
  const response = await fetch("http://localhost:5000/api/scrape/video", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ video_id: videoId }),
  });

  return response.json();
}

// Poll for results
async function pollForResults() {
  while (true) {
    const statusResponse = await fetch(
      "http://localhost:5000/api/scrape/status"
    );
    const statusData = await statusResponse.json();

    if (statusData.status === "completed" || statusData.status === "failed") {
      const resultResponse = await fetch(
        "http://localhost:5000/api/scrape/result"
      );
      return resultResponse.json();
    }

    // Wait 2 seconds before polling again
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }
}
```
