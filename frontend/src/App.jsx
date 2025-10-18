import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import MarketIntelligence from './pages/MarketIntelligence';
import Campaigns from './pages/Campaigns';
import Services from './pages/Services';
import Observability from './pages/Observability';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/market-intelligence" element={<MarketIntelligence />} />
            <Route path="/campaigns" element={<Campaigns />} />
            <Route path="/services" element={<Services />} />
            <Route path="/observability" element={<Observability />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
