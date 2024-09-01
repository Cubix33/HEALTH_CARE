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

  const handleLogin = async () => {
    if (userID && password) {
      try {
        const response = await fetch('http://localhost:8000/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: userID,
            password: password,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('token', data.access);
          if (role === 'doctor') {
            navigate('http://127.0.0.1:8000/api/user/patients/');
          } else {
            navigate('http://127.0.0.1:8000/api/user/get-diabetes-data/');
          }
        } else {
          alert('Invalid login credentials. Please try again.');
        }
      } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again later.');
      }
    } else {
      alert('Please enter both User ID and Password.');
    }
  };

  const handleSignUp = async () => {
    if (password !== confirmPassword) {
      alert('Passwords do not match.');
      return;
    }
    if (firstName && phoneNo && password && confirmPassword) {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            first_name: firstName,
            phone: phoneNo,
            password: password,
            password2: confirmPassword,
          }),
        });

        if (response.ok) {
          alert('Sign-up successful! You can now log in.');
          setIsSignup(false);
        } else {
          alert('Sign-up failed. Please try again.');
        }
      } catch (error) {
        console.error('Error during sign-up:', error);
        alert('An error occurred. Please try again later.');
      }
    } else {
      alert('Please fill out all fields.');
    }
  };
  return (
    <div className="login-container">
      <h1 className="login-title">
        {isSignup ? 'Patient Sign Up' : (role === 'doctor' ? 'Doctor' : 'Patient')} 
        {isSignup ? 'Sign Up' : 'Login'}
      </h1>
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