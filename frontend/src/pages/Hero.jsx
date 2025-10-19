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
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <circle cx="24" cy="24" r="22" stroke="#4F9CFF" strokeWidth="2"/>
          <path d="M24 14C19.6 14 16 17.6 16 22C16 24.4 17.2 26.6 19 28L19 32C19 33.1 19.9 34 21 34L27 34C28.1 34 29 33.1 29 32L29 28C30.8 26.6 32 24.4 32 22C32 17.6 28.4 14 24 14Z" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M20 32L20 35M28 32L28 35" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round"/>
        </svg>
      ),
      title: "Marketing Teams",
      description: "Automate campaign planning and leverage AI to generate winning strategies based on real-time market data."
    },
    {
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <path d="M24 8L26.5 18L36 14L30 22L40 24L30 26L36 34L26.5 30L24 40L21.5 30L12 34L18 26L8 24L18 22L12 14L21.5 18L24 8Z" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      title: "Startups & Scale-ups",
      description: "Compete with enterprise marketing budgets by using AI-powered intelligence to make smarter, faster decisions."
    },
    {
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <rect x="10" y="18" width="28" height="20" rx="2" stroke="#4F9CFF" strokeWidth="2"/>
          <path d="M14 18V14C14 12.9 14.9 12 16 12H32C33.1 12 34 12.9 34 14V18" stroke="#4F9CFF" strokeWidth="2"/>
          <path d="M10 24H38" stroke="#4F9CFF" strokeWidth="2"/>
          <circle cx="24" cy="30" r="2" fill="#4F9CFF"/>
        </svg>
      ),
      title: "Enterprise Organizations",
      description: "Manage multi-channel campaigns at scale with complete observability and closed-loop learning."
    },
    {
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <circle cx="24" cy="24" r="16" stroke="#4F9CFF" strokeWidth="2"/>
          <circle cx="24" cy="24" r="10" stroke="#4F9CFF" strokeWidth="2"/>
          <circle cx="24" cy="24" r="4" fill="#4F9CFF"/>
          <path d="M24 8V16M24 32V40M8 24H16M32 24H40" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round"/>
        </svg>
      ),
      title: "Digital Agencies",
      description: "Deliver exceptional results for multiple clients with automated campaign generation and performance tracking."
    },
    {
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <path d="M10 32L14 22L20 28L26 18L32 24L38 14" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <rect x="8" y="8" width="32" height="32" rx="2" stroke="#4F9CFF" strokeWidth="2"/>
          <path d="M28 14L32 10L36 14" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      title: "Data-Driven Leaders",
      description: "Make confident decisions backed by AI analysis of market signals, customer behavior, and campaign performance."
    },
    {
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <path d="M24 10C24 10 14 15 14 24C14 29.5 18.5 34 24 34C29.5 34 34 29.5 34 24C34 15 24 10 24 10Z" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <circle cx="24" cy="24" r="4" fill="#4F9CFF"/>
          <path d="M24 10V6M10 24H6M24 38V42M38 24H42" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round"/>
        </svg>
      ),
      title: "Innovation Teams",
      description: "Stay ahead of market trends with intelligent alerts and autonomous campaign optimization."
    }
  ];

  const pricingPlans = [
    {
      name: "Free Trial",
      price: "$0",
      period: "15 days",
      description: "Perfect for individuals to explore NexusPlanner",
      features: [
        "3 AI-generated campaigns",
        "Basic market intelligence",
        "Campaign templates access",
        "Standard support",
        "Single user account",
        "Email notifications"
      ],
      cta: "Start Free Trial",
      highlighted: false
    },
    {
      name: "Team",
      price: "$299",
      period: "per month",
      description: "Best for growing teams and agencies",
      features: [
        "Unlimited AI-generated campaigns",
        "Real-time market intelligence",
        "Advanced RAG-powered insights",
        "Multi-agent coordination",
        "Up to 10 team members",
        "Priority support",
        "Campaign performance analytics",
        "CRM integration (HubSpot, Salesforce)",
        "Custom templates",
        "API access"
      ],
      cta: "Get Started",
      highlighted: true
    },
    {
      name: "Enterprise",
      price: "Custom",
      period: "contact sales",
      description: "For large organizations with advanced needs",
      features: [
        "Everything in Team, plus:",
        "Unlimited team members",
        "Dedicated account manager",
        "Custom AI model training",
        "Advanced observability & audit trails",
        "SSO & Active Directory integration",
        "Custom SLA agreements",
        "On-premise deployment options",
        "White-label capabilities",
        "Advanced security & compliance",
        "24/7 premium support",
        "Custom integrations"
      ],
      cta: "Contact Sales",
      highlighted: false
    }
  ];

  const organizationalTeams = [
    {
      team: "Marketing & Growth",
      useCase: "Generate and optimize campaigns, track ROI, and respond to market trends instantly",
      impact: "156% increase in campaign ROI on average"
    },
    {
      team: "Product Marketing",
      useCase: "Launch products with data-driven campaigns tailored to specific customer segments",
      impact: "Reduce campaign planning time from weeks to minutes"
    },
    {
      team: "Sales Enablement",
      useCase: "Create targeted campaigns based on CRM data and customer behavior patterns",
      impact: "Better sales-marketing alignment and lead quality"
    },
    {
      team: "Customer Success",
      useCase: "Design retention campaigns and upsell strategies using customer insights",
      impact: "Increased customer lifetime value"
    },
    {
      team: "Revenue Operations",
      useCase: "Optimize marketing spend with AI-powered analytics and performance tracking",
      impact: "Data-driven budget allocation decisions"
    },
    {
      team: "Business Intelligence",
      useCase: "Access detailed observability into campaign performance and market signals",
      impact: "Complete transparency into marketing effectiveness"
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
                <div className="benefit-icon">
                  {benefit.icon}
                </div>
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

        <section className="case-study-section">
          <h2 className="section-title">Success Story</h2>
          <p className="section-subtitle">How TechVenture Inc. Transformed Their Marketing</p>
          
          <div className="case-study-card">
            <div className="case-study-header">
              <div className="company-badge">
                <div className="company-logo">TV</div>
                <div>
                  <h3>TechVenture Inc.</h3>
                  <p>Enterprise SaaS Platform</p>
                </div>
              </div>
              <div className="case-study-meta">
                <span className="industry-tag">B2B SaaS</span>
                <span className="size-tag">250+ Employees</span>
              </div>
            </div>

            <div className="case-study-content">
              <div className="challenge-section">
                <h4>The Challenge</h4>
                <p>
                  TechVenture's marketing team was spending 2-3 weeks planning each campaign, struggling to keep pace with rapidly changing market conditions. Their manual process involved multiple spreadsheets, endless meetings, and by the time campaigns launched, market opportunities had often passed.
                </p>
              </div>

              <div className="solution-section">
                <h4>The Solution</h4>
                <p>
                  TechVenture implemented NexusPlanner's AI-powered platform to automate campaign generation and tap into real-time market intelligence. The platform integrated seamlessly with their existing HubSpot CRM, allowing them to leverage customer data for more targeted campaigns.
                </p>
              </div>

              <div className="results-grid">
                <div className="result-item">
                  <div className="result-number">156%</div>
                  <div className="result-label">Increase in Campaign ROI</div>
                </div>
                <div className="result-item">
                  <div className="result-number">92%</div>
                  <div className="result-label">Reduction in Planning Time</div>
                </div>
                <div className="result-item">
                  <div className="result-number">3.2x</div>
                  <div className="result-label">More Campaigns Launched</div>
                </div>
                <div className="result-item">
                  <div className="result-number">$2.4M</div>
                  <div className="result-label">Additional Revenue Generated</div>
                </div>
              </div>

              <div className="key-benefits">
                <h4>Key Benefits Realized</h4>
                <ul>
                  <li>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <circle cx="10" cy="10" r="9" stroke="#4F9CFF" strokeWidth="2"/>
                      <path d="M6 10L9 13L14 7" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Automated campaign generation from market signals in under 5 minutes
                  </li>
                  <li>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <circle cx="10" cy="10" r="9" stroke="#4F9CFF" strokeWidth="2"/>
                      <path d="M6 10L9 13L14 7" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Real-time market trend detection enabling rapid response to opportunities
                  </li>
                  <li>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <circle cx="10" cy="10" r="9" stroke="#4F9CFF" strokeWidth="2"/>
                      <path d="M6 10L9 13L14 7" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Complete observability into AI decision-making for compliance and optimization
                  </li>
                  <li>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <circle cx="10" cy="10" r="9" stroke="#4F9CFF" strokeWidth="2"/>
                      <path d="M6 10L9 13L14 7" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    CRM integration providing personalized campaigns based on customer segments
                  </li>
                </ul>
              </div>

              <blockquote className="case-study-quote">
                "NexusPlanner didn't just speed up our process - it fundamentally transformed how we think about campaign planning. We're now proactive instead of reactive, and our results speak for themselves."
                <cite>- Sarah Chen, CMO at TechVenture Inc.</cite>
              </blockquote>
            </div>
          </div>
        </section>

        <section className="pricing-section">
          <h2 className="section-title">Simple, Transparent Pricing</h2>
          <p className="section-subtitle">Choose the plan that fits your needs</p>
          
          <div className="pricing-grid">
            {pricingPlans.map((plan, index) => (
              <div key={index} className={`pricing-card ${plan.highlighted ? 'highlighted' : ''}`}>
                {plan.highlighted && <div className="popular-badge">Most Popular</div>}
                <div className="pricing-header">
                  <h3 className="plan-name">{plan.name}</h3>
                  <div className="plan-price">
                    <span className="price">{plan.price}</span>
                    <span className="period">/{plan.period}</span>
                  </div>
                  <p className="plan-description">{plan.description}</p>
                </div>
                <ul className="features-list">
                  {plan.features.map((feature, i) => (
                    <li key={i}>
                      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <circle cx="10" cy="10" r="9" stroke={plan.highlighted ? '#4F9CFF' : '#64748b'} strokeWidth="2"/>
                        <path d="M6 10L9 13L14 7" stroke={plan.highlighted ? '#4F9CFF' : '#64748b'} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
                <button 
                  className={`pricing-cta ${plan.highlighted ? 'primary' : 'secondary'}`}
                  onClick={handleGetStarted}
                >
                  {plan.cta}
                </button>
              </div>
            ))}
          </div>
        </section>

        <section className="organizational-teams-section">
          <h2 className="section-title">Which Teams Can Use NexusPlanner?</h2>
          <p className="section-subtitle">
            NexusPlanner powers collaboration across your entire organization
          </p>
          
          <div className="teams-grid">
            {organizationalTeams.map((item, index) => (
              <div key={index} className="team-card">
                <div className="team-header">
                  <h3>{item.team}</h3>
                </div>
                <p className="team-usecase">{item.useCase}</p>
                <div className="team-impact">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M2 12L5 8L8 10L12 4" stroke="#4F9CFF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <circle cx="12" cy="4" r="1.5" fill="#4F9CFF"/>
                  </svg>
                  <span>{item.impact}</span>
                </div>
              </div>
            ))}
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
