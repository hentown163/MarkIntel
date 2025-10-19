import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Hero.css';

function Hero() {
  const navigate = useNavigate();
  const [activeTestimonial, setActiveTestimonial] = useState(0);

  const handleGetStarted = () => {
    navigate('/login');
  };

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "CMO, TechVenture Inc.",
      company: "Enterprise SaaS",
      quote: "NexusPlanner transformed how we approach campaign planning. What used to take our team 2 weeks now happens in minutes with better results. The AI-powered insights are incredible.",
      avatar: "SC"
    },
    {
      name: "Michael Rodriguez",
      role: "Marketing Director",
      company: "E-commerce Retail",
      quote: "The real-time market intelligence feature is a game-changer. We can now respond to market trends instantly and our campaign ROI has increased by 156% in just 3 months.",
      avatar: "MR"
    },
    {
      name: "Emily Watson",
      role: "Founder & CEO",
      company: "Digital Agency",
      quote: "As an agency, we manage dozens of clients. NexusPlanner helps us deliver personalized, data-driven campaigns at scale. Our clients love the transparency and results.",
      avatar: "EW"
    }
  ];

  const beneficiaries = [
    {
      icon: "👔",
      title: "Marketing Teams",
      description: "Automate campaign planning and leverage AI to generate winning strategies based on real-time market data."
    },
    {
      icon: "🚀",
      title: "Startups & Scale-ups",
      description: "Compete with enterprise marketing budgets by using AI-powered intelligence to make smarter, faster decisions."
    },
    {
      icon: "🏢",
      title: "Enterprise Organizations",
      description: "Manage multi-channel campaigns at scale with complete observability and closed-loop learning."
    },
    {
      icon: "🎯",
      title: "Digital Agencies",
      description: "Deliver exceptional results for multiple clients with automated campaign generation and performance tracking."
    },
    {
      icon: "📊",
      title: "Data-Driven Leaders",
      description: "Make confident decisions backed by AI analysis of market signals, customer behavior, and campaign performance."
    },
    {
      icon: "💡",
      title: "Innovation Teams",
      description: "Stay ahead of market trends with intelligent alerts and autonomous campaign optimization."
    }
  ];

  const nextTestimonial = () => {
    setActiveTestimonial((prev) => (prev + 1) % testimonials.length);
  };

  const prevTestimonial = () => {
    setActiveTestimonial((prev) => (prev - 1 + testimonials.length) % testimonials.length);
  };

  return (
    <div className="hero-container">
      <div className="hero-content">
        <div className="hero-header">
          <div className="hero-logo">
            <div className="logo-icon">
              <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
                <rect width="60" height="60" rx="12" fill="url(#gradient)" />
                <path d="M20 30L27 23L34 30L41 23" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M20 37L27 30L34 37L41 30" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                <defs>
                  <linearGradient id="gradient" x1="0" y1="0" x2="60" y2="60">
                    <stop offset="0%" stopColor="#4F9CFF" />
                    <stop offset="100%" stopColor="#2563EB" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <h1 className="hero-title">NexusPlanner</h1>
          </div>
          <p className="hero-tagline">AI-Powered Campaign Intelligence Platform</p>
        </div>

        <div className="hero-main">
          <h2 className="hero-headline">
            Transform Market Signals into
            <span className="gradient-text"> Winning Campaigns</span>
          </h2>
          <p className="hero-description">
            NexusPlanner combines real-time market intelligence with advanced AI to generate 
            data-driven marketing campaigns that respond to market opportunities instantly.
          </p>

          <div className="hero-cta">
            <button className="cta-primary" onClick={handleGetStarted}>
              Get Started
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M7 4L13 10L7 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
            <div className="demo-credentials">
              <span className="demo-label">Demo Credentials:</span>
              <code>demo / demo123</code>
            </div>
          </div>
        </div>

        <div className="hero-features">
          <div className="feature-card">
            <div className="feature-icon">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                <circle cx="20" cy="20" r="18" stroke="#4F9CFF" strokeWidth="2" />
                <path d="M14 20L18 24L26 16" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <h3>Market Intelligence</h3>
            <p>Real-time analysis of market signals and customer behavior patterns</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                <rect x="6" y="6" width="28" height="28" rx="4" stroke="#4F9CFF" strokeWidth="2" />
                <path d="M14 20H26M20 14V26" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </div>
            <h3>AI-Generated Campaigns</h3>
            <p>Automatically create compelling campaigns based on market insights</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                <path d="M8 30L15 20L22 25L32 12" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                <circle cx="15" cy="20" r="2" fill="#4F9CFF" />
                <circle cx="22" cy="25" r="2" fill="#4F9CFF" />
                <circle cx="32" cy="12" r="2" fill="#4F9CFF" />
              </svg>
            </div>
            <h3>Performance Tracking</h3>
            <p>Monitor campaign effectiveness with detailed analytics and observability</p>
          </div>
        </div>

        <section className="benefits-section">
          <h2 className="section-title">Who Benefits from NexusPlanner?</h2>
          <p className="section-subtitle">
            Whether you're a startup or enterprise, NexusPlanner adapts to your needs
          </p>
          
          <div className="benefits-grid">
            {beneficiaries.map((benefit, index) => (
              <div key={index} className="benefit-card">
                <div className="benefit-icon">{benefit.icon}</div>
                <h3 className="benefit-title">{benefit.title}</h3>
                <p className="benefit-description">{benefit.description}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="testimonials-section">
          <h2 className="section-title">Trusted by Marketing Leaders</h2>
          <p className="section-subtitle">
            See how teams are achieving breakthrough results with NexusPlanner
          </p>

          <div className="testimonial-container">
            <button className="testimonial-nav prev" onClick={prevTestimonial} aria-label="Previous testimonial">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M15 18L9 12L15 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>

            <div className="testimonial-card">
              <div className="quote-icon">"</div>
              <p className="testimonial-quote">{testimonials[activeTestimonial].quote}</p>
              <div className="testimonial-author">
                <div className="author-avatar">{testimonials[activeTestimonial].avatar}</div>
                <div className="author-info">
                  <p className="author-name">{testimonials[activeTestimonial].name}</p>
                  <p className="author-role">{testimonials[activeTestimonial].role}</p>
                  <p className="author-company">{testimonials[activeTestimonial].company}</p>
                </div>
              </div>
              <div className="testimonial-dots">
                {testimonials.map((_, index) => (
                  <button
                    key={index}
                    className={`dot ${index === activeTestimonial ? 'active' : ''}`}
                    onClick={() => setActiveTestimonial(index)}
                    aria-label={`Go to testimonial ${index + 1}`}
                  />
                ))}
              </div>
            </div>

            <button className="testimonial-nav next" onClick={nextTestimonial} aria-label="Next testimonial">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          </div>
        </section>

        <div className="hero-stats">
          <div className="stat-item">
            <div className="stat-number">10+</div>
            <div className="stat-label">Active Services</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">20+</div>
            <div className="stat-label">Market Signals</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">AI</div>
            <div className="stat-label">Powered</div>
          </div>
        </div>

        <div className="final-cta">
          <h2>Ready to Transform Your Marketing?</h2>
          <p>Join marketing leaders who are already using AI to stay ahead</p>
          <button className="cta-primary large" onClick={handleGetStarted}>
            Start Free Trial
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7 4L13 10L7 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </div>
      </div>

      <div className="hero-background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>
    </div>
  );
}

export default Hero;
