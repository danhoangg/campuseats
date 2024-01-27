import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from "./NavBar";
import ChatContainer from "./ChatContainer";

function App() {
  return (
    <Router>
      <div className='App bg-red-200 h-screen'>
        <Navbar />
        <Routes>
          <Route exact path="/matches" element={<ChatContainer />}>
          </Route>
          <Route exact path="/matching" element={<p>hi</p>}>
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
