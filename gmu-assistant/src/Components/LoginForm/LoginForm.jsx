import React, { useState } from 'react';
import './LoginForm.css';

const LoginForm = ({ onFormSubmit,onResponse }) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Adjusted to pass an object with a username property
    onFormSubmit({ username: inputValue });
  };

  return (
    <div className='wrapper'>
      <form onSubmit={handleSubmit}>
        <h1>GMU AI Assistant</h1>
        <div className="input-box">
          <label htmlFor="username">Enter something here:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={inputValue}
            onChange={handleInputChange}
            required
          />
          <button type="submit">Enter</button>
        </div>

      </form>
    </div>
  );
};

export default LoginForm;
