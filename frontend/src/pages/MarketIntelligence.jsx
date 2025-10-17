import { useState, useEffect } from 'react';
import { TrendingUp, Filter } from 'lucide-react';
import { marketIntelligenceAPI } from '../api/client';
import './MarketIntelligence.css';

export default function MarketIntelligence() {
  const [signals, setSignals] = useState([]);

  useEffect(() => {
    loadSignals();
  }, []);

  const loadSignals = async () => {
    try {
      const res = await marketIntelligenceAPI.getAll();
      setSignals(res.data);
    } catch (error) {
      console.error('Error loading signals:', error);
    }
  };

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
        {signals.map((signal) => (
          <div key={signal.id} className="signal-card">
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
        ))}
      </div>
    </div>
  );
}
