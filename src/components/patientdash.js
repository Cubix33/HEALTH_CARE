import React, { useState } from 'react';
import './patientdash.css'; // Import the CSS file

const PatientDashboard = () => {
  const [patientID, setPatientID] = useState('');
  const [pregnancies, setPregnancies] = useState('');
  const [glucose, setGlucose] = useState('');
  const [bloodPressure, setBloodPressure] = useState('');
  const [skinThickness, setSkinThickness] = useState('');
  const [insulin, setInsulin] = useState('');
  const [bmi, setBmi] = useState('');
  const [diabetesPedigreeFunction, setDiabetesPedigreeFunction] = useState('');
  const [age, setAge] = useState('');
  const [outcome, setOutcome] = useState('');

  const handleSubmit = () => {
    // Add logic to handle form submission here
    if (patientID && pregnancies && glucose && bloodPressure && skinThickness && insulin && bmi && diabetesPedigreeFunction && age && outcome) {
      alert('Medical details submitted successfully.');
      // Add actual submission logic here
    } else {
      alert('Please fill in all fields.');
    }
  };

  return (
    <div className="patient-dashboard-container">
      <h1 className="dashboard-title">Patient Dashboard</h1>
      <div className="details-form">
        <h2 className="form-title">Upload Medical Details</h2>
        <input
          type="text"
          placeholder="Patient ID"
          value={patientID}
          onChange={(e) => setPatientID(e.target.value)}
          className="form-input"
        />
        <input
          type="number"
          placeholder="Pregnancies"
          value={pregnancies}
          onChange={(e) => setPregnancies(e.target.value)}
          className="form-input"
        />
        <input
          type="number"
          placeholder="Glucose"
          value={glucose}
          onChange={(e) => setGlucose(e.target.value)}
          className="form-input"
        />
        <input
          type="number"
          placeholder="Blood Pressure"
          value={bloodPressure}
          onChange={(e) => setBloodPressure(e.target.value)}
          className="form-input"
        />
        <input
          type="number"
          placeholder="Skin Thickness"
          value={skinThickness}
          onChange={(e) => setSkinThickness(e.target.value)}
          className="form-input"
        />
        <input
          type="number"
          placeholder="Insulin"
          value={insulin}
          onChange={(e) => setInsulin(e.target.value)}
          className="form-input"
        />
        <input
          type="number"
          placeholder="BMI"
          value={bmi}
          onChange={(e) => setBmi(e.target.value)}
          className="form-input"
        />
        <input
          type="number"
          placeholder="Diabetes Pedigree Function"
          value={diabetesPedigreeFunction}
          onChange={(e) => setDiabetesPedigreeFunction(e.target.value)}
          className="form-input"
        />
        <input
          type="number"
          placeholder="Age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          className="form-input"
        />
        <input
          type="text"
          placeholder="Outcome (Diabetes or Not)"
          value={outcome}
          onChange={(e) => setOutcome(e.target.value)}
          className="form-input"
        />
        <button onClick={handleSubmit} className="submit-button">Submit Details</button>
      </div>
    </div>
  );
};

export default PatientDashboard;

