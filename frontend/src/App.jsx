import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { withAuthenticationRequired } from '@auth0/auth0-react';

import Navbar from "./NavBar";
import ChatContainer from "./ChatContainer";
import Login from './Login';
import Profile from './Profile';

function App() {
  const ProtectedChatContainer = withAuthenticationRequired(ChatContainer, {});
  const ProtectedProfile = withAuthenticationRequired(Profile, {});

  return (
    <Router>
      <div className='App bg-red-200 h-screen'>
        <Navbar />
        <Routes>
          <Route exact path="/matches" element={<ProtectedChatContainer />} />
          <Route exact path="/matching" element={<p>hi</p>} />
          <Route exact path="/login" element={<Login />} />
          <Route exact path="/profile" element={<ProtectedProfile />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
