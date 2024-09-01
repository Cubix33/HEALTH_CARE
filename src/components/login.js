import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css'; // Import the CSS file

const LoginPage = ({ role }) => {
  const navigate = useNavigate();
  const [userID, setUserID] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [phoneNo, setPhoneNo] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isSignup, setIsSignup] = useState(false);

  const handleLogin = () => {
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

  const handleSignUp = () => {
    if (password !== confirmPassword) {
      alert('Passwords do not match.');
      return;
    }
    if (firstName && phoneNo && password && confirmPassword) {
      // Add sign-up logic here
      alert('Sign-up successful! You can now log in.');
      setIsSignup(false);
    } else {
      alert('Please fill out all fields.');
    }
  };

  return (
    <div className="login-container">
      <h1 className="login-title">{isSignup ? 'Patient ' : (role === 'doctor' ? 'Doctor' : 'Patient')} {isSignup ? 'Sign Up' : 'Login'}</h1>
      {isSignup ? (
        <div className="login-form">
          <input
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            className="login-input"
          />
          <input
            type="text"
            placeholder="Phone No"
            value={phoneNo}
            onChange={(e) => setPhoneNo(e.target.value)}
            className="login-input"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="login-input"
          />
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="login-input"
          />
          <button onClick={handleSignUp} className="login-button">Sign Up</button>
          <p>Already have an account? <button onClick={() => setIsSignup(false)} className="toggle-button">Login</button></p>
        </div>
      ) : (
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
          {role === 'patient' && (
            <div className="signup-option">
              <p>Don't have an account?</p>
              <button onClick={() => setIsSignup(true)} className="signup-button">
                Sign Up
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LoginPage;

