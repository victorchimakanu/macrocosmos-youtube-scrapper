
/**
 * API client for the Macrocosmos YouTube Scraper
 * 
 * This module provides functions to interact with the Macrocosmos YouTube Scraper API.
 * It sets up an Axios instance with the proper base URL and authentication headers.
 */

import axios from 'axios';

// Use environment variables for API configuration
const API_BASE = import.meta.env.VITE_API_BASE || 'https://macrocosmos-youtube-scraper-backend.onrender.com';
const API_KEY = import.meta.env.VITE_API_KEY || '';

// Create an axios instance with default configuration
export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
    'X-Api-Key': API_KEY,
  },
});

/**
 * Scrapes data for a YouTube video
 * 
 * @param {string} videoId - The YouTube video ID or URL
 * @returns {Promise<any>} - Promise resolving to the scraped video data
 */
export const scrapeVideo = (videoId: string) => {
  // Extract video ID if a full URL was provided
  const extractedId = extractVideoId(videoId);
  return api.post('/api/scrape/video', { video_id: extractedId });
};

/**
 * Scrapes data for a YouTube channel
 * 
 * @param {string} channelId - The YouTube channel ID or URL
 * @returns {Promise<any>} - Promise resolving to the scraped channel data
 */
export const scrapeChannel = (channelId: string) => {
  // Extract channel ID if a full URL was provided
  const extractedId = extractChannelId(channelId);
  return api.post('/api/scrape/channel', { channel_id: extractedId });
};

/**
 * Extracts a video ID from a YouTube URL or returns the ID if already in ID format
 * 
 * @param {string} videoInput - The YouTube video URL or ID
 * @returns {string} - The extracted video ID
 */
export const extractVideoId = (videoInput: string): string => {
  // Return directly if it doesn't look like a URL
  if (!videoInput.includes('youtube.com') && !videoInput.includes('youtu.be')) {
    return videoInput;
  }
  
  try {
    // For standard YouTube URLs (youtube.com/watch?v=VIDEO_ID)
    if (videoInput.includes('youtube.com/watch')) {
      const url = new URL(videoInput);
      const videoId = url.searchParams.get('v');
      if (videoId) return videoId;
    }
    
    // For shortened YouTube URLs (youtu.be/VIDEO_ID)
    if (videoInput.includes('youtu.be')) {
      const urlParts = videoInput.split('/');
      return urlParts[urlParts.length - 1].split('?')[0];
    }
    
    // If no ID found, return the original input
    return videoInput;
  } catch (error) {
    console.error('Error parsing YouTube URL:', error);
    return videoInput;
  }
};

/**
 * Extracts a channel ID from a YouTube URL or returns the ID if already in ID format
 * 
 * @param {string} channelInput - The YouTube channel URL or ID
 * @returns {string} - The extracted channel ID
 */
export const extractChannelId = (channelInput: string): string => {
  // Return directly if it doesn't look like a URL
  if (!channelInput.includes('youtube.com')) {
    return channelInput;
  }
  
  try {
    // For channel URLs (youtube.com/channel/CHANNEL_ID)
    if (channelInput.includes('/channel/')) {
      const parts = channelInput.split('/channel/');
      return parts[1].split('/')[0].split('?')[0];
    }
    
    // For custom URLs (youtube.com/c/CHANNEL_NAME)
    if (channelInput.includes('/c/') || channelInput.includes('/@')) {
      // We can only return the handle here, the API will need to handle this
      const parts = channelInput.includes('/c/') 
        ? channelInput.split('/c/') 
        : channelInput.split('/@');
      return parts[1].split('/')[0].split('?')[0];
    }
    
    // If no ID found, return the original input
    return channelInput;
  } catch (error) {
    console.error('Error parsing YouTube channel URL:', error);
    return channelInput;
  }
};
