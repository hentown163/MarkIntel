import { useState, useEffect } from 'react';
import { Sparkles, Search, Plus } from 'lucide-react';
import { campaignsAPI } from '../api/client';
import CampaignModal from '../components/CampaignModal';
import './Campaigns.css';

export default function Campaigns() {
  const [campaigns, setCampaigns] = useState([]);
  const [filter, setFilter] = useState('all');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      const res = await campaignsAPI.getAll();
      setCampaigns(res.data);
    } catch (error) {
      console.error('Error loading campaigns:', error);
    }
  };

  const filteredCampaigns = filter === 'all' 
    ? campaigns 
    : campaigns.filter(c => c.status === filter);

  return (
    <div className="campaigns-page">
      <div className="page-header">
        <div>
          <h1>Campaign Library</h1>
          <p>AI-generated campaigns with themes, timelines, and channel strategies</p>
        </div>
        <button className="btn-generate" onClick={() => setIsModalOpen(true)}>
          <Sparkles size={18} />
          Generate New Campaign
        </button>
      </div>

      <div className="campaigns-controls">
        <div className="search-bar">
          <Search size={18} />
          <input type="text" placeholder="Search campaigns by title, theme, or channel..." />
        </div>
        <div className="filter-buttons">
          <button className={filter === 'all' ? 'active' : ''} onClick={() => setFilter('all')}>
            All Campaigns ({campaigns.length})
          </button>
          <button className={filter === 'active' ? 'active' : ''} onClick={() => setFilter('active')}>
            Active ({campaigns.filter(c => c.status === 'active').length})
          </button>
          <button className={filter === 'draft' ? 'active' : ''} onClick={() => setFilter('draft')}>
            Draft ({campaigns.filter(c => c.status === 'draft').length})
          </button>
          <button className={filter === 'completed' ? 'active' : ''} onClick={() => setFilter('completed')}>
            Completed ({campaigns.filter(c => c.status === 'completed').length})
          </button>
        </div>
      </div>

      <div className="campaigns-grid">
        {filteredCampaigns.map((campaign) => (
          <div key={campaign.id} className="campaign-item">
            <div className="campaign-item-header">
              <h3>{campaign.name}</h3>
              <span className={`status-badge ${campaign.status}`}>{campaign.status}</span>
            </div>
            <div className="campaign-theme">
              <span className="theme-icon">💡</span>
              <span>{campaign.theme}</span>
            </div>
            <div className="campaign-dates">
              📅 {campaign.start_date} - {campaign.end_date}
            </div>
            {campaign.metrics && (
              <div className="campaign-metrics">
                📈 {campaign.metrics.engagement || campaign.metrics.leads || campaign.metrics.conversions}
              </div>
            )}
            <div className="campaign-channels-grid">
              {campaign.channel_mix.map((channel, idx) => (
                <span key={idx} className="channel-badge">{channel.channel}</span>
              ))}
            </div>
          </div>
        ))}
      </div>

      <CampaignModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onSuccess={loadCampaigns} />
    </div>
  );
}
