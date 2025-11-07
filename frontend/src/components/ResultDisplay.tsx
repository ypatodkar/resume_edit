import { FaFileAlt } from 'react-icons/fa';
import { ResumeOptimizationResult } from '../types';
import SummarySection from './SummarySection';
import TechnicalSkillsSection from './TechnicalSkillsSection';
import WorkExperienceSection from './WorkExperienceSection';
import ProjectsSection from './ProjectsSection';
import NotesSection from './NotesSection';

interface ResultDisplayProps {
  result: ResumeOptimizationResult;
}

export default function ResultDisplay({ result }: ResultDisplayProps) {
  // Backward compatibility: handle both old and new key names
  const workExperienceSection = result.work_experience_section || result.fortinet_section;

  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  return (
    <div className="result-container">
      <div className="result-header">
        <h2>✨ Optimization Results</h2>
        {result.intro_note && (
          <p className="intro-note">{result.intro_note}</p>
        )}
      </div>

      <div className="results-content">
        {result.summary && (
          <SummarySection 
            summary={result.summary} 
            onCopy={handleCopy} 
          />
        )}

        {result.technical_skills && (
          <TechnicalSkillsSection 
            technicalSkills={result.technical_skills} 
            onCopy={handleCopy} 
          />
        )}

        {workExperienceSection && (
          <WorkExperienceSection 
            newLine={workExperienceSection.new_line} 
            onCopy={handleCopy} 
          />
        )}

        {result.projects && result.projects.length > 0 && (
          <ProjectsSection projects={result.projects} />
        )}

        {result.overall_notes && (
          <NotesSection notes={result.overall_notes} />
        )}
      </div>

      <div className="json-viewer">
        <details>
          <summary><FaFileAlt className="icon" /> View Raw JSON</summary>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </details>
      </div>
    </div>
  );
}

