# Search Engine Project

This repository contains a full-stack search engine application with a Django backend and a React frontend. The project is designed to index, search, and display patent or document data efficiently, leveraging modern web technologies and vector search capabilities.

## Project Structure

```
search_engine/
├── backend/      # Django backend (API, database, search logic)
├── frontend/     # React frontend (UI, user interaction)
├── search/       # Scripts and tools for indexing, querying, and data processing
```

---

## Backend (`backend/`)
- **Framework:** Django
- **Key Components:**
  - `manage.py`: Django management script
  - `search/`: Django app for search logic (models, views, urls)
  - `search_engine/`: Django project settings and configuration
  - `db.sqlite3`: SQLite database for development
- **Features:**
  - RESTful API endpoints for search and data retrieval
  - Database models for storing indexed data
  - Admin interface for managing data

---

## Frontend (`frontend/`)
- **Framework:** React
- **Key Components:**
  - `src/`: Main React source code (components, styles)
    - `App.js`: Main application component
    - `SearchBar.js`, `SearchResults.js`, `PatentPage.js`: UI components for search and results
  - `public/`: Static assets and HTML template
  - `package.json`: Project dependencies and scripts
- **Features:**
  - User-friendly search interface
  - Real-time display of search results
  - Patent/document detail pages

---

## Search Scripts (`search/`)
- **Purpose:** Data processing, indexing, and advanced search
- **Key Scripts:**
  - `faiss_prepare.py`: Prepares vector indices using FAISS for efficient similarity search
  - `query.py`, `query_2.py`: Query logic for searching indexed data
  - `upload.py`, `download.py`: Data import/export utilities
  - `testcases/`: Test scripts and sample data for validation

---

## Getting Started

### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies (using a virtual environment is recommended):
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

---

## Usage
- Access the frontend at `http://localhost:3000` (default React port).
- The backend API runs at `http://localhost:8000` (default Django port).
- Use the search bar to query indexed data and view results.

---

## Acknowledgements
- [Django](https://www.djangoproject.com/)
- [React](https://reactjs.org/)
- [FAISS](https://github.com/facebookresearch/faiss)
