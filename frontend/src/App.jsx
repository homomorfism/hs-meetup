import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import FindEvents from './pages/FindEvents';
import EventDetails from './pages/EventDetails';
import UserProfile from './pages/UserProfile';
import GroupDetails from './pages/GroupDetails';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/find" element={<FindEvents />} />
            <Route path="/events/:id" element={<EventDetails />} />
            <Route path="/members/:id" element={<UserProfile />} />
            <Route path="/groups/:id" element={<GroupDetails />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
