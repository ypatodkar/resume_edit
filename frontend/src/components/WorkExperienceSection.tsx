import { FaBriefcase, FaCopy } from 'react-icons/fa';

interface WorkExperienceSectionProps {
  newLine: string;
  onCopy: (text: string) => void;
}

export default function WorkExperienceSection({ 
  newLine, 
  onCopy 
}: WorkExperienceSectionProps) {
  const wordCount = (text: string): number => {
    return text.split(/\s+/).filter(Boolean).length;
  };

  return (
    <section className="result-section">
      <div className="section-header">
        <h3><FaBriefcase className="icon" /> Work Experience</h3>
        <span className="word-count-badge">
          {wordCount(newLine)} words{' '}
          {wordCount(newLine) <= 15 ? '✅' : '⚠️'}
        </span>
      </div>
      <div className="work-experience-line">
        "{newLine}"
      </div>
      <button
        className="copy-button"
        onClick={() => onCopy(newLine)}
      >
        <FaCopy className="icon" /> Copy
      </button>
    </section>
  );
}

