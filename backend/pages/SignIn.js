import React from "react";
import Navbar from "../../../backend/components/Navbar";
import { useNavigate } from "react-router-dom";

function SignIn() {
    const navigate = useNavigate();

    return (
        <>
            <Navbar />

            <div className="container mt-5">
                <div className="row justify-content-center">
                    <div className="col-md-5">
                        <div className="card-box">
                            <h3 className="mb-4 text-center">Sign In</h3>

                            <input className="form-control mb-3" placeholder="Email" />
                            <input className="form-control mb-3" type="password" placeholder="Password" />

                            <button
                                className="btn btn-primary w-100"
                                onClick={() => navigate("/dashboard")}
                            >
                                Login
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default SignIn;
