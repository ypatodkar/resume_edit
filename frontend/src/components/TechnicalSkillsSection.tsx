import { FaTools, FaCopy } from 'react-icons/fa';

interface TechnicalSkillsSectionProps {
  technicalSkills: string;
  onCopy: (text: string) => void;
}

export default function TechnicalSkillsSection({ 
  technicalSkills, 
  onCopy 
}: TechnicalSkillsSectionProps) {
  return (
    <section className="result-section">
      <div className="section-header">
        <h3><FaTools className="icon" /> Technical Skills</h3>
      </div>
      <div className="skills-text">
        {technicalSkills.split('\n').map((line, idx) => (
          <div key={idx} className="skill-line">
            {line.startsWith('**') ? (
              <strong>{line.replace(/\*\*/g, '')}</strong>
            ) : (
              line
            )}
          </div>
        ))}
      </div>
      <button
        className="copy-button"
        onClick={() => onCopy(technicalSkills)}
      >
        <FaCopy className="icon" /> Copy
      </button>
    </section>
  );
}

