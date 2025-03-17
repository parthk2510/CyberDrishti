// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import {getAuth} from "firebase/auth";
const firebaseConfig = {
  apiKey: "AIzaSyCFT9j8MAlRT-_KgN91xg0EutC4eT7_2L0",
  authDomain: "cyberdrishti-e9c7e.firebaseapp.com",
  projectId: "cyberdrishti-e9c7e",
  storageBucket: "cyberdrishti-e9c7e.firebasestorage.app",
  messagingSenderId: "228946333783",
  appId: "1:228946333783:web:8e3500842df0f383f71312",
  measurementId: "G-L1MHKEEKJJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);