
import { useState } from 'react';
import { scrapeVideo } from '../api';
import Spinner from './Spinner';
import ErrorAlert from './ErrorAlert';
import ResultCard from './ResultCard';
import { Search } from 'lucide-react';
import { motion } from 'framer-motion';

/**
 * Form component for scraping YouTube videos
 * 
 * Allows users to input a YouTube video URL or ID and view the scraped data
 * @returns {JSX.Element} Video scraping form component
 */
const VideoForm = () => {
  const [videoInput, setVideoInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Reset previous results and errors
    setResult(null);
    setError(null);
    
    // Validate input
    if (!videoInput.trim()) {
      setError('Please enter a YouTube video URL or ID');
      return;
    }
    
    // Start loading state
    setLoading(true);
    
    try {
      // Call API to scrape video data
      const response = await scrapeVideo(videoInput.trim());
      setResult(response.data);
    } catch (err: any) {
      // Handle errors from API or network
      console.error('Error scraping video:', err);
      const errorMessage = err.response?.data?.error || 
        err.message || 
        'An error occurred while scraping the video';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div 
      className="w-full max-w-3xl mx-auto"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <motion.form 
        onSubmit={handleSubmit} 
        className="mb-6"
        initial={{ y: 20 }}
        animate={{ y: 0 }}
        transition={{ type: "spring", stiffness: 100 }}
      >
        <div className="mb-4">
          <label htmlFor="videoInput" className="block text-sm font-medium text-[#404059] mb-1">
            YouTube Video URL or ID
          </label>
          <div className="flex flex-col sm:flex-row">
            <input
              id="videoInput"
              type="text"
              value={videoInput}
              onChange={(e) => setVideoInput(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
              className="w-full px-4 py-2 border border-[#C2B8BE] rounded-t-md sm:rounded-l-md sm:rounded-tr-none focus:ring-2 focus:ring-[#E34C4E] focus:border-[#E34C4E] focus:outline-none transition-colors mb-2 sm:mb-0"
              disabled={loading}
            />
            <motion.button
              type="submit"
              className="w-full sm:w-auto bg-[#E34C4E] hover:bg-[#404059] text-white px-4 py-2 rounded-b-md sm:rounded-r-md sm:rounded-bl-none font-medium transition-colors disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center"
              disabled={loading}
              whileHover={{ scale: 1.03, backgroundColor: "#404059" }}
              whileTap={{ scale: 0.97 }}
              animate={{
                boxShadow: loading ? "none" : ["0px 0px 0px rgba(227, 76, 78, 0)", "0px 0px 8px rgba(227, 76, 78, 0.5)", "0px 0px 0px rgba(227, 76, 78, 0)"],
              }}
              transition={{
                boxShadow: {
                  repeat: Infinity,
                  duration: 2,
                }
              }}
            >
              <Search className="h-4 w-4 mr-2" />
              Scrape Video
            </motion.button>
          </div>
          <p className="text-sm text-[#818595] mt-1">
            Enter a full YouTube video URL or just the video ID
          </p>
        </div>
      </motion.form>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
        >
          <ErrorAlert message={error} onDismiss={() => setError(null)} />
        </motion.div>
      )}
      
      {loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <Spinner />
        </motion.div>
      )}
      
      {!loading && result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ type: "spring", damping: 12 }}
        >
          <ResultCard data={result} type="video" />
        </motion.div>
      )}
    </motion.div>
  );
};

export default VideoForm;
