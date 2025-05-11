
import { useState } from 'react';
import { scrapeChannel } from '../api';
import Spinner from './Spinner';
import ErrorAlert from './ErrorAlert';
import ResultCard from './ResultCard';
import { Search } from 'lucide-react';

/**
 * Form component for scraping YouTube channels
 * 
 * Allows users to input a YouTube channel URL or ID and view the scraped data
 * @returns {JSX.Element} Channel scraping form component
 */
const ChannelForm = () => {
  const [channelInput, setChannelInput] = useState('');
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
    if (!channelInput.trim()) {
      setError('Please enter a YouTube channel URL or ID');
      return;
    }
    
    // Start loading state
    setLoading(true);
    
    try {
      // Call API to scrape channel data
      const response = await scrapeChannel(channelInput.trim());
      setResult(response.data);
    } catch (err: any) {
      // Handle errors from API or network
      console.error('Error scraping channel:', err);
      const errorMessage = err.response?.data?.error || 
        err.message || 
        'An error occurred while scraping the channel';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="mb-4">
          <label htmlFor="channelInput" className="block text-sm font-medium text-[#404059] mb-1">
            YouTube Channel URL or ID
          </label>
          <div className="flex">
            <input
              id="channelInput"
              type="text"
              value={channelInput}
              onChange={(e) => setChannelInput(e.target.value)}
              placeholder="https://www.youtube.com/c/GoogleDevelopers"
              className="flex-1 px-4 py-2 border border-[#C2B8BE] rounded-l-md focus:ring-2 focus:ring-[#E34C4E] focus:border-[#E34C4E] focus:outline-none transition-colors"
              disabled={loading}
            />
            <button
              type="submit"
              className="bg-[#E34C4E] hover:bg-[#404059] text-white px-4 py-2 rounded-r-md font-medium transition-colors disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center"
              disabled={loading}
            >
              <Search className="h-4 w-4 mr-2" />
              Scrape Channel
            </button>
          </div>
          <p className="text-sm text-[#818595] mt-1">
            Enter a YouTube channel URL, handle (@username), or channel ID
          </p>
        </div>
      </form>

      {error && <ErrorAlert message={error} onDismiss={() => setError(null)} />}
      
      {loading && <Spinner />}
      
      {!loading && result && (
        <ResultCard data={result} type="channel" />
      )}
    </div>
  );
};

export default ChannelForm;
