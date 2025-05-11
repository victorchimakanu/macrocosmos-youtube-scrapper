
import { useState } from 'react';
import VideoForm from '@/components/VideoForm';
import ChannelForm from '@/components/ChannelForm';
import ApiKeyBanner from '@/components/ApiKeyBanner';
import { FileText, Download } from 'lucide-react';
import { motion } from 'framer-motion';
import { useIsMobile } from '@/hooks/use-mobile';

/**
 * Main application page with tabs for video and channel scraping
 * 
 * @returns {JSX.Element} Main application page
 */
const Index = () => {
  const [activeTab, setActiveTab] = useState<'video' | 'channel'>('video');
  const isMobile = useIsMobile();

  return (
    <motion.div 
      className="min-h-screen font-sans relative"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#E7E8EA] to-[#C2B8BE] z-0 overflow-hidden">
        <motion.div 
          className="absolute top-0 right-0 w-1/3 h-1/3 rounded-full bg-gradient-to-br from-[#E34C4E]/20 to-[#404059]/30 blur-3xl"
          animate={{ 
            x: [10, 30, 10], 
            y: [10, 25, 10],
            scale: [1, 1.1, 1],
          }}
          transition={{ 
            duration: 20, 
            repeat: Infinity, 
            repeatType: "reverse" 
          }}
        />
        <motion.div 
          className="absolute bottom-10 left-10 w-1/4 h-1/4 rounded-full bg-gradient-to-tr from-[#404059]/20 to-[#C2B8BE]/30 blur-3xl"
          animate={{ 
            x: [-10, -30, -10], 
            y: [10, -20, 10],
            scale: [1, 1.2, 1],
          }}
          transition={{ 
            duration: 25, 
            repeat: Infinity, 
            repeatType: "reverse" 
          }}
        />
      </div>
      
      {/* Header with updated colors and layout */}
      <header className="relative z-10 bg-gradient-to-r from-[#E34C4E] to-[#404059] text-white shadow-lg">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <motion.div 
              className="flex items-center"
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <div className="flex-shrink-0">
                <motion.img 
                  src="/logo.png" 
                  alt="Macrocosmos Logo" 
                  className="h-10 w-10" 
                  whileHover={{ 
                    rotate: 10,
                    scale: 1.1,
                  }}
                  transition={{ type: "spring", stiffness: 300 }}
                />
              </div>
              <div className="ml-4">
                <h1 className="text-2xl font-bold text-white">YT Scraper</h1>
              </div>
            </motion.div>
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        <ApiKeyBanner />

        {/* Introduction with updated colors */}
        <motion.div 
          className="bg-white/80 backdrop-blur-sm rounded-lg shadow-md p-4 sm:p-6 mb-6 sm:mb-8 border-l-4 border-[#E34C4E]"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ type: "spring", damping: 12, delay: 0.1 }}
        >
          <h2 className="text-xl font-bold text-[#404059] mb-3 flex items-center">
            <FileText className="h-5 w-5 mr-2 text-[#E34C4E]" />
            Welcome to Macrocosmos YouTube Scraper
          </h2>
          <p className="text-[#404059] mb-4">
            This tool allows you to extract valuable data from YouTube videos and channels. Simply enter a YouTube URL or ID, 
            and our service will scrape the available information and present it in a structured format.
          </p>
          <motion.div 
            className="bg-[#E7E8EA]/70 p-4 rounded-md border border-[#C2B8BE] flex items-start"
            whileHover={{ scale: 1.01, backgroundColor: "rgba(231, 232, 234, 0.9)" }}
          >
            <Download className="h-5 w-5 mr-2 text-[#404059] mt-1 flex-shrink-0" />
            <p className="text-[#404059] text-sm">
              <span className="font-medium">Important:</span> When scraping video content, the transcript is automatically 
              downloaded and saved as a PDF file for your convenience. You can use this for research, content analysis, or reference purposes.
            </p>
          </motion.div>
        </motion.div>

        {/* Tabs with updated colors */}
        <motion.div 
          className="bg-white/80 backdrop-blur-sm rounded-lg shadow-md overflow-hidden mb-6 sm:mb-8"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ type: "spring", damping: 12, delay: 0.2 }}
        >
          <div className="flex flex-col sm:flex-row border-b border-[#C2B8BE]">
            <motion.button
              onClick={() => setActiveTab('video')}
              className={`
                py-3 sm:py-4 px-4 sm:px-6 font-medium text-sm focus:outline-none transition-all duration-300 relative
                ${activeTab === 'video'
                  ? 'text-[#E34C4E] bg-white'
                  : 'text-[#818595] hover:text-[#404059] bg-[#E7E8EA] hover:bg-[#C2B8BE]/30'}
              `}
              whileHover={{ backgroundColor: activeTab === 'video' ? 'rgba(255,255,255,1)' : 'rgba(194,184,190,0.3)' }}
              whileTap={{ scale: 0.98 }}
              aria-current={activeTab === 'video' ? 'page' : undefined}
            >
              <span className="flex items-center justify-center">
                <svg className="h-5 w-5 mr-2" fill={activeTab === 'video' ? '#E34C4E' : '#818595'} viewBox="0 0 24 24">
                  <path d="M23 7v10c0 1.105-.895 2-2 2H3c-1.105 0-2-.895-2-2V7c0-1.105.895-2 2-2h18c1.105 0 2 .895 2 2zm-2 0l-9 5.5L3 7v10l9-5.5 9 5.5V7z"/>
                </svg>
                Video Scraper
              </span>
              {activeTab === 'video' && (
                <motion.span 
                  className="absolute bottom-0 left-0 w-full h-1 bg-[#E34C4E]"
                  layoutId="activeTab"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
            </motion.button>
            <motion.button
              onClick={() => setActiveTab('channel')}
              className={`
                py-3 sm:py-4 px-4 sm:px-6 font-medium text-sm focus:outline-none transition-all duration-300 relative
                ${activeTab === 'channel'
                  ? 'text-[#E34C4E] bg-white'
                  : 'text-[#818595] hover:text-[#404059] bg-[#E7E8EA] hover:bg-[#C2B8BE]/30'}
              `}
              whileHover={{ backgroundColor: activeTab === 'channel' ? 'rgba(255,255,255,1)' : 'rgba(194,184,190,0.3)' }}
              whileTap={{ scale: 0.98 }}
              aria-current={activeTab === 'channel' ? 'page' : undefined}
            >
              <span className="flex items-center justify-center">
                <svg className="h-5 w-5 mr-2" fill={activeTab === 'channel' ? '#E34C4E' : '#818595'} viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                </svg>
                Channel Scraper
              </span>
              {activeTab === 'channel' && (
                <motion.span 
                  className="absolute bottom-0 left-0 w-full h-1 bg-[#E34C4E]"
                  layoutId="activeTab"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
            </motion.button>
          </div>

          {/* Content */}
          <motion.div 
            className="p-4 sm:p-6 bg-white"
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            {activeTab === 'video' ? <VideoForm /> : <ChannelForm />}
          </motion.div>
        </motion.div>

        {/* How to Use Section with updated colors */}
        <motion.div 
          className="bg-white/80 backdrop-blur-sm rounded-lg shadow-md p-4 sm:p-6 mb-6 sm:mb-8 border-l-4 border-[#818595]"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ type: "spring", damping: 12, delay: 0.3 }}
          whileHover={{ boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)" }}
        >
          <h2 className="text-xl font-bold text-[#404059] mb-3">How to Use</h2>
          <ol className="list-decimal list-inside space-y-2 text-[#404059]">
            <motion.li 
              initial={{ x: -5, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              Select either <strong>Video Scraper</strong> or <strong>Channel Scraper</strong> tab based on your needs.
            </motion.li>
            <motion.li 
              initial={{ x: -5, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              Enter a YouTube video URL (e.g., <code className="bg-[#E7E8EA] px-1 py-0.5 rounded text-sm">https://www.youtube.com/watch?v=dQw4w9WgXcQ</code>) or channel URL.
            </motion.li>
            <motion.li 
              initial={{ x: -5, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              Click the "Scrape" button and wait for the results to appear.
            </motion.li>
            <motion.li 
              initial={{ x: -5, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.7 }}
            >
              View the structured data extracted from YouTube.
            </motion.li>
            <motion.li 
              initial={{ x: -5, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              For videos with transcripts, a PDF will be automatically downloaded.
            </motion.li>
          </ol>
        </motion.div>
      </main>

      {/* Footer with updated colors */}
      <footer className="relative z-10 bg-[#404059] text-white py-6 sm:py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-[#C2B8BE] text-sm">
            © {new Date().getFullYear()} Macrocosmos YouTube Scraper · All rights reserved
          </p>
        </div>
      </footer>
    </motion.div>
  );
};

export default Index;
