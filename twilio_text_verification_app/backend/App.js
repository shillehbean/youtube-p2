const mongoose = require('mongoose');
const twilio = require('twilio');
const express = require('express');

const config = require('./config');
const User = require('./models/User.js');

mongoose.connect(config.mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = mongoose.connection;
const twilioClient = twilio(config.twilioAccountSID, config.twilioAuthToken);


db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
  console.log('Connected to MongoDB');
});

const app = express();
app.use(express.json());

app.post('/register', async (req, res) => {
  try {
    const user = new User({
      name: req.body.name,
      password: req.body.password,
      phoneNumber: req.body.phoneNumber,
    });
    await user.save();

    const verificationCode = generateRandomCode();

    await twilioClient.messages.create({
      body: `Your verification code is: ${verificationCode}`,
      from: '+18444361959',
      to: req.body.phoneNumber,
    });

    user.verificationCode = verificationCode;
    await user.save();

    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});


app.post('/verify', async (req, res) => {
  try {
    const phoneNumber = req.body.phoneNumber;
    const verificationCode = req.body.verificationCode;

    const user = await User.findOne({ phoneNumber });
    if (!user) {
      res.status(404).json({ error: 'User not found' });
      return;
    }

    if (user.verificationCode === verificationCode) {
      res.status(200).json({ message: 'Verification successful' });
    } else {
      res.status(400).json({ error: 'Verification code is incorrect' });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
});


function generateRandomCode() {
  return Math.floor(100000 + Math.random() * 900000).toString();
}


const port = 3000; 
app.use(express.json());

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
