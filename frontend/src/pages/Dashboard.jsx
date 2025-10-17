import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Target, TrendingUp, Users, Sparkles, Calendar, ArrowUp } from 'lucide-react';
import { dashboardAPI, campaignsAPI, marketIntelligenceAPI } from '../api/client';
import CampaignModal from '../components/CampaignModal';
import './Dashboard.css';

export default function Dashboard() {
  const navigate = useNavigate();
  const [metrics, setMetrics] = useState(null);
  const [recentCampaigns, setRecentCampaigns] = useState([]);
  const [recentInsights, setRecentInsights] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [metricsRes, campaignsRes, insightsRes] = await Promise.all([
        dashboardAPI.getMetrics(),
        campaignsAPI.getRecent(),
        marketIntelligenceAPI.getRecent(),
      ]);
      setMetrics(metricsRes.data);
      setRecentCampaigns(campaignsRes.data);
      setRecentInsights(insightsRes.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  const statCards = metrics ? [
    { icon: Target, label: 'Active Campaigns', value: metrics.active_campaigns.count, change: metrics.active_campaigns.change },
    { icon: TrendingUp, label: 'Market Insights', value: metrics.market_insights.count, change: metrics.market_insights.change },
    { icon: Users, label: 'Competitor tracking', value: metrics.competitor_tracking.count, change: metrics.competitor_tracking.change },
    { icon: Sparkles, label: 'AI Generations', value: metrics.ai_generations.count, change: metrics.ai_generations.change },
  ] : [];

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
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="stat-card">
              <div className="stat-icon">
                <Icon size={24} />
              </div>
              <div className="stat-content">
                <h3>{stat.value}</h3>
                <p>{stat.label}</p>
                <span className="stat-change">{stat.change}</span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="dashboard-content">
        <div className="section recent-campaigns">
          <div className="section-header">
            <h2>Recent Campaigns</h2>
            <button className="view-all" onClick={() => navigate('/campaigns')}>View all →</button>
          </div>
          <div className="campaigns-list">
            {recentCampaigns.map((campaign) => (
              <div key={campaign.id} className="campaign-card">
                <div className="campaign-header">
                  <h3>{campaign.name}</h3>
                  <span className={`status-badge ${campaign.status}`}>{campaign.status}</span>
                </div>
                <div className="campaign-theme">
                  <span className="theme-icon">💡</span>
                  <span>{campaign.theme}</span>
                </div>
                <div className="campaign-meta">
                  <span><Calendar size={14} /> {campaign.start_date} - {campaign.end_date}</span>
                  {campaign.metrics && (
                    <span><ArrowUp size={14} /> {campaign.metrics.engagement || campaign.metrics.leads || campaign.metrics.conversions}</span>
                  )}
                </div>
                <div className="campaign-channels">
                  {campaign.channel_mix.slice(0, 4).map((channel, idx) => (
                    <span key={idx} className="channel-tag">{channel.channel}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="section latest-intelligence">
          <div className="section-header">
            <h2>Latest Intelligence</h2>
            <button className="view-all" onClick={() => navigate('/market-intelligence')}>View all →</button>
          </div>
          <div className="insights-list">
            {recentInsights.map((insight) => (
              <div key={insight.id} className="insight-item">
                <div className="insight-icon">
                  <TrendingUp size={20} />
                </div>
                <div className="insight-content">
                  <h4>{insight.content.split('.')[0]}</h4>
                  <div className="insight-meta">
                    <span className="insight-source">{insight.source}</span>
                    <span className="insight-time">{new Date(insight.timestamp).toLocaleTimeString()}</span>
                  </div>
                </div>
                <span className={`impact-badge ${insight.impact}`}>{insight.impact} impact</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <CampaignModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onSuccess={loadData} />
    </div>
  );
}
