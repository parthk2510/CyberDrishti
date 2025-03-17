import React, { useState } from 'react';
import { FaUserCircle } from 'react-icons/fa';
import LogoutButton from './LogoutButton';
import './Header.css';

const Header = ({ toggleSidebar }) => {
    const [showDropdown, setShowDropdown] = useState(false);

    const handleProfileClick = () => {
        setShowDropdown(!showDropdown);
    };

    return (
        <div className="header">
            <div className="header-left">
                <button className="menu-icon" onClick={toggleSidebar}>☰</button>
                <h1 className="logo">Cyber Drishti</h1>
            </div>
            <div className="header-right">
                <div className="profile-container">
                <LogoutButton />
                </div>
            </div>
        </div>
    );
};

export default Header;
