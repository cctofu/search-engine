import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './PatentPage.css'; // Import the CSS file for styling

const PatentPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { claimText, mostSimilarClaim, patent_id } = location.state;
  const [patentDetails, setPatentDetails] = useState({
    keyword: [],
    abstract: '',
  });

  const fetchPatentDetails = async (claimTexts) => {
    try {
      const response = await fetch('http://101.6.161.39:8000/api/details', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ claim_texts: [claimTexts[0]] }),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setPatentDetails(data.data);
    } catch (error) {
      console.error('Error fetching patent details:', error);
    }
  };

  useEffect(() => {
    if (claimText) {
      fetchPatentDetails(claimText);
    }
  }, [claimText, mostSimilarClaim]);

  const { keyword, abstract } = patentDetails;

  const handleKeywordClick = (keyword) => {
    navigate(`/search?query=${keyword}&type=keyword`);
  };

  return (
    <div className="PatentPage">
      <h1 className="bold-text">{patent_id} Patent Information</h1>
      <p className="bold-text">Keywords:</p>
      {keyword && keyword.length > 0 ? (
        <ul>
          {keyword.map((kw, index) => (
            <li key={index}>
              <button onClick={() => handleKeywordClick(kw)} className="keyword-button">
                {kw}
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>Loading...</p>
      )}
      <p className="bold-text">Abstract:</p>
      <p>{abstract}</p>
      <p className="bold-text">Claim Texts:</p>
      {claimText && claimText.length > 0 ? (
        <ul>
          {claimText.map((text, index) => (
            <li key={index} className={index === mostSimilarClaim ? 'bold-text highlight-gray' : ''}>
              {text}
            </li>
          ))}
        </ul>
      ) : (
        <p>No claim texts available</p>
      )}
    </div>
  );
};

export default PatentPage;
