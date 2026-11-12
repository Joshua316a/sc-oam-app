# sc-oam-app

**Org Asset Manager API & Web UI**

A modern, API-first replacement for the Org Asset Manager (OAM) Tkinter-based application.
Built with **FastAPI** for the backend and **React + Vite + Tailwind** for the frontend.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional, for containerized deployment)

### Installation

#### Backend (FastAPI)
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the development server
uvicorn app:app --reload
```

#### Frontend (React + Vite)
```bash
# Install Node dependencies
cd web
npm install

# Start Vite dev server
npm run dev
```

### API Documentation
Once the backend is running, visit:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

### Docker (Optional)
```bash
docker build -t sc-oam-app .
docker run -p 8000:8000 -p 3000:3000 sc-oam-app
```

## 📦 Features

| Category | Endpoints/Features |
|----------|-------------------|
| **Blueprints** | CRUD operations, filtering, search |
| **Crafting** | Quality calculation, resource requirements |
| **Warehouse** | Inventory management |
| **Hangar** | Fleet vessel management |
| **Authentication** | JWT-based (pluggable) |
| **Database** | SQLite → PostgreSQL migration ready |

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, Python |
| **Frontend** | React, Vite, TypeScript |
| **Styling** | Tailwind CSS |
| **Database** | SQLAlchemy (SQLite/PostgreSQL) |
| **Container** | Docker |
| **CI/CD** | GitHub Actions |

## 📚 API Reference

Full auto-generated API documentation is available at `/docs` when the server is running.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/foo`)
3. Commit your changes (`git commit -m 'Add foo feature'`)
4. Push to the branch (`git push origin feature/foo`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
