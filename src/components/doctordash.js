import React, { useState } from 'react';
import './doctordash.css';

const DoctorDashboard = () => {
  const [patientID, setPatientID] = useState('');
  const [patientName, setPatientName] = useState('');
  const [uploadType, setUploadType] = useState(''); // To track whether the doctor is uploading or entering details manually
  const [prescriptionFile, setPrescriptionFile] = useState(null);
  const [prescriptionDetails, setPrescriptionDetails] = useState({
    pregnancies: '',
    glucose: '',
    bloodPressure: '',
    skinThickness: '',
    insulin: '',
    bmi: '',
    diabetesPedigreeFunction: '',
    age: '',
    outcome: ''
  });

  const handleFileUpload = (e) => {
    setPrescriptionFile(e.target.files[0]);
  };

  const handleManualDetailChange = (e) => {
    const { name, value } = e.target;
    setPrescriptionDetails((prevDetails) => ({
      ...prevDetails,
      [name]: value
    }));
  };

  const handleSubmit = () => {
    if (uploadType === 'file' && prescriptionFile) {
      alert(`Prescription for ${patientName} uploaded successfully.`);
    } else if (uploadType === 'manual' && Object.values(prescriptionDetails).every(detail => detail)) {
      alert(`Prescription for ${patientName} entered successfully.`);
    } else {
      alert('Please complete the form.');
    }

    // Clear the form fields
    setPatientID('');
    setPatientName('');
    setUploadType('');
    setPrescriptionFile(null);
    setPrescriptionDetails({
      pregnancies: '',
      glucose: '',
      bloodPressure: '',
      skinThickness: '',
      insulin: '',
      bmi: '',
      diabetesPedigreeFunction: '',
      age: '',
      outcome: ''
    });
  };

  return (
    <div className="doctor-dashboard-container">
      <h1 className="doctor-dashboard-title">Doctor Dashboard</h1>
      <div className="doctor-form">
        <input
          type="text"
          placeholder="Patient ID"
          value={patientID}
          onChange={(e) => setPatientID(e.target.value)}
          className="form-input"
        />
        <input
          type="text"
          placeholder="Patient Name"
          value={patientName}
          onChange={(e) => setPatientName(e.target.value)}
          className="form-input"
        />
        <div className="upload-options">
          <label className="option-label">
            <input
              type="radio"
              value="file"
              checked={uploadType === 'file'}
              onChange={() => setUploadType('file')}
            />
            Upload Prescription (Image/PDF)
          </label>
          <label className="option-label">
            <input
              type="radio"
              value="manual"
              checked={uploadType === 'manual'}
              onChange={() => setUploadType('manual')}
            />
            Enter Prescription Details Manually
          </label>
        </div>

        {uploadType === 'file' && (
          <div className="file-upload">
            <input
              type="file"
              accept="image/*,application/pdf"
              onChange={handleFileUpload}
              className="file-input"
            />
          </div>
        )}

        {uploadType === 'manual' && (
          <div className="manual-form">
            <input
              type="text"
              name="pregnancies"
              placeholder="Pregnancies"
              value={prescriptionDetails.pregnancies}
              onChange={handleManualDetailChange}
              className="form-input"
            />
            <input
              type="number"
              name="glucose"
              placeholder="Glucose"
              value={prescriptionDetails.glucose}
              onChange={handleManualDetailChange}
              className="form-input"
            />
            <input
              type="number"
              name="bloodPressure"
              placeholder="Blood Pressure"
              value={prescriptionDetails.bloodPressure}
              onChange={handleManualDetailChange}
              className="form-input"
            />
            <input
              type="number"
              name="skinThickness"
              placeholder="Skin Thickness"
              value={prescriptionDetails.skinThickness}
              onChange={handleManualDetailChange}
              className="form-input"
            />
            <input
              type="number"
              name="insulin"
              placeholder="Insulin"
              value={prescriptionDetails.insulin}
              onChange={handleManualDetailChange}
              className="form-input"
            />
            <input
              type="number"
              name="bmi"
              placeholder="BMI"
              value={prescriptionDetails.bmi}
              onChange={handleManualDetailChange}
              className="form-input"
            />
            <input
              type="number"
              name="diabetesPedigreeFunction"
              placeholder="Diabetes Pedigree Function"
              value={prescriptionDetails.diabetesPedigreeFunction}
              onChange={handleManualDetailChange}
              className="form-input"
            />
            <input
              type="number"
              name="age"
              placeholder="Age"
              value={prescriptionDetails.age}
              onChange={handleManualDetailChange}
              className="form-input"
            />
            <input
              type="text"
              name="outcome"
              placeholder="Outcome (Diabetes or Not)"
              value={prescriptionDetails.outcome}
              onChange={handleManualDetailChange}
              className="form-input"
            />
          </div>
        )}

        <button onClick={handleSubmit} className="form-button">
          Submit
        </button>
      </div>
    </div>
  );
};

export default DoctorDashboard;

