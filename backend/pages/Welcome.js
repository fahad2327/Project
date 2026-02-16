import React from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../../../backend/components/Navbar";

function Welcome() {
    const navigate = useNavigate();

    return (
        <>
            <Navbar />

            <div className="container hero">
                <div className="row align-items-center">

                    <div className="col-md-6">
                        <h1 className="fw-bold">Find Freelance Work & Jobs</h1>
                        <p className="text-muted">
                            Join our platform to hire freelancers or apply for jobs.
                        </p>

                        <button
                            className="btn btn-primary me-3 px-4 py-2"
                            onClick={() => navigate("/signin")}
                        >
                            Sign In
                        </button>

                        <button
                            className="btn btn-success px-4 py-2"
                            onClick={() => navigate("/signup")}
                        >
                            Sign Up
                        </button>
                    </div>

                    <div className="col-md-6 text-center">
                        <img
                            src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                            alt="hero"
                            className="img-fluid"
                            style={{ maxHeight: "350px" }}
                        />
                    </div>

                </div>
            </div>
        </>
    );
}

export default Welcome;
