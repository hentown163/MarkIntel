import { useState } from 'react';
import { Sparkles, Search } from 'lucide-react';
import { useCampaigns } from '../hooks';
import CampaignModal from '../components/CampaignModal';
import CampaignDetailModal from '../components/CampaignDetailModal';
import CampaignCard from '../components/CampaignCard';
import './Campaigns.css';

export default function Campaigns() {
  const [filter, setFilter] = useState('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const { campaigns, loading, error, reload } = useCampaigns();

  const filteredCampaigns = campaigns.filter(campaign => {
    const matchesFilter = filter === 'all' || campaign.status === filter;
    const matchesSearch = !searchQuery || 
      campaign.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      campaign.theme?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      campaign.channel_mix?.some(ch => ch.channel?.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesFilter && matchesSearch;
  });

  const getCountByStatus = (status) => {
    return campaigns.filter(c => c.status === status).length;
  };

  const handleCampaignClick = (campaign) => {
    setSelectedCampaign(campaign);
  };

  const handleCampaignUpdate = async (updatedCampaign) => {
    await reload();
    if (updatedCampaign) {
      setSelectedCampaign(updatedCampaign);
    }
  };

  if (error) {
    return (
      <div className="campaigns-page">
        <div className="error-message">
          Error loading campaigns: {error}
          <button onClick={reload}>Retry</button>
        </div>
      </div>
    );
  }

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
          <input 
            type="text" 
            placeholder="Search campaigns by title, theme, or channel..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="filter-buttons">
          <button className={filter === 'all' ? 'active' : ''} onClick={() => setFilter('all')}>
            All Campaigns ({campaigns.length})
          </button>
          <button className={filter === 'active' ? 'active' : ''} onClick={() => setFilter('active')}>
            Active ({getCountByStatus('active')})
          </button>
          <button className={filter === 'draft' ? 'active' : ''} onClick={() => setFilter('draft')}>
            Draft ({getCountByStatus('draft')})
          </button>
          <button className={filter === 'completed' ? 'active' : ''} onClick={() => setFilter('completed')}>
            Completed ({getCountByStatus('completed')})
          </button>
        </div>
      </div>

      <div className="campaigns-grid">
        {loading && campaigns.length === 0 ? (
          <div>Loading campaigns...</div>
        ) : filteredCampaigns.length === 0 ? (
          <div>No campaigns found. Try generating one!</div>
        ) : (
          filteredCampaigns.map((campaign) => (
            <div key={campaign.id} className="campaign-item">
              <CampaignCard campaign={campaign} onClick={handleCampaignClick} />
            </div>
          ))
        )}
      </div>

      <CampaignModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onSuccess={reload} 
      />

      <CampaignDetailModal
        campaign={selectedCampaign}
        isOpen={!!selectedCampaign}
        onClose={() => setSelectedCampaign(null)}
        onUpdate={handleCampaignUpdate}
      />
    </div>
  );
}
