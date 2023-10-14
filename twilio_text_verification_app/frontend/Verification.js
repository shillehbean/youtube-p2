import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import axios from 'axios';
import { useRoute } from '@react-navigation/native';

const Verification = () => {
  const [verificationCode, setVerificationCode] = useState('');
  const [verificationStatus, setVerificationStatus] = useState(null);
  const route = useRoute(); 
  const { phoneNumber } = route.params;

  const handleVerify = async () => {
    try {
      const response = await axios.post('http://localhost:3000/verify', {
        phoneNumber: phoneNumber,
        verificationCode: verificationCode
      });

      if (response.status === 200) {
        setVerificationStatus('Verification successful');
      } else {
        setVerificationStatus('Verification failed. Please try again.');
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <View style={styles.container}>
      {verificationStatus && <Text style={styles.successMessage}>{verificationStatus}</Text>}
      <Text style={styles.label}>Verification Code:</Text>
      <TextInput
        style={styles.input}
        value={verificationCode}
        onChangeText={setVerificationCode}
        placeholder="Enter verification code"
      />

      <Button title="Verify" onPress={handleVerify} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  label: {
    fontSize: 18,
    marginBottom: 5,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingLeft: 10,
  },
  successMessage: {
    fontSize: 16,
    color: 'green',
    marginBottom: 10,
  },
});

export default Verification;
