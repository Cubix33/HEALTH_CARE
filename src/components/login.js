import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css'; // Import the CSS file

const LoginPage = ({ role }) => {
  const navigate = useNavigate();
  const [userID, setUserID] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // Add authentication logic here
    if (userID && password) {
      if (role === 'doctor') {
        navigate('/doctor-dashboard');
      } else {
        navigate('/patient-dashboard');
      }
    } else {
      alert('Please enter both User ID and Password.');
    }
  };

  return (
    <div className="login-container">
      <h1 className="login-title">{role === 'doctor' ? 'Doctor' : 'Patient'} Login</h1>
      <div className="login-form">
        <input
          type="text"
          placeholder="Enter User ID"
          value={userID}
          onChange={(e) => setUserID(e.target.value)}
          className="login-input"
        />
        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="login-input"
        />
        <button onClick={handleLogin} className="login-button">Login</button>
      </div>
    </div>
  );
};

export default LoginPage;

