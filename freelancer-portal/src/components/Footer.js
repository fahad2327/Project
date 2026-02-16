import React from 'react';
import { FaFacebook, FaTwitter, FaLinkedin, FaGithub } from 'react-icons/fa';

function Footer() {
    return (
        <footer className="footer">
            <div className="container">
                <div className="row">
                    <div className="col-md-4 mb-4">
                        <h5 className="text-warning">Freelancer Portal</h5>
                        <p className="text-light">
                            Connecting talented freelancers with amazing opportunities worldwide.
                        </p>
                        <div className="social-icons">
                            <FaFacebook className="me-3 text-light" style={{ cursor: 'pointer' }} />
                            <FaTwitter className="me-3 text-light" style={{ cursor: 'pointer' }} />
                            <FaLinkedin className="me-3 text-light" style={{ cursor: 'pointer' }} />
                            <FaGithub className="text-light" style={{ cursor: 'pointer' }} />
                        </div>
                    </div>
                    <div className="col-md-2 mb-4">
                        <h6 className="text-warning">Quick Links</h6>
                        <ul className="list-unstyled">
                            <li><a href="/" className="text-light text-decoration-none">Home</a></li>
                            <li><a href="/about" className="text-light text-decoration-none">About</a></li>
                            <li><a href="/contact" className="text-light text-decoration-none">Contact</a></li>
                        </ul>
                    </div>
                    <div className="col-md-2 mb-4">
                        <h6 className="text-warning">For Freelancers</h6>
                        <ul className="list-unstyled">
                            <li><a href="/find-work" className="text-light text-decoration-none">Find Work</a></li>
                            <li><a href="/post-project" className="text-light text-decoration-none">Post Project</a></li>
                        </ul>
                    </div>
                    <div className="col-md-4 mb-4">
                        <h6 className="text-warning">Newsletter</h6>
                        <p className="text-light">Subscribe for latest opportunities</p>
                        <div className="input-group">
                            <input type="email" className="form-control" placeholder="Your email" />
                            <button className="btn btn-warning">Subscribe</button>
                        </div>
                    </div>
                </div>
                <hr className="bg-light" />
                <div className="text-center text-light">
                    <p className="mb-0">&copy; 2024 Freelancer Portal. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;