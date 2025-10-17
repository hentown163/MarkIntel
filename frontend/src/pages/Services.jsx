import { useState, useEffect } from 'react';
import { Sparkles } from 'lucide-react';
import { servicesAPI } from '../api/client';
import CampaignModal from '../components/CampaignModal';
import './Services.css';

export default function Services() {
  const [services, setServices] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    loadServices();
  }, []);

  const loadServices = async () => {
    try {
      const res = await servicesAPI.getAll();
      setServices(res.data);
    } catch (error) {
      console.error('Error loading services:', error);
    }
  };

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
          <h3>50+</h3>
          <p>Active Services</p>
        </div>
        <div className="stat-box">
          <h3>1,312</h3>
          <p>Total Mentions</p>
        </div>
        <div className="stat-box">
          <h3>44</h3>
          <p>Active Campaigns</p>
        </div>
        <div className="stat-box">
          <h3>+52%</h3>
          <p>Average Growth</p>
        </div>
      </div>

      <div className="services-list">
        {services.map((service) => (
          <div key={service.id} className="service-card">
            <div className="service-header">
              <div className="service-icon">
                <span>{service.category === 'Security' ? '🔒' : service.category === 'Cloud Infrastructure' ? '☁️' : service.category === 'Artificial Intelligence' ? '🤖' : service.category === 'Data & Analytics' ? '📊' : service.category === 'Edge & IoT' ? '📡' : '⚙️'}</span>
              </div>
              <button className="btn-generate-service" onClick={() => setIsModalOpen(true)}>
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
                <span className="stat-value">{service.market_mentions} <span className="stat-trend">+34%</span></span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Active Campaigns</span>
                <span className="stat-value">{service.active_campaigns}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Backed Competitors</span>
                <span className="stat-value">{service.backed_competitors}</span>
              </div>
            </div>

            <div className="service-competitors">
              <span className="label">Key Competitors:</span>
              <div className="competitors-tags">
                {service.competitors?.map((comp, idx) => (
                  <span key={idx} className="comp-tag">{comp}</span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      <CampaignModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onSuccess={loadServices} />
    </div>
  );
}
