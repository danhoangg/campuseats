import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Navbar from "./NavBar";
import ChatContainer from "./ChatContainer";
import Login from './Login';

function App() {
  return (
    <Router>
      <div className='App bg-red-200 h-screen'>
        <Navbar />
        <Routes>
          <Route exact path="/matches" element={<ChatContainer />} />
          <Route exact path="/matching" element={<p>hi</p>} />
          <Route exact path="/login" element={<Login />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
