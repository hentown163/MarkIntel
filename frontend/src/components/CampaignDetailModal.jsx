import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { X, RefreshCw, ThumbsUp, ThumbsDown, Calendar, DollarSign, TrendingUp, Target, Lightbulb, Edit, Trash2 } from 'lucide-react';
import { campaignsAPI } from '../api/client';
import './CampaignModal.css';

export default function CampaignDetailModal({ campaign, isOpen, onClose, onUpdate }) {
  const [regenerating, setRegenerating] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [currentCampaign, setCurrentCampaign] = useState(campaign);

  useEffect(() => {
    if (campaign) {
      setCurrentCampaign(campaign);
    }
  }, [campaign]);

  if (!isOpen || !campaign) return null;

  const handleRegenerateIdeas = async () => {
    try {
      setRegenerating('ideas');
      const response = await campaignsAPI.regenerateIdeas(campaign.id);
      setCurrentCampaign(response.data);
      if (onUpdate) {
        await onUpdate(response.data);
      }
      alert('Campaign ideas regenerated successfully!');
    } catch (error) {
      console.error('Error regenerating ideas:', error);
      alert('Failed to regenerate ideas. Please try again.');
    } finally {
      setRegenerating(null);
    }
  };

  const handleRegenerateChannels = async () => {
    try {
      setRegenerating('channels');
      const response = await campaignsAPI.regenerateStrategies(campaign.id);
      setCurrentCampaign(response.data);
      if (onUpdate) {
        await onUpdate(response.data);
      }
      alert('Channel strategies regenerated successfully!');
    } catch (error) {
      console.error('Error regenerating strategies:', error);
      alert('Failed to regenerate channel strategies. Please try again.');
    } finally {
      setRegenerating(null);
    }
  };

  const handleFeedback = async (type) => {
    try {
      setFeedback(type);
      await campaignsAPI.submitFeedback(campaign.id, {
        feedback_type: type,
        comment: `User ${type === 'positive' ? 'liked' : 'disliked'} this campaign`
      });
      alert(`Thank you for your ${type} feedback! This helps improve future campaigns.`);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setTimeout(() => setFeedback(null), 1500);
    }
  };

  const handleDelete = async () => {
    if (!confirm(`Are you sure you want to delete "${displayCampaign.name}"? This action cannot be undone.`)) {
      return;
    }
    
    try {
      setIsDeleting(true);
      await campaignsAPI.delete(displayCampaign.id);
      alert('Campaign deleted successfully!');
      if (onUpdate) {
        await onUpdate();
      }
      onClose();
    } catch (error) {
      console.error('Error deleting campaign:', error);
      alert('Failed to delete campaign. Please try again.');
    } finally {
      setIsDeleting(false);
    }
  };

  const displayCampaign = currentCampaign || campaign;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content campaign-detail-modal" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '900px' }}>
        <div className="modal-header">
          <div className="modal-title">
            <h2>{displayCampaign.name}</h2>
            <span className={`status-badge ${displayCampaign.status}`} style={{ marginLeft: '1rem' }}>{displayCampaign.status}</span>
          </div>
          <button className="modal-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div style={{ padding: '1.5rem 0' }}>
          <div className="campaign-detail-section">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.1rem' }}>
                <Lightbulb size={20} style={{ color: '#3b82f6' }} />
                Campaign Theme
              </h3>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button 
                  onClick={() => handleFeedback('positive')}
                  style={{ 
                    background: feedback === 'positive' ? '#22c55e' : '#1a2332',
                    border: '1px solid #2a3544',
                    padding: '0.5rem',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    color: '#fff'
                  }}
                  title="Like this campaign"
                >
                  <ThumbsUp size={16} />
                </button>
                <button 
                  onClick={() => handleFeedback('negative')}
                  style={{ 
                    background: feedback === 'negative' ? '#ef4444' : '#1a2332',
                    border: '1px solid #2a3544',
                    padding: '0.5rem',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    color: '#fff'
                  }}
                  title="Dislike this campaign"
                >
                  <ThumbsDown size={16} />
                </button>
              </div>
            </div>
            <div style={{ 
              padding: '1rem', 
              backgroundColor: '#1a2332', 
              borderRadius: '8px',
              border: '1px solid #2a3544'
            }}>
              <p style={{ fontSize: '1.2rem', fontWeight: '600', color: '#fff', marginBottom: '0.5rem' }}>
                {displayCampaign.theme}
              </p>
            </div>
          </div>

          <div className="campaign-detail-section" style={{ marginTop: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.1rem' }}>
                <Target size={20} style={{ color: '#3b82f6' }} />
                Campaign Ideas
              </h3>
              <button 
                onClick={handleRegenerateIdeas}
                disabled={regenerating === 'ideas'}
                style={{ 
                  background: '#3b82f6',
                  border: 'none',
                  padding: '0.5rem 1rem',
                  borderRadius: '6px',
                  cursor: regenerating === 'ideas' ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  color: '#fff',
                  opacity: regenerating === 'ideas' ? 0.6 : 1
                }}
              >
                <RefreshCw size={16} className={regenerating === 'ideas' ? 'spin' : ''} />
                {regenerating === 'ideas' ? 'Regenerating...' : 'Regenerate Ideas'}
              </button>
            </div>
            <div style={{ 
              padding: '1rem', 
              backgroundColor: '#1a2332', 
              borderRadius: '8px',
              border: '1px solid #2a3544',
              display: 'grid',
              gap: '1rem'
            }}>
              {displayCampaign.ideas && displayCampaign.ideas.map((idea, idx) => (
                <div key={idx} style={{ 
                  padding: '1rem',
                  backgroundColor: '#0f172a',
                  borderRadius: '6px',
                  border: '1px solid #1e293b'
                }}>
                  <h4 style={{ color: '#3b82f6', marginBottom: '0.5rem' }}>{idea.theme}</h4>
                  <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginBottom: '0.5rem' }}>{idea.core_message}</p>
                  <p style={{ color: '#64748b', fontSize: '0.85rem', fontStyle: 'italic' }}>
                    Competitive Angle: {idea.competitive_angle}
                  </p>
                  <div style={{ marginTop: '0.5rem', display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {idea.target_segments && idea.target_segments.map((segment, sidx) => (
                      <span key={sidx} style={{ 
                        background: '#1e293b', 
                        padding: '0.25rem 0.75rem', 
                        borderRadius: '999px',
                        fontSize: '0.75rem',
                        color: '#94a3b8'
                      }}>
                        {segment}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="campaign-detail-section" style={{ marginTop: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.1rem' }}>
                <TrendingUp size={20} style={{ color: '#3b82f6' }} />
                Channel Strategy
              </h3>
              <button 
                onClick={handleRegenerateChannels}
                disabled={regenerating === 'channels'}
                style={{ 
                  background: '#3b82f6',
                  border: 'none',
                  padding: '0.5rem 1rem',
                  borderRadius: '6px',
                  cursor: regenerating === 'channels' ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  color: '#fff',
                  opacity: regenerating === 'channels' ? 0.6 : 1
                }}
              >
                <RefreshCw size={16} className={regenerating === 'channels' ? 'spin' : ''} />
                {regenerating === 'channels' ? 'Regenerating...' : 'Regenerate Channels'}
              </button>
            </div>
            <div style={{ 
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '1rem'
            }}>
              {displayCampaign.channel_mix && displayCampaign.channel_mix.map((channel, idx) => (
                <div key={idx} style={{ 
                  padding: '1rem',
                  backgroundColor: '#1a2332',
                  borderRadius: '8px',
                  border: '1px solid #2a3544'
                }}>
                  <h4 style={{ color: '#fff', marginBottom: '0.5rem' }}>{channel.channel}</h4>
                  <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '0.5rem' }}>
                    {channel.content_type}
                  </p>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.75rem' }}>
                    <span style={{ color: '#64748b', fontSize: '0.8rem' }}>{channel.frequency}</span>
                    <span style={{ color: '#3b82f6', fontSize: '0.9rem', fontWeight: '600' }}>
                      {Math.round(channel.budget_allocation * 100)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="campaign-detail-section" style={{ marginTop: '1.5rem' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.1rem', marginBottom: '1rem' }}>
              <Calendar size={20} style={{ color: '#3b82f6' }} />
              Campaign Details
            </h3>
            <div style={{ 
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '1rem'
            }}>
              <div style={{ 
                padding: '1rem',
                backgroundColor: '#1a2332',
                borderRadius: '8px',
                border: '1px solid #2a3544'
              }}>
                <p style={{ color: '#64748b', fontSize: '0.85rem', marginBottom: '0.25rem' }}>Duration</p>
                <p style={{ color: '#fff', fontSize: '1rem' }}>
                  {displayCampaign.start_date} - {displayCampaign.end_date}
                </p>
              </div>
              <div style={{ 
                padding: '1rem',
                backgroundColor: '#1a2332',
                borderRadius: '8px',
                border: '1px solid #2a3544'
              }}>
                <p style={{ color: '#64748b', fontSize: '0.85rem', marginBottom: '0.25rem' }}>Budget</p>
                <p style={{ color: '#fff', fontSize: '1rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                  <DollarSign size={16} />
                  {displayCampaign.total_budget || 'TBD'}
                </p>
              </div>
              <div style={{ 
                padding: '1rem',
                backgroundColor: '#1a2332',
                borderRadius: '8px',
                border: '1px solid #2a3544'
              }}>
                <p style={{ color: '#64748b', fontSize: '0.85rem', marginBottom: '0.25rem' }}>Expected ROI</p>
                <p style={{ color: '#22c55e', fontSize: '1rem', fontWeight: '600' }}>
                  {displayCampaign.expected_roi ? `${displayCampaign.expected_roi}%` : 'TBD'}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="modal-footer" style={{ display: 'flex', justifyContent: 'space-between' }}>
          <button 
            className="btn-secondary" 
            onClick={handleDelete}
            disabled={isDeleting}
            style={{ 
              background: '#ef4444',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              opacity: isDeleting ? 0.6 : 1
            }}
          >
            <Trash2 size={16} />
            {isDeleting ? 'Deleting...' : 'Delete Campaign'}
          </button>
          <button className="btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

CampaignDetailModal.propTypes = {
  campaign: PropTypes.object,
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onUpdate: PropTypes.func,
};
