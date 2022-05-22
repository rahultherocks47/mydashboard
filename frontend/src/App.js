import './App.css';
import {BrowserRouter as Router,Route,Routes} from 'react-router-dom'
import Header from './components/Header';
import DemoPage from './pages/DemoPage'
import StockPage from './pages/StockPage'
import MapContainer from './pages/Map'

function App() {
  return (
    <Router>
    <div className="App">
      <header className="App-header">        
      <Header />        
      </header>
      <Routes>
      <Route path="/" exact element={<DemoPage />} />
      <Route path="/stock/:symbol" element={<StockPage />} />
      <Route path="/map" element={<MapContainer />} />
      </Routes>      
    </div>
    </Router>
  );
}

export default App;
