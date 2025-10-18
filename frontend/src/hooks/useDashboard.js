import { useState, useEffect, useCallback } from 'react';
import { dashboardAPI, campaignsAPI, marketIntelligenceAPI } from '../api/client';

export function useDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [recentCampaigns, setRecentCampaigns] = useState([]);
  const [recentInsights, setRecentInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [metricsRes, campaignsRes, insightsRes] = await Promise.all([
        dashboardAPI.getMetrics(),
        campaignsAPI.getRecent(),
        marketIntelligenceAPI.getRecent(),
      ]);
      
      setMetrics(metricsRes.data);
      setRecentCampaigns(campaignsRes.data.campaigns || []);
      setRecentInsights(insightsRes.data || []);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
      console.error('Error loading dashboard:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const getStatCards = useCallback(() => {
    if (!metrics) return [];
    
    return [
      { 
        iconName: 'Target', 
        label: 'Active Campaigns', 
        value: metrics.active_campaigns.count, 
        change: metrics.active_campaigns.change 
      },
      { 
        iconName: 'TrendingUp', 
        label: 'Market Insights', 
        value: metrics.market_insights.count, 
        change: metrics.market_insights.change 
      },
      { 
        iconName: 'Users', 
        label: 'Competitor tracking', 
        value: metrics.competitor_tracking.count, 
        change: metrics.competitor_tracking.change 
      },
      { 
        iconName: 'Sparkles', 
        label: 'AI Generations', 
        value: metrics.ai_generations.count, 
        change: metrics.ai_generations.change 
      },
    ];
  }, [metrics]);

  return {
    metrics,
    recentCampaigns,
    recentInsights,
    loading,
    error,
    reload: loadData,
    getStatCards,
  };
}
