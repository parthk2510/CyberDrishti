import React from 'react';
import { Navigate } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';

const ProtectedRoute = ({ user, children }) => {
    if (!user) return <Navigate to="/" replace />;
    
    return (
        <>
            <Header />
            <Sidebar />
            <div className="content">{children}</div>
        </>
    );
};

export default ProtectedRoute;
