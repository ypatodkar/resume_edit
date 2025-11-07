/**
 * Type definitions for the Resume Optimizer API responses
 */

export interface WorkExperienceSection {
  new_line: string;
}

export interface ProjectChanges {
  old_point?: string;
  new_point?: string;
  old_technologies?: string;
  new_technologies?: string;
}

export interface Project {
  project_name: string;
  status: 'modified' | 'no_changes';
  changes?: ProjectChanges;
}

export interface ResumeOptimizationResult {
  intro_note?: string;
  summary?: string;
  technical_skills?: string;
  work_experience_section?: WorkExperienceSection;
  fortinet_section?: WorkExperienceSection; // Backward compatibility
  projects?: Project[];
  overall_notes?: string;
}

export interface ApiError {
  error: string;
  trace?: string;
  raw_response?: string;
}

