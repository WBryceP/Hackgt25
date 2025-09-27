# Fact-Checking Platform

A modern web-based fact-checking platform designed to help users verify information and combat misinformation. This platform provides tools for researching and analyzing content to determine its accuracy and reliability.

## Project Goal

The primary goal of this project is to create a comprehensive fact-checking platform that enables users to:
- Submit content for fact-checking and verification
- Research information using automated tools and services
- Access reliable sources and cross-reference claims
- View detailed analysis and verification results
- Navigate through video content with fact-checking capabilities

## Architecture

This project follows a microservices architecture with separate frontend and backend services that can be deployed independently or together using Docker Compose.

## Folder Structure

### `/frontend`
**Technology Stack:** React 19, Vite, TailwindCSS, React Router DOM

The frontend service provides the user interface for the fact-checking platform.

**Key Components:**
- **React Router Setup:** Multi-page application with routing capabilities
- **CedarCopilot Integration:** AI-powered assistance with LLM provider configuration
- **Responsive UI:** Modern interface using TailwindCSS and Framer Motion

**Main Routes:**
- `/` - **Home Route:** Main landing page for the platform
- `/v/:id` - **Video Route:** Video content analysis and fact-checking interface

**Key Files:**
- `src/App.jsx` - Main application component with router configuration
- `src/routes/Home.jsx` - Home page component
- `src/routes/Video.jsx` - Video analysis interface with parameter-based routing
- `src/layout.jsx` - Shared layout component
- `package.json` - Dependencies and build configuration

**Development Scripts:**
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Code linting

### `/backend-research`
**Technology Stack:** FastAPI, Python, Uvicorn

The backend research service handles API requests, data processing, and research operations for fact-checking.

**Key Endpoints:**
- `GET /` - API information and version details
- `GET /health` - Health check endpoint for monitoring service status

**Key Files:**
- `main.py` - FastAPI application with core endpoints
- `requirements.txt` - Python dependencies (FastAPI, Uvicorn)
- `Dockerfile` - Container configuration for deployment
- `.env` - Environment configuration

**Service Features:**
- RESTful API architecture
- Health monitoring
- Docker containerization support
- Development environment configuration

### Root Configuration

**Key Files:**
- `docker-compose.yml` - Multi-service orchestration configuration
  - Backend service on port 8000
  - Health checks and auto-restart policies
  - Development environment setup
- `.gitignore` - Version control exclusions

## Getting Started

### Using Docker Compose (Recommended)
```bash
docker-compose up --build
```

### Manual Development Setup

**Backend Research Service:**
```bash
cd backend-research
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend Service:**
```bash
cd frontend
npm install
npm run dev
```

## Service Communication

- Frontend connects to backend via configured API endpoints
- CedarCopilot integration points to `http://localhost:3000/api/llm`
- Backend research service runs on port 8000
- Health monitoring available at `/health` endpoint

## Development Status

This is an early-stage project with basic service architecture in place. Current implementation includes:
- ✅ Basic frontend routing and UI framework
- ✅ Backend API foundation with health checks
- ✅ Docker containerization setup
- ✅ Development environment configuration

## Next Steps

The platform is ready for feature development including:
- Fact-checking algorithms and research tools
- Content analysis and verification systems
- Database integration for storing research results
- User authentication and management
- Enhanced video analysis capabilities
