import React from 'react';
import ReactDOM from 'react-dom/client';
import { Router } from "@/Router.tsx";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import '@/styles/globals.css';

const client = new QueryClient()

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={client}>
      <Router />
    </QueryClientProvider>
  </React.StrictMode>
);
