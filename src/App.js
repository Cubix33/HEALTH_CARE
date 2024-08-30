import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SelectRole from './components/selectRole';
import LoginPage from './components/login';
import DoctorDashboard from './components/doctordash';
import PatientDashboard from './components/patientdash';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SelectRole />} />
         <Route path="/doctor-login" element={<LoginPage role="doctor" />} />
        <Route path="/patient-login" element={<LoginPage role="patient" />} />
        <Route path="/doctor-dashboard" element={<DoctorDashboard />} />
        <Route path="/patient-dashboard" element={<PatientDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;

