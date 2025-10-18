import { TrendingUp, Filter } from 'lucide-react';
import { useMarketIntelligence } from '../hooks';
import './MarketIntelligence.css';

function SignalCard({ signal }) {
  return (
    <div className="signal-card">
      <div className="signal-icon">
        <TrendingUp size={24} />
      </div>
      <div className="signal-content">
        <div className="signal-header">
          <h3>{signal.content.split('.')[0]}</h3>
          <span className={`impact-badge ${signal.impact}`}>{signal.impact} impact</span>
        </div>
        <p className="signal-description">{signal.content}</p>
        <div className="signal-meta">
          <span className="signal-source">{signal.source}</span>
          <span className="signal-time">{new Date(signal.timestamp).toLocaleString()}</span>
          <div className="signal-tags">
            {signal.category && <span className="tag">{signal.category}</span>}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function MarketIntelligence() {
  const { signals, loading, error, reload } = useMarketIntelligence();

  if (error) {
    return (
      <div className="market-intelligence">
        <div className="error-message">
          Error loading market intelligence: {error}
          <button onClick={reload}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="market-intelligence">
      <div className="page-header">
        <div>
          <h1>Market Intelligence</h1>
          <p>Real-time analysis of 10,000+ daily data points across press releases, reports, and social media</p>
        </div>
        <button className="btn-filter">
          <Filter size={18} />
          Advanced Filters
        </button>
      </div>

      <div className="signals-list">
        {loading && signals.length === 0 ? (
          <div>Loading market signals...</div>
        ) : (
          signals.map((signal) => (
            <SignalCard key={signal.id} signal={signal} />
          ))
        )}
      </div>
    </div>
  );
}
