import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import config from './config';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [offerings, setOfferings] = useState([]);
  const [isSignedIn, setIsSignedIn] = useState(false);
  const [authEmail, setAuthEmail] = useState('');
  const [forgotEmail, setForgotEmail] = useState('');
  const [credits, setCredits] = useState('');
  const [advancedInfo, setAdvancedInfo] = useState([]);
  const backendURL = __DEV__ ? config.local.backendURL : config.production.backendURL;

  const loadOfferings = async () => {
    // Load offerings from your source (you removed Glassify-related code)
  };

  const handleSuccessfulTransactionResult = async (newCredits) => {
    // Handle a successful transaction result here, e.g., send data to your backend (removed sensitive information).
  };

  const purchase = async (sku) => {
    // Handle the purchase logic (you removed Glassify-related code)
  };

  const signIn = () => {
    setIsSignedIn(true);
  };

  const signOut = async () => {
    setIsSignedIn(false);
    await AsyncStorage.removeItem('isSignedIn');
    await AsyncStorage.removeItem('email');
    setAuthEmail('');
    // Clear other sensitive data if needed.
  };

  const globalValues = {
    isSignedIn,
    signIn,
    signOut,
    setAuthEmail,
    authEmail,
    forgotEmail,
    setForgotEmail,
    backendURL,
    offerings,
    purchase,
    credits,
    setCredits,
    advancedInfo,
  };

  return (
    <AuthContext.Provider value={globalValues}>
      {children}
    </AuthContext.Provider>
  );
};
