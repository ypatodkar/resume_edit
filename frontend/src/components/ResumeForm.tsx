import { FormEvent } from 'react';

interface ResumeFormProps {
  resumeText: string;
  jobDescription: string;
  loading: boolean;
  onResumeTextChange: (value: string) => void;
  onJobDescriptionChange: (value: string) => void;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
  onClear: () => void;
}

export default function ResumeForm({
  resumeText,
  jobDescription,
  loading,
  onResumeTextChange,
  onJobDescriptionChange,
  onSubmit,
  onClear,
}: ResumeFormProps) {
  return (
    <form onSubmit={onSubmit} className="form">
      <div className="form-row">
        <div className="form-group">
          <label htmlFor="resume">Resume Text</label>
          <textarea
            id="resume"
            value={resumeText}
            onChange={(e) => onResumeTextChange(e.target.value)}
            placeholder="Paste your resume text here..."
            rows={10}
            required
          />
          <div className="char-count">{resumeText.length} characters</div>
        </div>

        <div className="form-group">
          <label htmlFor="jobDescription">Job Description</label>
          <textarea
            id="jobDescription"
            value={jobDescription}
            onChange={(e) => onJobDescriptionChange(e.target.value)}
            placeholder="Paste the job description here..."
            rows={10}
            required
          />
          <div className="char-count">{jobDescription.length} characters</div>
        </div>
      </div>

      <div className="button-group">
        <button type="submit" disabled={loading || !resumeText || !jobDescription}>
          🚀 Optimize Resume
        </button>
        <button type="button" onClick={onClear} className="secondary">
          Clear
        </button>
      </div>
    </form>
  );
}

