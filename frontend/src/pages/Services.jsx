import { useState } from 'react';
import { Sparkles } from 'lucide-react';
import { useServices } from '../hooks';
import CampaignModal from '../components/CampaignModal';
import './Services.css';

const getCategoryIcon = (category) => {
  const icons = {
    'Security': '🔒',
    'Cloud Infrastructure': '☁️',
    'Artificial Intelligence': '🤖',
    'Data & Analytics': '📊',
    'Edge & IoT': '📡',
  };
  return icons[category] || '⚙️';
};

function ServiceCard({ service, onGenerateCampaign }) {
  return (
    <div className="service-card">
      <div className="service-header">
        <div className="service-icon">
          <span>{getCategoryIcon(service.category)}</span>
        </div>
        <button className="btn-generate-service" onClick={onGenerateCampaign}>
          <Sparkles size={16} />
          Generate Campaign
        </button>
      </div>
      
      <div className="service-info">
        <h3>{service.name}</h3>
        <span className="service-category">{service.category}</span>
        <p className="service-description">{service.description}</p>
      </div>

      <div className="service-stats">
        <div className="stat-item">
          <span className="stat-label">Market Mentions</span>
          <span className="stat-value">
            {service.market_mentions} <span className="stat-trend">+34%</span>
          </span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Active Campaigns</span>
          <span className="stat-value">{service.active_campaigns}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Tracked Competitors</span>
          <span className="stat-value">{service.competitors?.length || 0}</span>
        </div>
      </div>

      {service.competitors && service.competitors.length > 0 && (
        <div className="service-competitors">
          <span className="label">Key Competitors:</span>
          <div className="competitors-tags">
            {service.competitors.map((comp, idx) => (
              <span key={idx} className="comp-tag">{comp}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function Services() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { services, loading, error, reload } = useServices();

  const totalMentions = services.reduce((sum, s) => sum + (s.market_mentions || 0), 0);
  const totalCampaigns = services.reduce((sum, s) => sum + (s.active_campaigns || 0), 0);

  if (error) {
    return (
      <div className="services-page">
        <div className="error-message">
          Error loading services: {error}
          <button onClick={reload}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="services-page">
      <div className="page-header">
        <div>
          <h1>Service Catalog</h1>
          <p>50+ enterprise services tracked across cloud infrastructure, security, and AI platforms</p>
        </div>
      </div>

      <div className="services-stats">
        <div className="stat-box">
          <h3>{services.length}+</h3>
          <p>Active Services</p>
        </div>
        <div className="stat-box">
          <h3>{totalMentions.toLocaleString()}</h3>
          <p>Total Mentions</p>
        </div>
        <div className="stat-box">
          <h3>{totalCampaigns}</h3>
          <p>Active Campaigns</p>
        </div>
        <div className="stat-box">
          <h3>+52%</h3>
          <p>Average Growth</p>
        </div>
      </div>

      <div className="services-list">
        {loading && services.length === 0 ? (
          <div>Loading services...</div>
        ) : (
          services.map((service) => (
            <ServiceCard 
              key={service.id} 
              service={service} 
              onGenerateCampaign={() => setIsModalOpen(true)}
            />
          ))
        )}
      </div>

      <CampaignModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onSuccess={reload} 
      />
    </div>
  );
}
