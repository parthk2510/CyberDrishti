import React from 'react';
import { signOut } from 'firebase/auth';
import { auth } from '../firebaseConfig';  // Firebase auth instance
import './LogoutButton.css';  // Import CSS

const LogoutButton = () => {
    const handleLogout = async () => {
        try {
            await signOut(auth);
            alert("Successfully logged out!");
        } catch (error) {
            console.error("Logout failed:", error.message);
        }
    };

    return (
        <button className="logout-button" onClick={handleLogout}>
            Logout
        </button>
    );
};

export default LogoutButton;
