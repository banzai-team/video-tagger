import React from 'react';
import ReactDOM from 'react-dom/client';
import {Router} from "@/Router.tsx";

import '@/styles/globals.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <Router />
  </React.StrictMode>
);
