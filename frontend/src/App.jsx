import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import FindEvents from './pages/FindEvents';
import FindGroups from './pages/FindGroups';
import EventDetails from './pages/EventDetails';
import UserProfile from './pages/UserProfile';
import GroupDetails from './pages/GroupDetails';
import Login from './pages/Login';
import Signup from './pages/Signup';
import PersonalProfile from './pages/PersonalProfile';
import Chat from './pages/Chat';
import './styles/harbourspace-theme.css';
import './App.css';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="app">
          <Header />
          <main>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/find" element={<FindEvents />} />
              <Route path="/groups" element={<FindGroups />} />
              <Route path="/events/:id" element={<EventDetails />} />
              <Route path="/members/:id" element={<UserProfile />} />
              <Route path="/groups/:id" element={<GroupDetails />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <PersonalProfile />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/chat"
                element={
                  <ProtectedRoute>
                    <Chat />
                  </ProtectedRoute>
                }
              />
            </Routes>
          </main>
          <Footer />
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
