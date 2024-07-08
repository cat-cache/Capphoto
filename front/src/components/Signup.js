import "./Login.css";
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

export default function Signup()



{
  return (
    
      <div className="container">
        <div className="row">
          <div className="col-md-6 offset-md-3">
            <h2 className="text-center text-dark mt-5" style={{ fontFamily: 'Courier New', fontWeight: 'bold' }}>Login</h2>
            <div className="text-center mb-5" style={{ fontFamily: 'Courier New', fontWeight: 'bold',}}>
  Your AI Powered Gallery
</div>

            
            <div className="card my-5">
              <form className="card-body cardbody-color p-lg-5">
                <div className="text-center">
                  <img
                    src="https://static.vecteezy.com/system/resources/previews/016/776/195/original/cappuccino-with-froth-in-a-glass-cup-mug-illustration-clip-art-sticker-print-sign-or-symbol-for-coffee-shops-cafe-restaurants-etc-vector.jpg"
                    className="img-fluid profile-image-pic img-thumbnail rounded-circle my-3"
                    width="200px"
                    alt="profile"
                  />
                </div>

                <div className="mb-3">
                  <input
                    type="text"
                    className="form-control"
                    id="Username"
                    aria-describedby="emailHelp"
                    placeholder="User Name"
                  />
                </div>
                <div className="mb-3">
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    placeholder="password"
                  />
                </div>
                <div className="mb-3">
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    placeholder="verify password"
                  />
                </div>
                <div className="text-center">
                  <button
                    type="submit"
                    className="btn btn-color px-5 mb-5 w-100"
                  >
                    Signup
                  </button>
                </div>
                <div
                  id="emailHelp"
                  className="form-text text-center mb-5 text-dark"
                >
                  
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    
  );
}
