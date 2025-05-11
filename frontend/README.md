
# Macrocosmos YouTube Scraper

A production-ready frontend application for scraping YouTube video and channel data. This application connects to the Macrocosmos YouTube Scraper API to extract valuable information from YouTube videos and channels.

## Features

- **Video Scraping**: Extract data from any YouTube video
- **Channel Scraping**: Extract data from any YouTube channel
- **Responsive Design**: Works on all device sizes
- **Error Handling**: Graceful error handling and user feedback
- **Loading States**: Visual feedback during API requests

## Tech Stack

- React with Vite
- TypeScript
- Tailwind CSS
- Axios for HTTP requests

## Getting Started

### Prerequisites

- Node.js (v14+)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/macrocosmos-youtube-scraper.git
cd macrocosmos-youtube-scraper
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory with the following variables:
```
VITE_API_BASE=https://macrocosmos-youtube-scraper.onrender.com
VITE_API_KEY=your_api_key_here
```

4. Start the development server:
```bash
npm run dev
```

The app will be available at http://localhost:5173 (or another port if 5173 is in use).

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE` | Base URL for the backend API | https://macrocosmos-youtube-scraper.onrender.com |
| `VITE_API_KEY` | API key for authentication | (Required, no default) |

## Building for Production

To create a production build:

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Deployment

You can deploy this application on any static hosting service like Netlify, Vercel, or GitHub Pages.

### Deploying to Netlify

1. Connect your repository to Netlify
2. Set the build command to `npm run build`
3. Set the publish directory to `dist`
4. Add the environment variables (`VITE_API_BASE` and `VITE_API_KEY`)

### Deploying to Vercel

1. Connect your repository to Vercel
2. Set the Framework Preset to "Vite"
3. Add the environment variables (`VITE_API_BASE` and `VITE_API_KEY`)

## Project Structure

```
src/
├── api.ts           # Axios setup + API functions
├── components/      # Reusable components
│   ├── ApiKeyBanner.tsx  # Warning for missing API key
│   ├── ChannelForm.tsx   # Channel scraping form
│   ├── ErrorAlert.tsx    # Error display component
│   ├── ResultCard.tsx    # Displays scraping results
│   ├── Spinner.tsx       # Loading indicator
│   └── VideoForm.tsx     # Video scraping form
└── pages/
    └── Index.tsx    # Main application page
```

## API Documentation

The application connects to the Macrocosmos YouTube Scraper API at `https://macrocosmos-youtube-scraper.onrender.com`. The API requires authentication using an API key passed in the `X-Api-Key` header.

### Available Endpoints

#### Video Scraping

```
POST /scrape/video
Content-Type: application/json
X-Api-Key: your_api_key

{
  "video_id": "dQw4w9WgXcQ"
}
```

#### Channel Scraping

```
POST /scrape/channel
Content-Type: application/json
X-Api-Key: your_api_key

{
  "channel_id": "UCsBjURrPoezykLs9EqgamOA"
}
```

## License

[MIT](LICENSE)
