interface ErrorBoxProps {
  error: string;
}

export default function ErrorBox({ error }: ErrorBoxProps) {
  return (
    <div className="error-box">
      <h3>❌ Error</h3>
      <p>{error}</p>
    </div>
  );
}

