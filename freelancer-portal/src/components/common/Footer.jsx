// import React from 'react';
// import './Footer.css';

// const Footer = () => {
//     return (
//         <footer className="footer">
//             <div className="footer-content">
//                 <div className="footer-section">
//                     <h3>FreelanceHub</h3>
//                     <p>Connecting talented freelancers with innovative companies worldwide.</p>
//                 </div>
//                 <div className="footer-section">
//                     <h4>Quick Links</h4>
//                     <ul>
//                         <li><a href="/about">About Us</a></li>
//                         <li><a href="/contact">Contact</a></li>
//                         <li><a href="/terms">Terms of Service</a></li>
//                         <li><a href="/privacy">Privacy Policy</a></li>
//                     </ul>
//                 </div>
//                 <div className="footer-section">
//                     <h4>Follow Us</h4>
//                     <div className="social-links">
//                         <a href="#"><i className="fab fa-facebook"></i></a>
//                         <a href="#"><i className="fab fa-twitter"></i></a>
//                         <a href="#"><i className="fab fa-linkedin"></i></a>
//                         <a href="#"><i className="fab fa-github"></i></a>
//                     </div>
//                 </div>
//             </div>
//             <div className="footer-bottom">
//                 <p>&copy; 2026 FreelanceHub. All rights reserved.</p>
//             </div>
//         </footer>
//     );
// };

// export default Footer;
import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-section">
                    <h3>FreelanceHub</h3>
                    <p>Connecting talented freelancers with innovative companies worldwide.</p>
                </div>
                <div className="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><Link to="/about">About Us</Link></li>
                        <li><Link to="/contact">Contact</Link></li>
                        <li><Link to="/terms">Terms of Service</Link></li>
                        <li><Link to="/privacy">Privacy Policy</Link></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h4>Follow Us</h4>
                    <div className="social-links">
                        <a href="https://facebook.com" target="_blank" rel="noopener noreferrer"><i className="fab fa-facebook"></i></a>
                        <a href="https://twitter.com" target="_blank" rel="noopener noreferrer"><i className="fab fa-twitter"></i></a>
                        <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer"><i className="fab fa-linkedin"></i></a>
                        <a href="https://github.com" target="_blank" rel="noopener noreferrer"><i className="fab fa-github"></i></a>
                    </div>
                </div>
            </div>
            <div className="footer-bottom">
                <p>&copy; 2026 FreelanceHub. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;