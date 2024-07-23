// backend/server.js
const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const { verifyCaptcha } = require('./middleware/recaptchaMiddleware');
const jwt = require('jsonwebtoken');

dotenv.config();
const app = express();
app.use(cors());
app.use(express.json());
app.post('/api/login', verifyCaptcha, (req, res) => {
  const { email, password } = req.body;
  if (email === 'test@example.com' && password === 'password') {
    const token = jwt.sign({ id: 1, email }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.json({ token });
  } else {
    res.status(401).json({ message: 'Invalid credentials' });
  }
});
const PORT = process.env.PORT || 5002;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));