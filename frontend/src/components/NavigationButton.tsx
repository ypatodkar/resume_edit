import { useNavigate } from 'react-router-dom';

interface NavigationButtonProps {
  to: string;
  label: string;
  className?: string;
}

export default function NavigationButton({ to, label, className = '' }: NavigationButtonProps) {
  const navigate = useNavigate();

  return (
    <button
      onClick={() => navigate(to)}
      className={className}
    >
      {label}
    </button>
  );
}

