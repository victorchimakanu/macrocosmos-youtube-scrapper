
import { useState } from 'react';
import { motion } from 'framer-motion';
import { Download } from 'lucide-react';

/**
 * A card component to display the results of a YouTube scrape
 * 
 * @param {Object} props - Component props
 * @param {Object} props.data - The scraped data to display
 * @param {string} props.type - The type of data ('video' or 'channel')
 * @returns {JSX.Element} Formatted result card
 */
interface ResultCardProps {
  data: any;
  type: 'video' | 'channel';
}

const ResultCard = ({ data, type }: ResultCardProps) => {
  const [expanded, setExpanded] = useState(false);
  const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:5000';

  // Format video data for display with new requirements
  const formatVideoData = () => {
    const {
      title,
      video_id,
      channel_name,
      views,
      likes,
      comment_count,
      published_date,
      description,
      thumbnail,
      duration,
      url,
      ...rest
    } = data;

    // Function to download transcript as PDF
    const handleDownloadTranscript = () => {
      if (!video_id) return;
      
      // Create the download URL using the backend API
      const downloadUrl = `${API_BASE}/api/download/pdf/${video_id}`;
      
      // Open the URL in a new tab or trigger download
      window.open(downloadUrl, '_blank');
    };

    return (
      <div>
        {thumbnail && (
          <div className="mb-4">
            <img
              src={thumbnail}
              alt={title || "Video thumbnail"}
              className="w-full h-auto rounded-lg"
            />
          </div>
        )}

        <h2 className="text-xl font-bold mb-3">{title || "Untitled Video"}</h2>
        
        {/* Key Video Info Section */}
        <div className="space-y-3 mb-5 bg-gray-50 p-4 rounded-lg border border-[#C2B8BE]/30">
          {video_id && (
            <div className="flex flex-wrap">
              <span className="font-medium w-32 text-[#404059]">Video ID:</span>
              <span className="text-gray-700 break-all">{video_id}</span>
            </div>
          )}
          
          {url && (
            <div className="flex flex-wrap">
              <span className="font-medium w-32 text-[#404059]">Video URL:</span>
              <a 
                href={url} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-blue-600 hover:underline break-all"
              >
                {url}
              </a>
            </div>
          )}
          
          {channel_name && (
            <div className="flex flex-wrap">
              <span className="font-medium w-32 text-[#404059]">Channel:</span>
              <span className="text-gray-700">{channel_name}</span>
            </div>
          )}
          
          {duration && (
            <div className="flex flex-wrap">
              <span className="font-medium w-32 text-[#404059]">Duration:</span>
              <span className="text-gray-700">{duration}</span>
            </div>
          )}
        </div>
        
        {/* Download Transcript Button */}
        {video_id && (
          <div className="mb-5">
            <motion.button
              onClick={handleDownloadTranscript}
              className="w-full sm:w-auto bg-[#404059] hover:bg-[#E34C4E] text-white px-4 py-3 rounded-md font-medium transition-all flex items-center justify-center"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              animate={{
                boxShadow: ["0px 0px 0px rgba(64, 64, 89, 0)", "0px 0px 8px rgba(64, 64, 89, 0.5)", "0px 0px 0px rgba(64, 64, 89, 0)"],
              }}
              transition={{
                boxShadow: {
                  repeat: Infinity,
                  duration: 2.5,
                }
              }}
            >
              <Download className="h-5 w-5 mr-2" />
              Download Transcript
            </motion.button>
          </div>
        )}
        
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-4">
          {views !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-sm text-gray-500">Views</p>
              <p className="font-semibold">{formatNumber(views)}</p>
            </div>
          )}
          
          {likes !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-sm text-gray-500">Likes</p>
              <p className="font-semibold">{formatNumber(likes)}</p>
            </div>
          )}
          
          {comment_count !== undefined && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-sm text-gray-500">Comments</p>
              <p className="font-semibold">{formatNumber(comment_count)}</p>
            </div>
          )}
          
          {published_date && (
            <div className="bg-gray-50 p-3 rounded">
              <p className="text-sm text-gray-500">Published</p>
              <p className="font-semibold">{published_date}</p>
            </div>
          )}
        </div>
        
        {description && (
          <div className="mt-4">
            <h3 className="font-medium mb-2">Description</h3>
            <p className={`text-gray-700 whitespace-pre-line ${!expanded && 'line-clamp-3'}`}>
              {description}
            </p>
            {description.split('\n').length > 3 && (
              <button
                onClick={() => setExpanded(!expanded)}
                className="text-blue-600 hover:text-blue-800 text-sm mt-1 focus:outline-none"
              >
                {expanded ? 'Show less' : 'Read more'}
              </button>
            )}
          </div>
        )}
        
        {/* Show additional data if available */}
        {Object.keys(rest).length > 0 && (
          <div className="mt-6 border-t pt-4">
            <button
              onClick={() => setExpanded(!expanded)}
              className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
            >
              {expanded ? 'Hide' : 'Show'} additional data
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className={`h-4 w-4 ml-1 transform ${expanded ? 'rotate-180' : ''}`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
            
            {expanded && (
              <div className="mt-3 grid gap-2 text-sm">
                {Object.entries(rest).map(([key, value]) => (
                  <div key={key} className="flex">
                    <span className="font-medium w-1/3">{formatKey(key)}:</span>
                    <span className="w-2/3">
                      {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  // Format channel data for display
  const formatChannelData = () => {
    const {
      channel_name,
      subscribers,
      total_videos,
      join_date,
      description,
      profile_picture,
      banner_image,
      recent_videos,
      ...rest
    } = data;

    return (
      <div>
        {banner_image && (
          <div className="mb-4 rounded-lg overflow-hidden h-32 sm:h-40 relative">
            <img
              src={banner_image}
              alt="Channel banner"
              className="w-full h-full object-cover"
            />
          </div>
        )}
        
        <div className="flex flex-col sm:flex-row sm:items-center mb-6">
          {profile_picture && (
            <div className="mb-4 sm:mb-0 sm:mr-4">
              <img
                src={profile_picture}
                alt="Channel profile"
                className="w-16 h-16 sm:w-20 sm:h-20 rounded-full border-2 border-white shadow-md"
              />
            </div>
          )}
          
          <div>
            <h2 className="text-xl font-bold">{channel_name || "Untitled Channel"}</h2>
            
            <div className="flex flex-wrap gap-x-4 gap-y-2 mt-2 text-sm text-gray-600">
              {subscribers !== undefined && (
                <p>
                  <span className="font-medium">{formatNumber(subscribers)}</span> subscribers
                </p>
              )}
              {total_videos !== undefined && (
                <p>
                  <span className="font-medium">{formatNumber(total_videos)}</span> videos
                </p>
              )}
              {join_date && (
                <p>Joined {join_date}</p>
              )}
            </div>
          </div>
        </div>
        
        {description && (
          <div className="mt-4">
            <h3 className="font-medium mb-2">Description</h3>
            <p className={`text-gray-700 whitespace-pre-line ${!expanded && 'line-clamp-3'}`}>
              {description}
            </p>
            {description.split('\n').length > 3 && (
              <button
                onClick={() => setExpanded(!expanded)}
                className="text-blue-600 hover:text-blue-800 text-sm mt-1 focus:outline-none"
              >
                {expanded ? 'Show less' : 'Read more'}
              </button>
            )}
          </div>
        )}
        
        {recent_videos && recent_videos.length > 0 && (
          <div className="mt-6">
            <h3 className="font-medium mb-3">Recent Videos</h3>
            <div className="space-y-3">
              {recent_videos.slice(0, expanded ? undefined : 3).map((video: any, index: number) => (
                <div key={index} className="bg-gray-50 p-3 rounded hover:bg-gray-100 transition-colors">
                  <p className="font-medium">{video.title}</p>
                  <div className="flex gap-x-4 text-sm text-gray-600 mt-1">
                    {video.views !== undefined && (
                      <p>{formatNumber(video.views)} views</p>
                    )}
                    {video.published && (
                      <p>{video.published}</p>
                    )}
                  </div>
                </div>
              ))}
              
              {recent_videos.length > 3 && (
                <button
                  onClick={() => setExpanded(!expanded)}
                  className="text-blue-600 hover:text-blue-800 text-sm mt-1 focus:outline-none"
                >
                  {expanded ? 'Show less' : `Show ${recent_videos.length - 3} more videos`}
                </button>
              )}
            </div>
          </div>
        )}
        
        {/* Show additional data if available */}
        {Object.keys(rest).length > 0 && (
          <div className="mt-6 border-t pt-4">
            <button
              onClick={() => setExpanded(!expanded)}
              className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
            >
              {expanded ? 'Hide' : 'Show'} additional data
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className={`h-4 w-4 ml-1 transform ${expanded ? 'rotate-180' : ''}`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
            
            {expanded && (
              <div className="mt-3 grid gap-2 text-sm">
                {Object.entries(rest).map(([key, value]) => (
                  <div key={key} className="flex">
                    <span className="font-medium w-1/3">{formatKey(key)}:</span>
                    <span className="w-2/3">
                      {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  // Format numbers for display (e.g., 1000 -> 1K)
  const formatNumber = (num: number): string => {
    if (!num && num !== 0) return 'N/A';
    if (num === 0) return '0';
    
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  // Format API keys to be more readable
  const formatKey = (key: string): string => {
    return key
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <motion.div 
      className="bg-white rounded-lg shadow-md p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", damping: 12 }}
    >
      {type === 'video' ? formatVideoData() : formatChannelData()}
    </motion.div>
  );
};

export default ResultCard;
