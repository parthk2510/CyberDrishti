import React, { useState } from 'react';
import { FaUserCircle } from 'react-icons/fa';
import './Header.css';

const Header = ({ toggleSidebar }) => {
    const [showDropdown, setShowDropdown] = useState(false);

    const handleProfileClick = () => {
        setShowDropdown(!showDropdown);
    };

    const handleLogout = () => {
        console.log("User logged out");
    };

    return (
        <div className="header">
            <div className="header-left">
                <button className="menu-icon" onClick={toggleSidebar}>☰</button>
                <h1 className="logo">Cyber Drishti</h1>
            </div>
            <div className="header-right">
                <div className="profile-container">
                    <FaUserCircle className="profile-icon" onClick={handleProfileClick} />
                    {showDropdown && (
                        <div className="dropdown-menu">
                            <button onClick={handleLogout}>Logout</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Header;
