import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { PromptProvider } from './contexts/PromptContext';
import App from './App';
import PromptEditor from './pages/PromptEditor';
import './index.css';

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('Failed to find the root element');
}

const root = createRoot(rootElement);
root.render(
  <StrictMode>
    <BrowserRouter>
      <PromptProvider>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/prompt-editor" element={<PromptEditor />} />
        </Routes>
      </PromptProvider>
    </BrowserRouter>
  </StrictMode>
);

