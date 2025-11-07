import { FaRegLightbulb } from 'react-icons/fa';

interface NotesSectionProps {
  notes: string;
}

export default function NotesSection({ notes }: NotesSectionProps) {
  return (
    <section className="result-section">
      <div className="section-header">
        <h3><FaRegLightbulb className="icon" /> Notes</h3>
      </div>
      <p className="notes-text">{notes}</p>
    </section>
  );
}

