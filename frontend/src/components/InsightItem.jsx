import PropTypes from 'prop-types';
import { TrendingUp } from 'lucide-react';

export default function InsightItem({ insight }) {
  const { content, source, timestamp, impact } = insight;
  
  return (
    <div className="insight-item">
      <div className="insight-icon">
        <TrendingUp size={20} />
      </div>
      <div className="insight-content">
        <h4>{content.split('.')[0]}</h4>
        <div className="insight-meta">
          <span className="insight-source">{source}</span>
          <span className="insight-time">{new Date(timestamp).toLocaleTimeString()}</span>
        </div>
      </div>
      <span className={`impact-badge ${impact}`}>{impact} impact</span>
    </div>
  );
}

InsightItem.propTypes = {
  insight: PropTypes.shape({
    id: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
    source: PropTypes.string.isRequired,
    timestamp: PropTypes.string.isRequired,
    impact: PropTypes.string.isRequired,
  }).isRequired,
};
