import React from 'react';
import './styles/ReportPage.css';

const ReportPage = () => {
    return (
        <div className="report-page-container">
            <h1>Incident Reporting Form</h1>

            <form className="report-page">
                <section className="contact-info">
                    <h2>Contact Information of the Reporter</h2>
                    <label>Name & Role/Title</label>
                    <input type="text" placeholder="Enter your name and role" />

                    <label>Organization Name</label>
                    <input type="text" placeholder="Enter organization name" />

                    <label>Contact No.</label>
                    <input type="text" placeholder="Enter contact number" />

                    <label>Email</label>
                    <input type="email" placeholder="Enter email address" />

                    <label>Address</label>
                    <textarea placeholder="Enter address"></textarea>
                </section>

                <section className="incident-details">
                    <h2>Basic Incident Details</h2>
                    <label>Affected Entity</label>
                    <input type="text" placeholder="Enter affected entity" />

                    <label>Incident Type</label>
                    <div className="checkbox-group">
                        {[
                            'Targeted scanning/probing of critical networks/systems',
                            'Compromise of critical systems/information',
                            'Unauthorised access of IT systems/data',
                            'Defacement or intrusion into the website',
                            'Malicious code attacks',
                            'Attack on servers and network devices',
                            'Identity Theft, spoofing and phishing attacks',
                            'DoS/DDoS attacks',
                            'Attacks on Critical infrastructure and Wireless networks',
                            'Data Breach',
                            'Data Leak'
                        ].map((incident, index) => (
                            <label key={index}>
                                <input class="checkBox" type="checkbox" /> {incident}
                            </label>
                        ))}
                    </div>

                    <label>Is the affected system critical to the organization’s mission?</label>
                    <textarea placeholder="Provide brief details"></textarea>

                    <h2>Basic Information of Affected System</h2>
                    <label>Domain/URL</label>
                    <input type="text" placeholder="Enter domain/URL" />

                    <label>IP Address</label>
                    <input type="text" placeholder="Enter IP address" />

                    <label>Operating System</label>
                    <input type="text" placeholder="Enter OS details" />

                    <label>Make/Model/Cloud Details</label>
                    <input type="text" placeholder="Enter details" />

                    <label>Location of Affected System</label>
                    <input type="text" placeholder="Enter location details" />

                    <label>Network and ISP Name</label>
                    <input type="text" placeholder="Enter ISP details" />

                    <label>Brief Description of Incident</label>
                    <textarea placeholder="Enter description"></textarea>

                    <label>Occurrence Date & Time</label>
                    <input type="datetime-local" />

                    <label>Detection Date & Time</label>
                    <input type="datetime-local" />
                </section>

                <button type="submit" className="submit-btn">Submit Report</button>
            </form>
        </div>
    );
};

export default ReportPage;
