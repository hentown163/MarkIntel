import { useState, useEffect, useCallback } from 'react';
import { marketIntelligenceAPI } from '../api/client';

export function useMarketIntelligence() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadSignals = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await marketIntelligenceAPI.getAll();
      setSignals(response.data || []);
    } catch (err) {
      setError(err.message || 'Failed to load market intelligence');
      console.error('Error loading market intelligence:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSignals();
  }, [loadSignals]);

  const filterByImpact = useCallback((impact) => {
    return signals.filter(signal => signal.impact === impact);
  }, [signals]);

  const filterByCategory = useCallback((category) => {
    return signals.filter(signal => signal.category === category);
  }, [signals]);

  const getHighImpactSignals = useCallback(() => {
    return filterByImpact('high');
  }, [filterByImpact]);

  return {
    signals,
    loading,
    error,
    reload: loadSignals,
    filterByImpact,
    filterByCategory,
    getHighImpactSignals,
  };
}
