
import { motion } from 'framer-motion';

/**
 * A loading spinner component to show during API requests
 * 
 * @returns {JSX.Element} Animated spinner element
 */
const Spinner = () => {
  return (
    <div className="flex justify-center items-center p-6" aria-busy="true" aria-label="Loading">
      <motion.div 
        className="flex flex-col items-center"
      >
        <motion.div 
          className="h-10 w-10 rounded-full border-4 border-[#C2B8BE]"
          animate={{ 
            rotate: 360,
            borderTopColor: ['#E34C4E', '#404059', '#818595', '#E34C4E'],
            scale: [1, 1.1, 1],
          }}
          transition={{ 
            duration: 1.8, 
            repeat: Infinity, 
            ease: "linear",
          }}
        />
        <motion.p
          className="mt-3 text-sm text-[#404059] font-medium"
          animate={{ opacity: [0.6, 1, 0.6] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          Scraping video data...
        </motion.p>
      </motion.div>
    </div>
  );
};

export default Spinner;
