import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles } from 'lucide-react';
import { useDashboard } from '../hooks';
import CampaignModal from '../components/CampaignModal';
import StatCard from '../components/StatCard';
import CampaignCard from '../components/CampaignCard';
import InsightItem from '../components/InsightItem';
import './Dashboard.css';

export default function Dashboard() {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { recentCampaigns, recentInsights, loading, error, reload, getStatCards } = useDashboard();
  
  const statCards = getStatCards();

  if (error) {
    return (
      <div className="dashboard">
        <div className="error-message">
          Error loading dashboard: {error}
          <button onClick={reload}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h1>Welcome to NexusPlanner</h1>
          <p>Autonomous AI-powered marketing intelligence for CloudScale Inc.</p>
        </div>
        <button className="btn-generate" onClick={() => setIsModalOpen(true)}>
          <Sparkles size={18} />
          Generate Campaign
        </button>
      </div>

      <div className="stats-grid">
        {loading && statCards.length === 0 ? (
          <div>Loading metrics...</div>
        ) : (
          statCards.map((stat, index) => (
            <StatCard 
              key={index} 
              iconName={stat.iconName} 
              label={stat.label} 
              value={stat.value} 
              change={stat.change} 
            />
          ))
        )}
      </div>

      <div className="dashboard-content">
        <div className="section recent-campaigns">
          <div className="section-header">
            <h2>Recent Campaigns</h2>
            <button className="view-all" onClick={() => navigate('/campaigns')}>View all →</button>
          </div>
          <div className="campaigns-list">
            {loading && recentCampaigns.length === 0 ? (
              <div>Loading campaigns...</div>
            ) : recentCampaigns.length === 0 ? (
              <div>No campaigns yet. Generate your first campaign!</div>
            ) : (
              recentCampaigns.map((campaign) => (
                <CampaignCard key={campaign.id} campaign={campaign} />
              ))
            )}
          </div>
        </div>

        <div className="section latest-intelligence">
          <div className="section-header">
            <h2>Latest Intelligence</h2>
            <button className="view-all" onClick={() => navigate('/market-intelligence')}>View all →</button>
          </div>
          <div className="insights-list">
            {loading && recentInsights.length === 0 ? (
              <div>Loading insights...</div>
            ) : (
              recentInsights.map((insight) => (
                <InsightItem key={insight.id} insight={insight} />
              ))
            )}
          </div>
        </div>
      </div>

      <CampaignModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onSuccess={reload} 
      />
    </div>
  );
}
