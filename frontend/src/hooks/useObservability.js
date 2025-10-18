import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';

export default function useObservability() {
  const [decisions, setDecisions] = useState([]);
  const [traces, setTraces] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchObservabilityData();
  }, []);

  const fetchObservabilityData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [decisionsRes, tracesRes, decisionStatsRes, traceStatsRes] = await Promise.all([
        apiClient.get('/audit/decisions/recent?limit=50'),
        apiClient.get('/audit/traces/recent?limit=50'),
        apiClient.get('/audit/stats/decisions'),
        apiClient.get('/audit/stats/traces')
      ]);

      setDecisions(decisionsRes.data);
      setTraces(tracesRes.data);

      const combinedStats = {
        total_decisions: decisionStatsRes.data.total_decisions,
        total_traces: traceStatsRes.data.total_traces,
        success_rate: traceStatsRes.data.success_rate?.toFixed(1) || 0,
        avg_confidence: decisionStatsRes.data.average_confidence,
        avg_duration: traceStatsRes.data.average_duration_ms?.toFixed(0) || 0,
        by_type: decisionStatsRes.data.by_type || {}
      };

      setStats(combinedStats);

      const metricsData = {
        total_execution_time_ms: tracesRes.data.reduce((sum, t) => sum + (t.total_duration_ms || 0), 0),
        total_steps: tracesRes.data.reduce((sum, t) => sum + (t.steps?.length || 0), 0),
        api_calls_count: tracesRes.data.length,
        total_tokens_used: 0,
        cache_hits: 0
      };

      setMetrics(metricsData);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching observability data:', err);
      setError(err.message || 'Failed to fetch observability data');
      setLoading(false);
    }
  };

  const refresh = () => {
    fetchObservabilityData();
  };

  return {
    decisions,
    traces,
    metrics,
    stats,
    loading,
    error,
    refresh
  };
}
