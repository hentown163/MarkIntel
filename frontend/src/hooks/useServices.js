import { useState, useEffect, useCallback } from 'react';
import { servicesAPI } from '../api/client';

export function useServices() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadServices = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await servicesAPI.getAll();
      setServices(response.data || []);
    } catch (err) {
      setError(err.message || 'Failed to load services');
      console.error('Error loading services:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadServices();
  }, [loadServices]);

  const getServiceById = useCallback(async (id) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await servicesAPI.getById(id);
      return response.data;
    } catch (err) {
      setError(err.message || 'Failed to load service');
      console.error('Error loading service:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    services,
    loading,
    error,
    reload: loadServices,
    getServiceById,
  };
}
