import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';
import SearchResults from './SearchResults'; // Make sure this component exists and is correctly named
import PatentPage from './PatentPage';

ReactDOM.render(
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/search" element={<SearchResults />} />
      <Route path="/patent" element={<PatentPage />} />
    </Routes>
  </Router>,
  document.getElementById('root')
);
