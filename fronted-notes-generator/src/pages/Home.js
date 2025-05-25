import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

function Home() {
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="container">
      <h1>Welcome to AI Notes Generator</h1>
      <p>
        This project helps you generate AI-enhanced lecture notes by analyzing
        uploaded video lectures and presentations.
      </p>
      <div>
        <button onClick={() => handleNavigate('/login')}>Login</button>
        <button onClick={() => handleNavigate('/register')}>Register</button>
      </div>
    </div>
  );
}

export default Home;
