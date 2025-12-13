# 🧠 AI News Dashboard

> Real-time AI News Aggregation & Broadcasting Platform powered by HuggingFace models

## ✨ Features

- 📰 **Automated News Ingestion** from 20+ top AI sources
- 🤖 **AI-Powered Analysis** using HuggingFace Inference API
- 🔍 **Semantic Search** with vector embeddings (384-dim all-MiniLM-L6-v2)
- 📊 **Impact Scoring** & sentiment analysis
- 📣 **Multi-Platform Broadcasting** (LinkedIn, Email, WhatsApp)
- 🎯 **Category Filtering** (Research, Product, Business, Policy)
- ⚡ **Real-time Updates** every 15 minutes
- 🗄️ **PostgreSQL + pgvector** for similarity search

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   20+ RSS   │────▶│   Backend    │────▶│  PostgreSQL │
│   Sources   │     │   (FastAPI)  │     │  + pgvector │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           │ HuggingFace API
                           │ (Text Analysis + Embeddings)
                           ▼
                    ┌──────────────┐
                    │   Frontend   │
                    │  (Next.js)   │
                    └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- HuggingFace API Key (free tier works!)
- 4GB+ RAM

### 1. Clone & Configure

```bash
git clone <your-repo>
cd ai-news-dashboard

# Create backend .env file
cp backend/.env.example backend/.env

# Edit backend/.env and add:
# HUGGINGFACE_API_KEY=your_key_here
```

### 2. Get HuggingFace API Key

1. Go to https://huggingface.co/settings/tokens
2. Create a new token (read access is enough)
3. Copy it to `backend/.env`

### 3. Start Everything

```bash
# Build and start all services
docker-compose up --build

# OR run in detached mode
docker-compose up -d
```

### 4. Access the Dashboard

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📦 What Happens on First Run

1. ✅ PostgreSQL starts with pgvector extension
2. ✅ Alembic runs database migrations
3. ✅ 20 news sources are seeded automatically
4. ✅ HuggingFace model downloads (first time only)
5. ✅ News ingestion starts (runs every 15 min)

## 🛠️ Manual Operations

### Run Migrations

```bash
docker exec -it ai_news_backend alembic upgrade head
```

### Seed Sources Manually

```bash
docker exec -it ai_news_backend python scripts/seed_sources.py
```

### Trigger News Ingestion

```bash
docker exec -it ai_news_backend python scripts/run_ingestion.py
```

### Test HuggingFace Service

```bash
docker exec -it ai_news_backend python scripts/test_huggingface.py
```

### View Logs

```bash
# All logs
docker-compose logs -f

# Backend only
docker logs ai_news_backend --tail=100 -f

# Frontend only
docker logs ai_news_frontend --tail=100 -f
```

### Database Access

```bash
docker exec -it ai_news_db psql -U user -d ai_news

# Useful queries
\dt                           # List tables
SELECT COUNT(*) FROM news_items;
SELECT * FROM sources;
```

## 🔧 Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

## 📚 API Endpoints

### News Endpoints

- `GET /api/v1/news/` - Get all news (with filters)
- `GET /api/v1/news/{id}` - Get specific news item
- `POST /api/v1/news/search` - Semantic search
- `GET /api/v1/news/categories/list` - Get all categories
- `GET /api/v1/news/stats/dashboard` - Dashboard statistics

### Source Endpoints

- `GET /api/v1/sources/` - List all sources
- `POST /api/v1/sources/` - Add new source

### Broadcast Endpoints

- `POST /api/v1/broadcast/` - Broadcast news item

## 🎯 Models Used

### Text Analysis
- **Model**: Any HuggingFace model (default: GPT-2-style models)
- **Task**: Summarization, impact scoring, sentiment analysis
- **Fallback**: Keyword-based analysis if API fails

### Embeddings
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Execution**: Local (fast, no API calls needed!)

## 🔐 Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/ai_news

# Security
SECRET_KEY=your-secret-key-here

# HuggingFace
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
HUGGINGFACE_MODEL_ID=sentence-transformers/all-MiniLM-L6-v2
HUGGINGFACE_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=30

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 🐛 Troubleshooting

### No news appearing?

```bash
# Check if sources exist
docker exec -it ai_news_db psql -U user -d ai_news -c "SELECT * FROM sources;"

# Manually trigger ingestion
docker exec -it ai_news_backend python scripts/run_ingestion.py

# Check backend logs
docker logs ai_news_backend --tail=50
```

### HuggingFace API errors?

- Free tier has rate limits (30 req/min for some endpoints)
- The app uses local embeddings by default (no API calls)
- Text analysis might hit limits - increase MAX_REQUESTS_PER_MINUTE

### Database migration issues?

```bash
# Reset migrations
docker exec -it ai_news_backend alembic downgrade base
docker exec -it ai_news_backend alembic upgrade head

# Or rebuild from scratch
docker-compose down -v
docker-compose up --build
```

## 📈 Production Deployment

### Recommended Stack

- **Backend**: Railway / Render / Fly.io
- **Frontend**: Vercel / Netlify
- **Database**: Neon / Supabase (with pgvector)

### Production Checklist

- [ ] Use strong SECRET_KEY
- [ ] Set BACKEND_CORS_ORIGINS to production URLs
- [ ] Use production database (not SQLite)
- [ ] Enable HTTPS
- [ ] Set up monitoring (Sentry recommended)
- [ ] Configure proper rate limiting
- [ ] Set up backup strategy
- [ ] Use environment-specific .env files

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use for any purpose!

## 🙏 Acknowledgments

- HuggingFace for amazing models and APIs
- FastAPI team for the incredible framework
- pgvector for vector similarity search

---

Built with ❤️ using FastAPI, Next.js, and HuggingFace