import React from 'react';
import { createRoot } from 'react-dom/client';
import CampusExplorer from './CampusExplorer.jsx';
import './styles.css';
import './campus-overrides.css';

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <CampusExplorer />
  </React.StrictMode>,
);
