import React, { useState } from 'react';
import './patientdash.css'; // Import the CSS file

const PatientDashboard = () => {
  const [patientName, setPatientName] = useState('');
  const [patientID, setPatientID] = useState('');
  const [age, setAge] = useState('');
  const [view, setView] = useState('details'); // State to manage view

  const handleViewChange = (viewType) => {
    setView(viewType);
  };

  return (
    <div className="patient-dashboard-container">
      <h1 className="dashboard-title">Patient Dashboard</h1>

      {/* Patient Details Section */}
      {view === 'details' && (
        <div className="patient-details">
          <h2 className="details-title">Patient Details</h2>
          <p><strong>Name:</strong> {patientName}</p>
          <p><strong>ID:</strong> {patientID}</p>
          <p><strong>Age:</strong> {age}</p>
          <div className="view-options">
            <button onClick={() => handleViewChange('analytics')} className={`view-button ${view === 'analytics' ? 'active' : ''}`}>View Analytics</button>
            <button onClick={() => handleViewChange('recommendations')} className={`view-button ${view === 'recommendations' ? 'active' : ''}`}>Check Recommendations</button>
          </div>
        </div>
      )}

      {/* Analytics Section */}
      {view === 'analytics' && (
        <div className="analytics-section">
          <h2 className="section-title">Patient Analytics</h2>
          {/* Add your analytics display logic here */}
          <p>Here you can display patient analytics data.</p>
          <button onClick={() => handleViewChange('details')} className="back-button">Back to Details</button>
        </div>
      )}

      {/* Recommendations Section */}
      {view === 'recommendations' && (
        <div className="recommendations-section">
          <h2 className="section-title">Recommendations</h2>
          {/* Add your recommendations display logic here */}
          <p>Here you can display patient recommendations.</p>
          <button onClick={() => handleViewChange('details')} className="back-button">Back to Details</button>
        </div>
      )}
    </div>
  );
};

export default PatientDashboard;

