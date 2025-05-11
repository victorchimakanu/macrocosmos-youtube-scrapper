
/**
 * Error alert component to display API or validation errors
 * 
 * @param {Object} props - Component props
 * @param {string} props.message - The error message to display
 * @param {Function} props.onDismiss - Function to call when dismissing the error
 * @returns {JSX.Element} Error alert component
 */
interface ErrorAlertProps {
  message: string;
  onDismiss: () => void;
}

const ErrorAlert = ({ message, onDismiss }: ErrorAlertProps) => {
  return (
    <div className="bg-red-50 border-l-4 border-red-500 p-4 my-4 rounded animate-fade-in" role="alert">
      <div className="flex items-start">
        <div className="flex-1">
          <p className="text-red-700 font-medium">Error</p>
          <p className="text-sm text-red-600 mt-1">{message}</p>
        </div>
        <button
          onClick={onDismiss}
          className="text-red-500 hover:text-red-700 transition-colors"
          aria-label="Dismiss"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default ErrorAlert;
