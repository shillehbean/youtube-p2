const mongoose = require('mongoose');

// Define the User schema
const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  password: {
    type: String,
    required: true,
  },
  phoneNumber: {
    type: String,
    required: true,
  },
  verificationCode: {
    type: String,
  },
  verified: {
    type: Boolean,
    default: false, // By default, a new user is not verified
  },
});

// Create a User model from the schema
const User = mongoose.model('User', userSchema);

module.exports = User;
