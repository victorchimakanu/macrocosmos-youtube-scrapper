# Macrocosmos YouTube Scraper Backend

A Flask-based microservice that exposes HTTP endpoints to scrape YouTube video and channel metadata via the YouTube Data API. Designed for easy deployment (e.g. on Render) and secure API-key-protected access.

---

## 🔍 Features

- **`POST /scrape/video`**  
  Scrape metadata for a single YouTube video ID.  
- **`POST /scrape/channel`**  
  Scrape metadata (and video list) for a YouTube channel ID.  
- **API-Key Authentication**  
  All endpoints require a custom header `X-Api-Key` to protect access.  
- **No Database**  
  Returns JSON directly; no external persistence required.  
- **Ready for Render Deployment**  
  Includes `requirements.txt`, `Procfile`, and optional `render.yaml`.

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)  
2. [Prerequisites](#prerequisites)  
3. [Installation & Configuration](#installation--configuration)  
4. [Environment Variables](#environment-variables)  
5. [Running Locally](#running-locally)  
6. [API Reference](#api-reference)  
   - [Authentication](#authentication)  
   - [`POST /scrape/video`](#post-scrapevideo)  
   - [`POST /scrape/channel`](#post-scrapechannel)  
7. [Error Handling](#error-handling)  
8. [Deployment to Render](#deployment-to-render)  
9. [Folder Structure](#folder-structure)  
10. [Contributing](#contributing)  
11. [License](#license)

---

## 🏁 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10+  
- Git  
- A [Google YouTube Data API v3 key](https://console.developers.google.com/apis/credentials)  
- An **API key** of your own to protect the scraper endpoints  

---

## ⚙️ Installation & Configuration

1. **Clone the repository**  
   ```bash
   git clone https://github.com/macrocosm-os/data-universe.git
   cd data-universe


2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows PowerShell
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a file named `.env` in the project root (or export in your shell):

   ```ini
   YOUTUBE_API_KEY=YOUR_GOOGLE_YT_API_KEY
   API_KEY=YOUR_CUSTOM_API_KEY
   FLASK_ENV=development       # optional: enables debug mode
   FLASK_APP=app.py
   ```

   If you use `python-dotenv`, these variables will be loaded automatically.

---

## 🔑 Environment Variables

| Variable          | Description                                       | Required |
| ----------------- | ------------------------------------------------- | :------: |
| `YOUTUBE_API_KEY` | Your Google YouTube Data API v3 key               |    Yes   |
| `API_KEY`         | Custom key for securing `/scrape/*` endpoints     |    Yes   |
| `FLASK_ENV`       | Flask environment (`development` or `production`) |    No    |
| `FLASK_APP`       | Point to the Flask application entry (`app.py`)   |    No    |

---

## ▶️ Running Locally

1. **Start Flask’s development server**

   ```bash
   flask run
   ```

   By default, it listens on `http://127.0.0.1:5000`.

2. **Or use Gunicorn** (mimics production)

   ```bash
   gunicorn app:app --reload
   ```

   This launches on port 8000 by default.

---

## 📖 API Reference

### Authentication

All requests **must** include the header:

```
X-Api-Key: <YOUR_CUSTOM_API_KEY>
```

Omitting or supplying a wrong key returns **401 Unauthorized**.

---

### `POST /scrape/video`

Scrape metadata for a single YouTube video.

* **URL:** `/scrape/video`
* **Method:** `POST`
* **Headers:**

  * `Content-Type: application/json`
  * `X-Api-Key: your_api_key_here`
* **Body:**

  ```json
  {
    "video_id": "dQw4w9WgXcQ"
  }
  ```
* **Success Response (200):**

  ```json
  {
    "title": "Never Gonna Give You Up",
    "description": "...",
    "views": "1000000",
    "likes": "900000",
    "comments": "50000",
    "published_at": "2009-10-25T06:57:33Z"
  }
  ```
* **Error Responses:**

  * `400 Bad Request` – missing `video_id`
  * `401 Unauthorized` – invalid or missing API key
  * `500 Internal Server Error` – YouTube API failure

---

### `POST /scrape/channel`

Scrape metadata and video list for a YouTube channel.

* **URL:** `/scrape/channel`
* **Method:** `POST`
* **Headers:**

  * `Content-Type: application/json`
  * `X-Api-Key: your_api_key_here`
* **Body:**

  ```json
  {
    "channel_id": "UC38IQsAvIsxxjztdMZQtwHA"
  }
  ```
* **Success Response (200):**

  ```json
  {
    "channel_name": "Example Channel",
    "subscribers": "2.3M",
    "total_views": "150000000",
    "videos": [
      {
        "video_id": "abc123",
        "title": "...",
        "views": "10000",
        // ...
      },
      // ...
    ]
  }
  ```
* **Error Responses:**

  * `400 Bad Request` – missing `channel_id`
  * `401 Unauthorized` – invalid or missing API key
  * `500 Internal Server Error` – YouTube API failure

---

## ⚠️ Error Handling

* **401 Unauthorized**

  ```json
  { "error": "Unauthorized" }
  ```
* **400 Bad Request**

  ```json
  { "error": "Missing video_id" }
  ```
* **500 Internal Server Error**

  ```json
  { "error": "Internal server error. Please try again later." }
  ```

---

## 🚢 Deployment to Render

1. **Push** your updated code to GitHub.
2. **Create** a new **Web Service** on Render:

   * **Environment:** Python 3
   * **Build Command:**

     ```
     pip install --upgrade pip
     pip install -r requirements.txt
     ```
   * **Start Command:**

     ```
     gunicorn app:app
     ```
3. **Configure Environment Variables** in Render Dashboard:

   * `YOUTUBE_API_KEY`
   * `API_KEY`
   * `FLASK_ENV=production`
4. Render will automatically build, deploy, and assign a public URL (e.g. `https://macrocosmos-youtube-scraper.onrender.com`).

(Optional) You may include a `render.yaml` to codify these settings:

```yaml
services:
  - type: web
    name: youtube-scraper
    env: python
    branch: main
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: YOUTUBE_API_KEY
      - key: API_KEY
      - key: FLASK_ENV
```

---

## 📁 Folder Structure

```
data-universe/
├── app.py               # Flask application entrypoint
├── requirements.txt     # Python dependencies
├── Procfile             # For Heroku/Render startup
├── render.yaml          # Render IaC blueprint (optional)
├── .env.example         # Example environment variables
└── scraping/
    └── youtube/
        └── youtube_custom_scraper.py  # Refactored CLI logic as functions
```

---

## 🤝 Contributing

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add ..."`
4. Push to origin: `git push origin feature/your-feature`
5. Open a Pull Request — we’ll review and merge.

Please follow conventional commits and run existing linters/tests before submitting.

---

## 📜 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

*Built with 💜 by the Daniel Dohou*

