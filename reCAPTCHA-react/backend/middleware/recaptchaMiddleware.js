// backend/middleware/recaptchaMiddleware.js
const axios = require('axios');
const asyncHandler = require('express-async-handler');

const verifyCaptcha = asyncHandler(async (req, res, next) => {
  const { captcha } = req.body;
  if (!captcha) {
    return res.status(400).json({ message: 'Please complete the CAPTCHA' });
  }
  const secretKey = process.env.CAPTCHA_SECRET_KEY;
  try {
    const response = await axios.post(
      `https://www.google.com/recaptcha/api/siteverify?secret=${secretKey}&response=${captcha}`
    );
    if (response.data.success) {
      next();
    } else {
      return res.status(400).json({ message: 'CAPTCHA verification failed' });
    }
  } catch (error) {
    return res.status(500).json({ message: 'CAPTCHA verification error' });
  }
});

module.exports = { verifyCaptcha };