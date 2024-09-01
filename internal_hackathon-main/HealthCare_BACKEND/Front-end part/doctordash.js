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
    /* outcome: '' */
  });
  const [patientFound, setPatientFound] = useState(false); // To track if a patient is found

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

  const handlePatientSearch = async () => {
    try {
      // Replace with actual API call
      const response = await fetch(`/api/patients/${patientID}`);
      const data = await response.json();

      if (response.ok && data.patientName) {
        setPatientName(data.patientName);
        setPatientFound(true);
      } else {
        alert('Patient not found. Please check the Patient ID.');
        setPatientFound(false);
        setPatientName('');
      }
    } catch (error) {
      alert('An error occurred while searching for the patient.');
      console.error('Error:', error);
    }
  };

  const handleSubmit = async () => {
    if (uploadType === 'file' && prescriptionFile) {
      // Handle file upload submission
      const formData = new FormData();
      formData.append('file', prescriptionFile);
      formData.append('patientID', patientID);

      try {
        const response = await fetch('/api/upload-prescription', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          alert(`Test Results for ${patientName} uploaded successfully.`);
        } else {
          alert('Failed to upload the file. Please try again.');
        }
      } catch (error) {
        alert('An error occurred while uploading the file.');
        console.error('Error:', error);
      }
    } else if (uploadType === 'manual' && Object.values(prescriptionDetails).every(detail => detail)) {
      // Handle manual details submission
      const requestBody = {
        patientID,
        prescriptionDetails,
      };

      try {
        const response = await fetch('/api/submit-prescription-details', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          alert(`Test results for ${patientName} entered successfully.`);
        } else {
          alert('Failed to submit the details. Please try again.');
        }
      } catch (error) {
        alert('An error occurred while submitting the details.');
        console.error('Error:', error);
      }
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
      /* outcome: '' */
    });
    setPatientFound(false);
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
        <button onClick={handlePatientSearch} className="form-button">Search</button>

        {patientFound && (
          <>
            <p>Patient Name: {patientName}</p>
            <div className="upload-options">
              <label className="option-label">
                <input
                  type="radio"
                  value="file"
                  checked={uploadType === 'file'}
                  onChange={() => setUploadType('file')}
                />
                Upload Test Results (Image/PDF)
              </label>
              <label className="option-label">
                <input
                  type="radio"
                  value="manual"
                  checked={uploadType === 'manual'}
                  onChange={() => setUploadType('manual')}
                />
                Enter Test Result Details Manually
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
              </div>
            )}

            <button onClick={handleSubmit} className="form-button">
              Submit
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default DoctorDashboard;
