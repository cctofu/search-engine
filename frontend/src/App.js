import React, { useState } from 'react';
import './App.css';
import { ConfigProvider, Space } from 'antd';
import SearchBar from './SearchBar';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('claim'); 

  const theme = {
    components: {
      AutoComplete: {
        activeShadow: "0 0 0 4px rgba(239,239,239,255)",
        activeBorderColor: "#c7c7c7",
        hoverBorderColor: "#9e9e9e",
        algorithm: true, // Enable algorithm
        fontFamily: 'Poppins, sans-serif'
      }
    },
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="title">
          Patent Search<span style={{color:"#ff6600"}}>.</span>
        </h1>
        <text className='title_text'>Search for relevant <span style={{fontWeight:"bold", color:'black'}}>patents</span></text>
        <ConfigProvider theme={theme}>
          <Space>
            <SearchBar
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            searchType={searchType}
            setSearchType={setSearchType}
            />
          </Space>
        </ConfigProvider>
      </header>
    </div>
  );
}

export default App;
