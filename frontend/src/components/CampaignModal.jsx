import { useState } from 'react';
import PropTypes from 'prop-types';
import { X, Sparkles, CheckCircle, Loader } from 'lucide-react';
import { campaignsAPI } from '../api/client';
import './CampaignModal.css';

export default function CampaignModal({ isOpen, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    product_service: '',
    target_audience: '',
    competitors: '',
    additional_context: '',
    duration_days: 30,
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generationProgress, setGenerationProgress] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    setGenerationProgress([]);
    
    const steps = [
      'Analyzing market signals...',
      'Generating campaign ideas...',
      'Optimizing channel mix...',
      'Creating campaign plan...',
      'Finalizing strategy...'
    ];

    let currentStep = 0;
    const progressInterval = setInterval(() => {
      if (currentStep < steps.length - 1) {
        setGenerationProgress(prev => [...prev, steps[currentStep]]);
        currentStep++;
      }
    }, 800);
    
    try {
      await campaignsAPI.generate(formData);
      clearInterval(progressInterval);
      setGenerationProgress(steps);
      
      setTimeout(() => {
        setFormData({
          product_service: '',
          target_audience: '',
          competitors: '',
          additional_context: '',
          duration_days: 30,
        });
        setGenerationProgress([]);
        onSuccess?.();
        onClose();
      }, 500);
    } catch (err) {
      clearInterval(progressInterval);
      setError(err.response?.data?.detail || err.message || 'Failed to generate campaign');
      setGenerationProgress([]);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <Sparkles size={20} />
            <h2>Generate AI Campaign</h2>
          </div>
          <button className="modal-close" onClick={onClose} disabled={loading}>
            <X size={20} />
          </button>
        </div>

        <p className="modal-description">
          Provide details about your product/service and target market. Our AI will generate a
          comprehensive campaign strategy.
        </p>

        {error && (
          <div className="error-message" style={{ marginBottom: '1rem', padding: '0.75rem', backgroundColor: '#fee', color: '#c00', borderRadius: '4px' }}>
            {error}
          </div>
        )}

        {loading && generationProgress.length > 0 && (
          <div className="progress-container" style={{ 
            marginBottom: '1rem', 
            padding: '1rem', 
            backgroundColor: '#1a2332', 
            borderRadius: '8px',
            border: '1px solid #2a3544'
          }}>
            <h3 style={{ fontSize: '0.9rem', marginBottom: '0.75rem', color: '#94a3b8' }}>Generation Progress</h3>
            {generationProgress.map((step, idx) => (
              <div key={idx} style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem', 
                marginBottom: '0.5rem',
                color: '#94a3b8'
              }}>
                <CheckCircle size={16} style={{ color: '#22c55e' }} />
                <span style={{ fontSize: '0.85rem' }}>{step}</span>
              </div>
            ))}
            {generationProgress.length < 5 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#94a3b8' }}>
                <Loader size={16} className="spin" style={{ color: '#3b82f6' }} />
                <span style={{ fontSize: '0.85rem' }}>Working...</span>
              </div>
            )}
          </div>
        )}

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="product_service">Product/Service *</label>
            <input
              type="text"
              id="product_service"
              placeholder="e.g., Cloud Security Platform, AI Analytics Tool"
              value={formData.product_service}
              onChange={(e) => handleChange('product_service', e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="target_audience">Target Audience *</label>
            <input
              type="text"
              id="target_audience"
              placeholder="e.g., Enterprise CIOs, SMB Technology Managers"
              value={formData.target_audience}
              onChange={(e) => handleChange('target_audience', e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="competitors">Key Competitors (Optional)</label>
            <input
              type="text"
              id="competitors"
              placeholder="e.g., AWS, Azure, Google Cloud"
              value={formData.competitors}
              onChange={(e) => handleChange('competitors', e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="additional_context">Additional Context (Optional)</label>
            <textarea
              id="additional_context"
              placeholder="Any specific market trends, recent announcements, or strategic goals..."
              rows={4}
              value={formData.additional_context}
              onChange={(e) => handleChange('additional_context', e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="modal-footer">
            <button type="button" className="btn-secondary" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              <Sparkles size={16} />
              {loading ? 'Generating...' : 'Generate Campaign'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

CampaignModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSuccess: PropTypes.func,
};
