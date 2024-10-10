import React from "react";
import { Routes, Route, Link } from "react-router-dom";

import "./css/App.css";

import Home from "./pages/Home";
import Community from "./pages/Community";
import Roote from "./pages/Roote";
import Support from "./pages/Support";
import Contact from "./pages/Contact";
import Signup from "./pages/Signup";
import Board from "./pages/Board";
import QnAboard from "./pages/QnAboard";
import Login from "./pages/Login";

function App() {
  return (
    <div className="App">
      <header>
        <div className="header-container">
          <div className="logo">
            <a href="/">Soul_Mate</a>
          </div>
          <nav>
            <div className="hamburger" id="hamburger">
              <div></div>
              <div></div>
              <div></div>
            </div>
            <ul id="nav-menu">
              <li>
                <Link to="/">메인</Link>
              </li>
              <li>
                <Link to="/Community">커뮤니티</Link>
              </li>
              <li>
                <Link to="/roote">노선정보</Link>
              </li>
              <li>
                <Link to="/support">지원</Link>
              </li>
              <li>
                <Link to="/contact">문의하기</Link>
              </li>
            </ul>
          </nav>
        </div>
      </header>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/community" element={<Community />} />
        <Route path="/roote" element={<Roote />} />
        <Route path="/support" element={<Support />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/board" element={<Board />} />
        <Route path="/QnAboard" element={<QnAboard />} />
        <Route path="/Login" element={<Login />} />
      </Routes>
    </div>
  );
}

export default App;
