import React from 'react';

import { GoogleLogin } from 'react-google-login';
import { refreshTokenSetup } from '../utils/RefreshToken';
import { CLIENT_ID } from "../constants"

const Login = () => {
  const onSuccess = (res) => {
    console.log('Login Success: currentUser:', res);
    // alert(
    //   `Logged in successfully welcome ${res.profileObj.name}. \n See console for full profile object.`
    // );
    refreshTokenSetup(res);
  };

  const onFailure = (res) => {
    console.log('Login failed: res:', res);
    alert(
      "Failed to login!"
    );
  };

  return (
    <div>
      <GoogleLogin
        clientId={CLIENT_ID}
        buttonText="Login"
        onSuccess={onSuccess}
        onFailure={onFailure}
        cookiePolicy={'single_host_origin'}
        style={{ marginTop: '100px' }}
        isSignedIn={true}
        accessType="offline"
        responseType="code"
        prompt="consent"
        // scope="profile email https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.install"
      />
    </div>
  );
}

export default Login;
