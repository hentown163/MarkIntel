import { Link, useLocation, useNavigate } from 'react-router-dom';
import { LayoutDashboard, TrendingUp, Target, Server, Sparkles, Brain, LogOut, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/market-intelligence', icon: TrendingUp, label: 'Market Intelligence' },
    { path: '/campaigns', icon: Target, label: 'Campaigns' },
    { path: '/services', icon: Server, label: 'Services' },
    { path: '/observability', icon: Brain, label: 'Observability' },
  ];

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Sparkles className="brand-icon" size={24} />
        <span className="brand-text">NexusPlanner</span>
      </div>
      
      <div className="nav-items">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </div>

      <div className="navbar-actions">
        <div className="user-info">
          <User size={16} />
          <span>{user?.name || user?.username}</span>
        </div>
        <button className="logout-button" onClick={handleLogout} title="Logout">
          <LogOut size={18} />
        </button>
        <div className="system-status">
          <div className="status-indicator"></div>
          <span>System Active</span>
        </div>
      </div>
    </nav>
  );
}
