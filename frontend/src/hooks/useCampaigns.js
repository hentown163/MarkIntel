import { useState, useEffect, useCallback } from 'react';
import { campaignsAPI } from '../api/client';

export function useCampaigns() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadCampaigns = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await campaignsAPI.getAll();
      setCampaigns(response.data.campaigns || []);
    } catch (err) {
      setError(err.message || 'Failed to load campaigns');
      console.error('Error loading campaigns:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCampaigns();
  }, [loadCampaigns]);

  const generateCampaign = useCallback(async (data) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await campaignsAPI.generate(data);
      await loadCampaigns();
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to generate campaign';
      setError(errorMessage);
      console.error('Error generating campaign:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [loadCampaigns]);

  const getCampaignById = useCallback(async (id) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await campaignsAPI.getById(id);
      return response.data;
    } catch (err) {
      setError(err.message || 'Failed to load campaign');
      console.error('Error loading campaign:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    campaigns,
    loading,
    error,
    reload: loadCampaigns,
    generateCampaign,
    getCampaignById,
  };
}
