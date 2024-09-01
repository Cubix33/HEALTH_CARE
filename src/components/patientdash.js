import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './patientdash.css';

// Register necessary chart components
Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const PatientDashboard = () => {
  const [patientName, setPatientName] = useState('');
  const [patientID, setPatientID] = useState('');
  const [age, setAge] = useState('');
  const [view, setView] = useState('details'); // State to manage view

  const handleViewChange = (viewType) => {
    setView(viewType);
 
    };

useEffect(() => {
  try {
    const script1 = document.createElement('script');
    script1.src = "https://www.chatbase.co/embed.min.js";
    script1.setAttribute('chatbotId', 'LvLEITWz4QTfBVGtZO6Cv');
    script1.setAttribute('domain', 'www.chatbase.co');
    script1.defer = true;
    document.body.appendChild(script1);

    const script2 = document.createElement('script');
    script2.innerHTML = `
      window.embeddedChatbotConfig = {
        chatbotId: "LvLEITWz4QTfBVGtZO6Cv",
        domain: "www.chatbase.co"
      };
    `;
    document.body.appendChild(script2);
  } catch (error) {
    console.error('Error loading chatbot script:', error);
  }

  return () => {
    // Clean up the scripts when the component unmounts
    const scripts = document.querySelectorAll('script[src*="chatbase.co"]');
    scripts.forEach(script => document.body.removeChild(script));
  };
}, []);


  return (
    <div className="patient-dashboard-container">
      <h1 className="dashboard-title">Patient Dashboard</h1>

      {/* Patient Details Section */}
      {view === 'details' && (
        <div className="patient-details">
          <h2 className="details-title">Patient Details</h2>
          <p><strong>Name:</strong> Hemank </p>
          <p><strong>ID:</strong> DMZXXT </p>
          <p><strong>Age:</strong> 38 </p>
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
          <img src = "diabetes_plot.jpg" alt="Diabetes Plot"   style={{
    width: '500px',
    height: 'auto',
    border: '2px solid #ccc',
    borderRadius: '10px',
    display: 'block',
    margin: '0 auto',
  }}
/ >
          <button onClick={() => handleViewChange('details')} className="back-button">Back to Details</button>
        </div>
      )}

      {/* Recommendations Section */}
      {view === 'recommendations' && (
        <div className="recommendations-section">
          <h2 className="section-title">Recommendations</h2>
          <div className="recommendations-content">
            {/* Diet Section */}
            <h3 className="subsection-title">Diet</h3>
            <ul>
              <li><strong>Reduce calorie intake:</strong> Aim for a daily calorie deficit of 500-1,000 calories.</li>
              <li><strong>Choose nutrient-rich foods:</strong> Focus on fruits, vegetables, whole grains, and lean proteins.</li>
              <li><strong>Limit processed foods, sugary drinks, and unhealthy fats:</strong> These foods contribute to weight gain and insulin resistance.</li>
              <li><strong>Example meal plan:</strong>
                <ul>
                  <li><em>Breakfast:</em> Oatmeal with berries and nuts.</li>
                  <li><em>Lunch:</em> Grilled chicken salad with mixed greens and vegetables.</li>
                  <li><em>Dinner:</em> Salmon with roasted vegetables and brown rice.</li>
                </ul>
              </li>
            </ul>

            {/* Exercises Section */}
            <h3 className="subsection-title">Exercises</h3>
            <ul>
              <li><strong>Engage in regular physical activity:</strong> Aim for at least 150 minutes of moderate-intensity exercise or 75 minutes of vigorous-intensity exercise per week.</li>
              <li><strong>Choose activities you enjoy:</strong> This will make it more likely that you'll stick to your exercise routine.</li>
              <li><strong>Example exercises:</strong>
                <ul>
                  <li>Brisk walking</li>
                  <li>Swimming</li>
                  <li>Cycling</li>
                  <li>Dancing</li>
                </ul>
              </li>
            </ul>

            {/* Routine Section */}
            <h3 className="subsection-title">Routine</h3>
            <ul>
              <li><strong>Establish a regular sleep schedule:</strong> Aim for 7-9 hours of sleep each night.</li>
              <li><strong>Manage stress:</strong> Stress can lead to overeating and unhealthy habits. Find healthy ways to cope with stress, such as exercise, meditation, or yoga.</li>
              <li><strong>Monitor your blood glucose levels:</strong> Check your blood glucose levels regularly to track your progress and make adjustments to your diet and exercise plan as needed.</li>
            </ul>

            {/* Educational Facts Section */}
            <h3 className="subsection-title">Educational Facts in a Funny Way</h3>
            <ul>
              <li><strong>Why do we get goosebumps when we're cold?</strong> Because our tiny hairs are standing up like little soldiers trying to trap warm air.</li>
              <li><strong>Why do we yawn?</strong> It's our body's way of cooling down our brains.</li>
              <li><strong>Why do we have belly buttons?</strong> It's the scar from where we were once connected to our mothers through the umbilical cord.</li>
            </ul>

            {/* Anomaly Status Section */}
            <h3 className="subsection-title">Anomaly Status</h3>
            <p><em>Moderate or low chances of being diabetic.</em></p>

          </div>
          <button onClick={() => handleViewChange('details')} className="back-button">Back to Details</button>
        </div>

      )}
    </div>
	 );
};

export default PatientDashboard;

