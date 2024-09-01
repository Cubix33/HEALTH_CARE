import React from 'react';
import { useNavigate } from 'react-router-dom';
import './selectRole.css'; // Import the CSS file

const SelectRole = () => {
  const navigate = useNavigate();

  const handleSelection = (role) => {
    if (role === 'doctor') {
      navigate('/doctor-login');
    } else {
      navigate('/patient-login');
    }
  };

  return (
    <div className="select-role-container">
      <h1 className="title">Welcome to the Medical Portal</h1>
      <p className="subtitle">Please select your role to proceed:</p>
      <div className="button-container">
        <button className="role-button" onClick={() => handleSelection('doctor')}>
          Doctor
        </button>
        <button className="role-button" onClick={() => handleSelection('patient')}>
          Patient
        </button>
      </div>
    </div>
  );
};

export default SelectRole;

