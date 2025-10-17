import { useState } from 'react';
import { X, Sparkles } from 'lucide-react';
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
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await campaignsAPI.generate(formData);
      onSuccess?.();
      onClose();
      setFormData({
        product_service: '',
        target_audience: '',
        competitors: '',
        additional_context: '',
        duration_days: 30,
      });
    } catch (error) {
      console.error('Error generating campaign:', error);
    } finally {
      setIsSubmitting(false);
    }
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
          <button className="modal-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <p className="modal-description">
          Provide details about your product/service and target market. Our AI will generate a
          comprehensive campaign strategy.
        </p>

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="product_service">Product/Service *</label>
            <input
              type="text"
              id="product_service"
              placeholder="e.g., Cloud Security Platform, AI Analytics Tool"
              value={formData.product_service}
              onChange={(e) => setFormData({ ...formData, product_service: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="target_audience">Target Audience *</label>
            <input
              type="text"
              id="target_audience"
              placeholder="e.g., Enterprise CIOs, SMB Technology Managers"
              value={formData.target_audience}
              onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="competitors">Key Competitors (Optional)</label>
            <input
              type="text"
              id="competitors"
              placeholder="e.g., AWS, Azure, Google Cloud"
              value={formData.competitors}
              onChange={(e) => setFormData({ ...formData, competitors: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label htmlFor="additional_context">Additional Context (Optional)</label>
            <textarea
              id="additional_context"
              placeholder="Any specific market trends, recent announcements, or strategic goals..."
              rows={4}
              value={formData.additional_context}
              onChange={(e) => setFormData({ ...formData, additional_context: e.target.value })}
            />
          </div>

          <div className="modal-footer">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={isSubmitting}>
              <Sparkles size={16} />
              {isSubmitting ? 'Generating...' : 'Generate Campaign'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
