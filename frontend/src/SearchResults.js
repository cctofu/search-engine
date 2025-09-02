import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Table, Spin } from 'antd';
import './SearchResults.css';
import SearchBar from './SearchBar'; // Import the new component

const App = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('keyword'); // State for search type
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false); // State for loading

  useEffect(() => {
    const query = new URLSearchParams(location.search).get('query');
    const type = new URLSearchParams(location.search).get('type') || 'keyword';
    setSearchQuery(query || '');
    setSearchType(type);

    if (query) {
      fetchResults(query, type);
    }
  }, [location.search]);

  const fetchResults = async (query, type) => {
    setLoading(true); // Set loading to true
    setSearchResults([]); // Clear previous results

    try {
      const response = await fetch('http://101.6.161.39:8000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, type }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      const highlightText = (text, keywords) => {
        const parts = text.split(new RegExp(`(${keywords.join('|')})`, 'gi'));
        return parts.map((part, index) =>
          keywords.includes(part.toLowerCase()) ? <span key={index} style={{ fontWeight: 'bold' }}>{part}</span> : part
        );
      };

      const truncateText = (text, length) => {
        return text.length > length ? text.substring(0, length) + '...' : text;
      };

      const fetchedResults = data.data.map((item, index) => ({
        id: index + 1,
        patentId: item.patent_id,
        claims: item.claims.slice(0, 5).map(claim => ({
          raw: claim,
          processed: type === 'keyword' ? highlightText(truncateText(claim, 150), query.split(' ')) : truncateText(claim, 150)
        })),
        full_claims: item.claims,
        mostSimilarClaimIndex: item.most_similar_claim_index, // Pass as index
      }));

      setSearchResults(fetchedResults);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false); // Set loading to false
    }
  };

  const handleRowClick = (record) => {
    navigate('/patent', { state: { claimText: record.full_claims, mostSimilarClaim: record.mostSimilarClaimIndex, patent_id: record.patentId } });
  };

  const columns = [
    {
      title: 'Patent ID',
      dataIndex: 'patentId',
      key: 'patentId',
      width: '20%',
    },
    {
      title: 'Claim Text',
      dataIndex: 'claims',
      key: 'claims',
      render: claims => claims.map((claim, index) => (
        <div key={index}>
          {claim.processed}
        </div>
      )),
    },
  ];

  return (
    <div className="App">
      <header className="Results">
        <h1 className="title">
          Patent Search<span style={{color:"#ff6600"}}>.</span>
        </h1>
        <text className='title_text'>Search for relevant <span style={{fontWeight:"bold", color:'black'}}>patents</span></text>
        <SearchBar
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          searchType={searchType}
          setSearchType={setSearchType}
        />
        <div style={{ height: '100vh', overflowY: 'scroll', width: '80%', marginBottom: "2%", marginTop: "1%", fontFamily:"Poppins" }}>
          {loading ? (
            <Spin tip="Loading..." style={{ marginTop: '20px' }} />
          ) : (
            <Table
              dataSource={searchResults}
              columns={columns}
              pagination={{ pageSize: 5 }}
              rowKey="id"
              onRow={(record) => {
                return {
                  onClick: () => handleRowClick(record), // Click row
                };
              }}
            />
          )}
        </div>
      </header>
    </div>
  );
};

export default App;
