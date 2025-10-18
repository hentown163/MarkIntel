import PropTypes from 'prop-types';
import { Target, TrendingUp, Users, Sparkles } from 'lucide-react';

const iconMap = {
  Target,
  TrendingUp,
  Users,
  Sparkles,
};

export default function StatCard({ iconName, label, value, change }) {
  const Icon = iconMap[iconName] || Target;
  
  return (
    <div className="stat-card">
      <div className="stat-icon">
        <Icon size={24} />
      </div>
      <div className="stat-content">
        <h3>{value}</h3>
        <p>{label}</p>
        <span className="stat-change">{change}</span>
      </div>
    </div>
  );
}

StatCard.propTypes = {
  iconName: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  change: PropTypes.string.isRequired,
};
