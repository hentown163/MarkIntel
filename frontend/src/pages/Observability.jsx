import { useState } from 'react';
import { Activity, Brain, Clock, CheckCircle, AlertCircle, TrendingUp } from 'lucide-react';
import './Observability.css';
import useObservability from '../hooks/useObservability';

function Observability() {
  const [activeTab, setActiveTab] = useState('decisions');
  const [selectedDecision, setSelectedDecision] = useState(null);
  const [selectedTrace, setSelectedTrace] = useState(null);
  
  const { decisions, traces, metrics, stats, loading, error } = useObservability();

  if (loading) {
    return (
      <div className="observability-page">
        <div className="loading-state">
          <Activity className="spinning" size={48} />
          <p>Loading observability data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="observability-page">
        <div className="error-state">
          <AlertCircle size={48} />
          <p>Error loading observability data: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="observability-page">
      <div className="page-header">
        <div className="header-content">
          <Brain size={32} />
          <div>
            <h1>Agent Observability</h1>
            <p>Complete visibility into autonomous agent reasoning and execution</p>
          </div>
        </div>
        <div className="system-status">
          <CheckCircle size={20} className="status-active" />
          <span>Agent Active</span>
        </div>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon decisions">
            <Brain size={24} />
          </div>
          <div className="metric-content">
            <div className="metric-value">{stats?.total_decisions || 0}</div>
            <div className="metric-label">Total Decisions</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon traces">
            <Activity size={24} />
          </div>
          <div className="metric-content">
            <div className="metric-value">{stats?.total_traces || 0}</div>
            <div className="metric-label">Execution Traces</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon performance">
            <TrendingUp size={24} />
          </div>
          <div className="metric-content">
            <div className="metric-value">{stats?.success_rate || '0'}%</div>
            <div className="metric-label">Success Rate</div>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon speed">
            <Clock size={24} />
          </div>
          <div className="metric-content">
            <div className="metric-value">{stats?.avg_duration || '0'}ms</div>
            <div className="metric-label">Avg Duration</div>
          </div>
        </div>
      </div>

      <div className="observability-tabs">
        <button
          className={`tab-button ${activeTab === 'decisions' ? 'active' : ''}`}
          onClick={() => setActiveTab('decisions')}
        >
          <Brain size={18} />
          Agent Decisions
        </button>
        <button
          className={`tab-button ${activeTab === 'traces' ? 'active' : ''}`}
          onClick={() => setActiveTab('traces')}
        >
          <Activity size={18} />
          Execution Traces
        </button>
        <button
          className={`tab-button ${activeTab === 'performance' ? 'active' : ''}`}
          onClick={() => setActiveTab('performance')}
        >
          <TrendingUp size={18} />
          Performance
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'decisions' && (
          <DecisionsTab 
            decisions={decisions} 
            selectedDecision={selectedDecision}
            onSelectDecision={setSelectedDecision}
          />
        )}
        
        {activeTab === 'traces' && (
          <TracesTab 
            traces={traces}
            selectedTrace={selectedTrace}
            onSelectTrace={setSelectedTrace}
          />
        )}
        
        {activeTab === 'performance' && (
          <PerformanceTab metrics={metrics} stats={stats} />
        )}
      </div>
    </div>
  );
}

function DecisionsTab({ decisions, selectedDecision, onSelectDecision }) {
  if (!decisions || decisions.length === 0) {
    return (
      <div className="empty-state">
        <Brain size={48} />
        <h3>No Decisions Logged</h3>
        <p>Agent decisions will appear here as the system operates</p>
      </div>
    );
  }

  return (
    <div className="decisions-container">
      <div className="decisions-list">
        {decisions.map((decision) => (
          <div
            key={decision.decision_id}
            className={`decision-card ${selectedDecision?.decision_id === decision.decision_id ? 'selected' : ''}`}
            onClick={() => onSelectDecision(decision)}
          >
            <div className="decision-header">
              <div className="decision-type">{formatDecisionType(decision.decision_type)}</div>
              <div className="decision-time">{formatTimestamp(decision.timestamp)}</div>
            </div>
            
            <div className="confidence-bar">
              <div className="confidence-label">Confidence</div>
              <div className="confidence-meter">
                <div 
                  className="confidence-fill"
                  style={{ width: `${decision.confidence_score * 100}%` }}
                />
              </div>
              <div className="confidence-value">{(decision.confidence_score * 100).toFixed(0)}%</div>
            </div>

            {decision.session_id && (
              <div className="decision-meta">
                <span className="session-badge">Session: {decision.session_id.slice(0, 8)}</span>
              </div>
            )}
          </div>
        ))}
      </div>

      {selectedDecision && (
        <div className="decision-details">
          <div className="details-header">
            <h3>Decision Details</h3>
            <button className="close-button" onClick={() => onSelectDecision(null)}>×</button>
          </div>

          <div className="details-section">
            <h4>Decision Information</h4>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Type:</span>
                <span className="info-value">{formatDecisionType(selectedDecision.decision_type)}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Timestamp:</span>
                <span className="info-value">{new Date(selectedDecision.timestamp).toLocaleString()}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Confidence:</span>
                <span className="info-value">{(selectedDecision.confidence_score * 100).toFixed(1)}%</span>
              </div>
              {selectedDecision.session_id && (
                <div className="info-item">
                  <span className="info-label">Session ID:</span>
                  <span className="info-value">{selectedDecision.session_id}</span>
                </div>
              )}
            </div>
          </div>

          <div className="details-section">
            <h4>Reasoning Chain</h4>
            <div className="reasoning-chain">
              {selectedDecision.reasoning_chain.map((step, index) => (
                <div key={index} className="reasoning-step">
                  <div className="step-number">{index + 1}</div>
                  <div className="step-content">{step}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="details-section">
            <h4>Data Sources</h4>
            <div className="data-sources">
              {selectedDecision.data_sources.map((source, index) => (
                <span key={index} className="source-badge">{source}</span>
              ))}
            </div>
          </div>

          {selectedDecision.metadata && Object.keys(selectedDecision.metadata).length > 0 && (
            <div className="details-section">
              <h4>Metadata</h4>
              <pre className="metadata-block">{JSON.stringify(selectedDecision.metadata, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function TracesTab({ traces, selectedTrace, onSelectTrace }) {
  if (!traces || traces.length === 0) {
    return (
      <div className="empty-state">
        <Activity size={48} />
        <h3>No Execution Traces</h3>
        <p>Execution traces will appear here as the agent performs tasks</p>
      </div>
    );
  }

  return (
    <div className="traces-container">
      <div className="traces-list">
        {traces.map((trace) => (
          <div
            key={trace.trace_id}
            className={`trace-card ${selectedTrace?.trace_id === trace.trace_id ? 'selected' : ''} ${trace.success ? 'success' : 'failure'}`}
            onClick={() => onSelectTrace(trace)}
          >
            <div className="trace-header">
              <div className="trace-status">
                {trace.success ? (
                  <CheckCircle size={20} className="success-icon" />
                ) : (
                  <AlertCircle size={20} className="error-icon" />
                )}
                <span>{trace.success ? 'Success' : 'Failed'}</span>
              </div>
              <div className="trace-time">{formatTimestamp(trace.start_time)}</div>
            </div>

            <div className="trace-info">
              <div className="trace-stat">
                <Clock size={16} />
                <span>{trace.total_duration_ms ? `${trace.total_duration_ms.toFixed(0)}ms` : 'In progress'}</span>
              </div>
              <div className="trace-stat">
                <Activity size={16} />
                <span>{trace.steps.length} steps</span>
              </div>
            </div>

            {!trace.success && trace.error_message && (
              <div className="trace-error">{trace.error_message}</div>
            )}
          </div>
        ))}
      </div>

      {selectedTrace && (
        <div className="trace-details">
          <div className="details-header">
            <h3>Execution Trace Details</h3>
            <button className="close-button" onClick={() => onSelectTrace(null)}>×</button>
          </div>

          <div className="details-section">
            <h4>Trace Information</h4>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Status:</span>
                <span className={`info-value ${selectedTrace.success ? 'success' : 'error'}`}>
                  {selectedTrace.success ? 'Success' : 'Failed'}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Duration:</span>
                <span className="info-value">
                  {selectedTrace.total_duration_ms ? `${selectedTrace.total_duration_ms.toFixed(0)}ms` : 'In progress'}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Start:</span>
                <span className="info-value">{new Date(selectedTrace.start_time).toLocaleString()}</span>
              </div>
              {selectedTrace.end_time && (
                <div className="info-item">
                  <span className="info-label">End:</span>
                  <span className="info-value">{new Date(selectedTrace.end_time).toLocaleString()}</span>
                </div>
              )}
            </div>
          </div>

          {!selectedTrace.success && selectedTrace.error_message && (
            <div className="details-section">
              <h4>Error</h4>
              <div className="error-message">{selectedTrace.error_message}</div>
            </div>
          )}

          <div className="details-section">
            <h4>Execution Steps</h4>
            <div className="execution-steps">
              {selectedTrace.steps.map((step, index) => (
                <div key={index} className="execution-step">
                  <div className="step-header">
                    <div className="step-number">{index + 1}</div>
                    <div className="step-name">{step.name}</div>
                    {step.duration_ms && (
                      <div className="step-duration">{step.duration_ms.toFixed(0)}ms</div>
                    )}
                  </div>
                  {step.details && (
                    <div className="step-details">{step.details}</div>
                  )}
                  {step.result && (
                    <div className="step-result">
                      <strong>Result:</strong> {JSON.stringify(step.result)}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function PerformanceTab({ metrics, stats }) {
  return (
    <div className="performance-container">
      <div className="performance-section">
        <h3>Overall Statistics</h3>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Total Decisions</div>
            <div className="stat-value">{stats?.total_decisions || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Total Traces</div>
            <div className="stat-value">{stats?.total_traces || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Success Rate</div>
            <div className="stat-value success">{stats?.success_rate || 0}%</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Average Confidence</div>
            <div className="stat-value">{stats?.avg_confidence ? (stats.avg_confidence * 100).toFixed(1) + '%' : 'N/A'}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Average Duration</div>
            <div className="stat-value">{stats?.avg_duration || 0}ms</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Total Steps</div>
            <div className="stat-value">{metrics?.total_steps || 0}</div>
          </div>
        </div>
      </div>

      {stats?.by_type && Object.keys(stats.by_type).length > 0 && (
        <div className="performance-section">
          <h3>Decisions by Type</h3>
          <div className="decision-types">
            {Object.entries(stats.by_type).map(([type, count]) => (
              <div key={type} className="type-card">
                <div className="type-label">{formatDecisionType(type)}</div>
                <div className="type-count">{count}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {metrics && (
        <div className="performance-section">
          <h3>Performance Metrics</h3>
          <div className="metrics-details">
            <div className="metric-row">
              <span className="metric-name">Total Execution Time:</span>
              <span className="metric-val">{metrics.total_execution_time_ms?.toFixed(0) || 0}ms</span>
            </div>
            <div className="metric-row">
              <span className="metric-name">API Calls Made:</span>
              <span className="metric-val">{metrics.api_calls_count || 0}</span>
            </div>
            <div className="metric-row">
              <span className="metric-name">Tokens Used:</span>
              <span className="metric-val">{metrics.total_tokens_used?.toLocaleString() || 0}</span>
            </div>
            <div className="metric-row">
              <span className="metric-name">Cache Hits:</span>
              <span className="metric-val">{metrics.cache_hits || 0}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function formatDecisionType(type) {
  return type
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function formatTimestamp(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;
  
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  
  if (days > 0) return `${days}d ago`;
  if (hours > 0) return `${hours}h ago`;
  if (minutes > 0) return `${minutes}m ago`;
  return `${seconds}s ago`;
}

export default Observability;
