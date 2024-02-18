import React, { useState } from 'react';
import LoginForm from './Components/LoginForm/LoginForm';

const App = () => {
  const [apiResponse, setApiResponse] = useState({}); // Use an object to store both response and status

  const handleButtonClick = async ({ username }) => {
    try {
      const response = await fetch('http://localhost:8000/logins/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
      });

      const responseData = await response.json();

      // Assuming your backend responds with an object that includes 'status' and 'response'
      // Update state with the whole response object
      setApiResponse({ status: responseData.status, response: responseData.response });
    } catch (error) {
      console.error('Error sending data:', error);
      setApiResponse({ status: 'Error sending data', response: null });
    }
  };

  return (
    <div>

      <LoginForm onFormSubmit={handleButtonClick} />
      <p className="ai-response">AI Response: {apiResponse.response}</p>

      {/* Display the status message */}
      
      {/* Conditionally render the AI response if it exists */}
    </div>
  );
};

export default App;
