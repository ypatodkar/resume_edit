import { useState, FormEvent } from 'react';
import './App.css';
import axios from 'axios';
import { ResumeOptimizationResult } from './types';
import { usePrompt } from './contexts/PromptContext';
import ResumeForm from './components/ResumeForm';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorBox from './components/ErrorBox';
import ResultDisplay from './components/ResultDisplay';
import NavigationButton from './components/NavigationButton';

// Normalize API URL - remove trailing slash to prevent double slashes
const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

function App() {
  const [resumeText, setResumeText] = useState<string>('');
  const [jobDescription, setJobDescription] = useState<string>('');
  const [result, setResult] = useState<ResumeOptimizationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { customPrompt } = usePrompt();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);

    try {
      const requestBody: any = {
        resume_text: resumeText,
        job_description: jobDescription
      };

      // Include custom prompt if set
      if (customPrompt) {
        requestBody.custom_prompt = customPrompt;
      }

      const response = await axios.post<ResumeOptimizationResult>(`${API_URL}/optimize/text`, requestBody);
      setResult(response.data);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const errorMessage = err.response?.data?.error || err.message || 'An error occurred';
        setError(errorMessage);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setResumeText('');
    setJobDescription('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <div className="header-top">
            <div>
              <h1>📄 Resume Optimizer</h1>
              <p>Optimize your resume to match job descriptions using AI</p>
            </div>
            <NavigationButton 
              to="/prompt-editor" 
              label="⚙️ Edit Prompt" 
              className="secondary"
            />
          </div>
          {customPrompt && (
            <div className="custom-prompt-indicator">
              ⚠️ Using custom prompt for this session
            </div>
          )}
        </header>

        <ResumeForm
          resumeText={resumeText}
          jobDescription={jobDescription}
          loading={loading}
          onResumeTextChange={setResumeText}
          onJobDescriptionChange={setJobDescription}
          onSubmit={handleSubmit}
          onClear={handleClear}
        />

        {loading && <LoadingSpinner />}

        {error && <ErrorBox error={error} />}

        {!loading && result && <ResultDisplay result={result} />}
      </div>
    </div>
  );
}

export default App;
