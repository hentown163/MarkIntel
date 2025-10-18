import PropTypes from 'prop-types';
import { Calendar, ArrowUp } from 'lucide-react';

export default function CampaignCard({ campaign }) {
  const { name, status, theme, start_date, end_date, metrics, channel_mix } = campaign;
  
  return (
    <div className="campaign-card">
      <div className="campaign-header">
        <h3>{name}</h3>
        <span className={`status-badge ${status}`}>{status}</span>
      </div>
      <div className="campaign-theme">
        <span className="theme-icon">💡</span>
        <span>{theme}</span>
      </div>
      <div className="campaign-meta">
        <span>
          <Calendar size={14} /> {start_date} - {end_date}
        </span>
        {metrics && (
          <span>
            <ArrowUp size={14} /> {metrics.engagement || metrics.leads || metrics.conversions}
          </span>
        )}
      </div>
      <div className="campaign-channels">
        {channel_mix && channel_mix.slice(0, 4).map((channel, idx) => (
          <span key={idx} className="channel-tag">{channel.channel}</span>
        ))}
      </div>
    </div>
  );
}

CampaignCard.propTypes = {
  campaign: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    theme: PropTypes.string.isRequired,
    start_date: PropTypes.string.isRequired,
    end_date: PropTypes.string.isRequired,
    metrics: PropTypes.object,
    channel_mix: PropTypes.arrayOf(PropTypes.object),
  }).isRequired,
};
