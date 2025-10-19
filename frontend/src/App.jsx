import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Hero from './pages/Hero';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import MarketIntelligence from './pages/MarketIntelligence';
import Campaigns from './pages/Campaigns';
import Services from './pages/Services';
import Observability from './pages/Observability';

function AppRoutes() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/" element={user ? <Navigate to="/dashboard" replace /> : <Hero />} />
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <div className="app">
              <Navbar />
              <main className="main-content">
                <Dashboard />
              </main>
            </div>
          </ProtectedRoute>
        }
      />
      <Route
        path="/market-intelligence"
        element={
          <ProtectedRoute>
            <div className="app">
              <Navbar />
              <main className="main-content">
                <MarketIntelligence />
              </main>
            </div>
          </ProtectedRoute>
        }
      />
      <Route
        path="/campaigns"
        element={
          <ProtectedRoute>
            <div className="app">
              <Navbar />
              <main className="main-content">
                <Campaigns />
              </main>
            </div>
          </ProtectedRoute>
        }
      />
      <Route
        path="/services"
        element={
          <ProtectedRoute>
            <div className="app">
              <Navbar />
              <main className="main-content">
                <Services />
              </main>
            </div>
          </ProtectedRoute>
        }
      />
      <Route
        path="/observability"
        element={
          <ProtectedRoute>
            <div className="app">
              <Navbar />
              <main className="main-content">
                <Observability />
              </main>
            </div>
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
