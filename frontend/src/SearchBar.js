import React, { useState, useCallback } from 'react';
import { AutoComplete, ConfigProvider, Space, Select } from 'antd';
import { useNavigate } from 'react-router-dom';
import debounce from 'lodash/debounce';
import './SearchBar.css'; // Import the CSS file for styling

const SearchBar = React.memo(({ searchQuery, setSearchQuery, searchType, setSearchType }) => {
  const [autocompleteResults, setAutocompleteResults] = useState([]);
  const navigate = useNavigate();

  const handleSearch = (value) => {
    if (value) {
      navigate(`/search?query=${value}&type=${searchType}`);
    }
  };

  const fetchAutocompleteResults = useCallback(debounce(async (query) => {
    try {
      const response = await fetch(`http://101.6.161.39:8000/api/autocomplete/${query}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json();
      if (result.code === 0 && Array.isArray(result.data)) {
        setAutocompleteResults([{ value: query }, ...result.data.map(item => ({ value: item }))]);
      } else {
        setAutocompleteResults([{ value: query }]);
      }
    } catch (error) {
      console.error('Error fetching autocomplete data:', error);
      setAutocompleteResults([{ value: query }]);
    }
  }, 300), []); // Debounce to limit the frequency of API calls

  const handleSelect = (value) => {
    setSearchQuery(value);
    handleSearch(value);
  };

  const handleInputChange = (value) => {
    setSearchQuery(value);
    if (searchType !== 'keyword') {
      setAutocompleteResults([{ value }]);
      fetchAutocompleteResults(value);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSearch(searchQuery);
    }
  };

  const handleSearchTypeChange = (value) => {
    setSearchType(value);
    setSearchQuery(''); // Clear the query when search type changes
    setAutocompleteResults([]); // Clear autocomplete results when search type changes
  };

  return (
    <ConfigProvider>
      <div className="search-bar-container">
        <Space>
          <AutoComplete
            className='custom-input'
            placeholder="Search for relevant patents"
            style={{ width: '500px', height: '60px', fontFamily: 'Poppins' }}
            value={searchQuery}
            onChange={handleInputChange}
            onSelect={handleSelect}
            options={searchType === 'keyword' ? [] : autocompleteResults}
            onKeyDown={handleKeyDown}
            filterOption={(inputValue, option) =>
              option.value.toUpperCase().indexOf(inputValue.toUpperCase()) !== -1
            }
          />
          <Select
            value={searchType}
            style={{ width: 120, height: 60, fontFamily: 'Poppins'}}
            onChange={handleSearchTypeChange}
            options={[
              { value: "claim", label: 'Claim' },
              { value: "keyword", label: 'Keyword' }
            ]}
          />
        </Space>
      </div>
    </ConfigProvider>
  );
});

export default SearchBar;
