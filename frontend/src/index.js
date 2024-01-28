import React from 'react';
import ReactDOM from 'react-dom';
import { Auth0Provider } from '@auth0/auth0-react';
import App from './App';
import './index.css';

const domain = 'dev-hxlk2gzqgooijai2.us.auth0.com';
const clientId = 'CdfdDkkxLEt8SXdLDbLiGFrhdwGFMvyv';

ReactDOM.render(
  <Auth0Provider
    domain={domain}
    clientId={clientId}
    redirectUri={window.location.origin}
  >
    <App />
  </Auth0Provider>,
  document.getElementById('root')
);