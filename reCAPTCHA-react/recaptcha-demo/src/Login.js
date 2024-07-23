// src/Login.js
import React, { useState } from 'react';
import axios from 'axios';
import ReCAPTCHA from 'react-google-recaptcha';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './Login.css'; // Import the CSS file

const Login = () => {
  const [formData, setFormData] = useState({ email: '', password: '', captcha: '' });
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Add state for login status
  const { email, password, captcha } = formData;

  const onChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onCaptchaChange = (value) => {
    setFormData({ ...formData, captcha: value });
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!captcha) {
      toast.error('Please complete the CAPTCHA');
      return;
    }
    try {
      const response = await axios.post('http://localhost:5002/api/login', { email, password, captcha });
      toast.success('Login successful');
      setIsLoggedIn(true); // Set login status to true on success
      console.log(response.data); // Handle the response
    } catch (error) {
      toast.error(error.response.data.message || 'Login failed');
    }
  };

  return (
    <div className="login-container">
      {isLoggedIn ? (
        <div className="success-message">
          <h1>Login Successful</h1>
        </div>
      ) : (
        <form className="login-form" onSubmit={onSubmit}>
          <input
            type="email"
            name="email"
            value={email}
            onChange={onChange}
            placeholder="Email"
            required
          />
          <input
            type="password"
            name="password"
            value={password}
            onChange={onChange}
            placeholder="Password"
            required
          />
          <div className="captcha-container">
            <ReCAPTCHA
              sitekey={process.env.REACT_APP_CAPTCHA_SITE_KEY}
              onChange={onCaptchaChange}
            />
          </div>
          <button type="submit">Login</button>
        </form>
      )}
      <ToastContainer position="top-right" autoClose={5000} />
    </div>
  );
};

export default Login;