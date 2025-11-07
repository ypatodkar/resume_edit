import { FaFileAlt, FaCopy } from 'react-icons/fa';

interface SummarySectionProps {
  summary: string;
  onCopy: (text: string) => void;
}

export default function SummarySection({ summary, onCopy }: SummarySectionProps) {
  const wordCount = (text: string): number => {
    return text.split(/\s+/).filter(Boolean).length;
  };

  return (
    <section className="result-section">
      <div className="section-header">
        <h3><FaFileAlt className="icon" /> Summary</h3>
        <span className="word-count-badge">
          {wordCount(summary)} words {wordCount(summary) < 33 ? '✅' : '⚠️'}
        </span>
      </div>
      <p className="summary-text">{summary}</p>
      <button
        className="copy-button"
        onClick={() => onCopy(summary)}
      >
        <FaCopy className="icon" /> Copy
      </button>
    </section>
  );
}

