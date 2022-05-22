import './App.css';
import { HashRouter as Router,Route,Routes} from "react-router-dom";
import Header from './components/Header';
import StockPage from './pages/StockPage';
import DemoPage from './pages/DemoPage';

function App() {
  return (
    <Router>
    <div className="container dark">
      <div className="app">
      <header>
      <Header />
      </header>      
      <Routes>      
      <Route path="/stock/:symbol" element={<StockPage />} />
      <Route path="/" exact element={<DemoPage />} />      
      </Routes>      
      </div>
    </div>    
    </Router>
  );
}

export default App;