import { useState } from 'react';
import { Sparkles, Search, Download, Trash2 } from 'lucide-react';
import { useCampaigns } from '../hooks';
import CampaignModal from '../components/CampaignModal';
import CampaignDetailModal from '../components/CampaignDetailModal';
import CampaignCard from '../components/CampaignCard';
import './Campaigns.css';
import axios from 'axios';

export default function Campaigns() {
  const [filter, setFilter] = useState('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedIds, setSelectedIds] = useState(new Set());
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

  const handleExport = async (format) => {
    try {
      const response = await axios.get(`/api/export/campaigns?format=${format}`, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `campaigns.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Export error:', error);
    }
  };

  const toggleSelect = (id) => {
    const newSelected = new Set(selectedIds);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedIds(newSelected);
  };

  const selectAll = () => {
    if (selectedIds.size === filteredCampaigns.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(filteredCampaigns.map(c => c.id)));
    }
  };

  const handleBulkDelete = async () => {
    if (!window.confirm(`Delete ${selectedIds.size} campaigns?`)) return;
    
    try {
      await axios.post('/api/campaigns/bulk-delete', Array.from(selectedIds));
      setSelectedIds(new Set());
      await reload();
    } catch (error) {
      console.error('Bulk delete error:', error);
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
        <div style={{ display: 'flex', gap: '10px' }}>
          {selectedIds.size > 0 && (
            <button className="btn-danger" onClick={handleBulkDelete}>
              <Trash2 size={18} />
              Delete {selectedIds.size}
            </button>
          )}
          <button className="btn-secondary" onClick={() => handleExport('csv')}>
            <Download size={18} />
            Export CSV
          </button>
          <button className="btn-generate" onClick={() => setIsModalOpen(true)}>
            <Sparkles size={18} />
            Generate New Campaign
          </button>
        </div>
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
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {filteredCampaigns.length > 0 && (
            <label style={{ display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer' }}>
              <input 
                type="checkbox" 
                checked={selectedIds.size === filteredCampaigns.length && filteredCampaigns.length > 0}
                onChange={selectAll}
              />
              Select All
            </label>
          )}
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
      </div>

      <div className="campaigns-grid">
        {loading && campaigns.length === 0 ? (
          <div>Loading campaigns...</div>
        ) : filteredCampaigns.length === 0 ? (
          <div>No campaigns found. Try generating one!</div>
        ) : (
          filteredCampaigns.map((campaign) => (
            <div key={campaign.id} className="campaign-item" style={{ position: 'relative' }}>
              <input 
                type="checkbox"
                style={{ position: 'absolute', top: '10px', right: '10px', zIndex: 10, cursor: 'pointer' }}
                checked={selectedIds.has(campaign.id)}
                onChange={(e) => {
                  e.stopPropagation();
                  toggleSelect(campaign.id);
                }}
              />
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
