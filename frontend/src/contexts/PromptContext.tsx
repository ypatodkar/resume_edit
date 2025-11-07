import { createContext, useContext, useState, ReactNode } from 'react';

interface PromptContextType {
  customPrompt: string | null;
  setCustomPrompt: (prompt: string | null) => void;
  clearCustomPrompt: () => void;
}

const PromptContext = createContext<PromptContextType | undefined>(undefined);

export function PromptProvider({ children }: { children: ReactNode }) {
  const [customPrompt, setCustomPrompt] = useState<string | null>(null);

  const clearCustomPrompt = () => {
    setCustomPrompt(null);
  };

  return (
    <PromptContext.Provider value={{ customPrompt, setCustomPrompt, clearCustomPrompt }}>
      {children}
    </PromptContext.Provider>
  );
}

export function usePrompt() {
  const context = useContext(PromptContext);
  if (context === undefined) {
    throw new Error('usePrompt must be used within a PromptProvider');
  }
  return context;
}

