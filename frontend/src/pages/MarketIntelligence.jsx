import { useState } from 'react';
import { TrendingUp, Filter, Download, X } from 'lucide-react';
import { useMarketIntelligence } from '../hooks';
import './MarketIntelligence.css';
import axios from 'axios';

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

function FilterModal({ isOpen, onClose, onApplyFilters }) {
  const [impact, setImpact] = useState('');
  const [category, setCategory] = useState('');
  const [source, setSource] = useState('');
  const [minRelevance, setMinRelevance] = useState('');

  if (!isOpen) return null;

  const handleApply = () => {
    onApplyFilters({ impact, category, source, min_relevance: minRelevance });
    onClose();
  };

  const handleClear = () => {
    setImpact('');
    setCategory('');
    setSource('');
    setMinRelevance('');
    onApplyFilters({});
    onClose();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Advanced Filters</h2>
          <button className="modal-close" onClick={onClose}>
            <X size={24} />
          </button>
        </div>
        <div className="modal-body">
          <div className="filter-group">
            <label>Impact Level</label>
            <select value={impact} onChange={(e) => setImpact(e.target.value)}>
              <option value="">All Levels</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <div className="filter-group">
            <label>Category</label>
            <input
              type="text"
              placeholder="Enter category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            />
          </div>
          <div className="filter-group">
            <label>Source</label>
            <input
              type="text"
              placeholder="Search by source"
              value={source}
              onChange={(e) => setSource(e.target.value)}
            />
          </div>
          <div className="filter-group">
            <label>Minimum Relevance Score (0-1)</label>
            <input
              type="number"
              min="0"
              max="1"
              step="0.1"
              placeholder="e.g., 0.7"
              value={minRelevance}
              onChange={(e) => setMinRelevance(e.target.value)}
            />
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn-secondary" onClick={handleClear}>Clear All</button>
          <button className="btn-primary" onClick={handleApply}>Apply Filters</button>
        </div>
      </div>
    </div>
  );
}

export default function MarketIntelligence() {
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [filters, setFilters] = useState({});
  const [filteredSignals, setFilteredSignals] = useState([]);
  const [isFiltering, setIsFiltering] = useState(false);
  const { signals, loading, error, reload } = useMarketIntelligence();

  const applyFilters = async (newFilters) => {
    if (Object.keys(newFilters).length === 0 || Object.values(newFilters).every(v => !v)) {
      setIsFiltering(false);
      setFilters({});
      setFilteredSignals([]);
      return;
    }

    try {
      setIsFiltering(true);
      setFilters(newFilters);
      const params = new URLSearchParams();
      if (newFilters.impact) params.append('impact', newFilters.impact);
      if (newFilters.category) params.append('category', newFilters.category);
      if (newFilters.source) params.append('source', newFilters.source);
      if (newFilters.min_relevance) params.append('min_relevance', newFilters.min_relevance);

      const response = await axios.get(`/api/market-intelligence/filter?${params}`);
      setFilteredSignals(response.data);
    } catch (error) {
      console.error('Filter error:', error);
    }
  };

  const handleExport = async (format) => {
    try {
      const response = await axios.get(`/api/export/market-intelligence?format=${format}`, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `market_intelligence.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Export error:', error);
    }
  };

  const displaySignals = isFiltering ? filteredSignals : signals;

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
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="btn-filter" onClick={() => setIsFilterOpen(true)}>
            <Filter size={18} />
            Advanced Filters
            {isFiltering && <span className="filter-badge">{Object.keys(filters).length}</span>}
          </button>
          <button className="btn-secondary" onClick={() => handleExport('csv')}>
            <Download size={18} />
            Export CSV
          </button>
          <button className="btn-secondary" onClick={() => handleExport('json')}>
            <Download size={18} />
            Export JSON
          </button>
        </div>
      </div>

      <div className="signals-list">
        {loading && displaySignals.length === 0 ? (
          <div>Loading market signals...</div>
        ) : (
          displaySignals.map((signal) => (
            <SignalCard key={signal.id} signal={signal} />
          ))
        )}
      </div>

      <FilterModal
        isOpen={isFilterOpen}
        onClose={() => setIsFilterOpen(false)}
        onApplyFilters={applyFilters}
      />
    </div>
  );
}
