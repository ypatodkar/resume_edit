import { FaFolderOpen, FaCopy } from 'react-icons/fa';
import { Project } from '../types';

interface ProjectsSectionProps {
  projects: Project[];
  onCopy: (text: string) => void;
}

export default function ProjectsSection({ projects, onCopy }: ProjectsSectionProps) {
  const wordCount = (text: string | undefined): number => {
    if (!text) return 0;
    return text.split(/\s+/).filter(Boolean).length;
  };

  const formatProjectForCopy = (project: Project): string => {
    let text = `${project.project_name}\n`;
    
    if (project.status === 'modified' && project.changes) {
      if (project.changes.old_point) {
        text += `Change this point: "${project.changes.old_point}"\n`;
      }
      if (project.changes.new_point) {
        text += `To: "${project.changes.new_point}"\n`;
      }
      if (project.changes.new_technologies) {
        text += `Change Technologies to: ${project.changes.new_technologies}\n`;
      }
    } else if (project.status === 'no_changes') {
      text += 'No changes needed.\n';
    }
    
    return text.trim();
  };

  const getAllProjectsText = (): string => {
    return projects
      .map((project, idx) => {
        let text = `${idx + 1}. ${formatProjectForCopy(project)}`;
        return text;
      })
      .join('\n\n');
  };

  return (
    <section className="result-section">
      <div className="section-header">
        <h3><FaFolderOpen className="icon" /> Projects ({projects.length} projects)</h3>
        <button
          className="copy-button"
          onClick={() => onCopy(getAllProjectsText())}
          title="Copy all projects"
        >
          <FaCopy className="icon" /> Copy All
        </button>
      </div>
      <div className="projects-list">
        {projects.map((project, idx) => (
          <div key={idx} className="project-item">
            <h4>
              {idx + 1}. {project.project_name}
              {project.status === 'no_changes' && (
                <span className="status-badge no-changes">✅ No changes</span>
              )}
              {project.status === 'modified' && (
                <span className="status-badge modified">✏️ Modified</span>
              )}
            </h4>
            {project.status === 'modified' && project.changes && (
              <div className="project-changes">
                {project.changes.old_point && (
                  <div className="change-item">
                    <strong>Change this point:</strong>
                    <p className="old-text">"{project.changes.old_point}"</p>
                  </div>
                )}
                {project.changes.new_point && (
                  <div className="change-item">
                    <strong>To:</strong>
                    <p className="new-text">"{project.changes.new_point}"</p>
                    <div className="word-count-small">
                      {wordCount(project.changes.new_point)} words
                    </div>
                  </div>
                )}
                {project.changes.old_technologies && project.changes.new_technologies && (
                  <div className="change-item">
                    <strong>Change Technologies to:</strong>
                    <p className="new-text">{project.changes.new_technologies}</p>
                  </div>
                )}
                <button
                  className="copy-button-small"
                  onClick={() => onCopy(formatProjectForCopy(project))}
                  title="Copy this project"
                >
                  <FaCopy className="icon" /> Copy
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

