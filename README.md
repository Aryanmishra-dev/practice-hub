#  PracticeHub

A modern, full-stack **MCQ (Multiple Choice Questions) practice platform** for learning and skill assessment.

> Build engaging, scalable quiz applications with **Next.js** frontend and **FastAPI** backend.

---

## What is PracticeHub?

PracticeHub is a complete learning platform where you can:
- ✅ Take practice quizzes on any topic
- ✅ Get instant feedback on your answers
- ✅ Track progress and performance metrics
- ✅ Practice at different difficulty levels (Easy → Expert)
- ✅ Prepare for certifications and exams
- ✅ Build engaging assessments for your students/users

---

## Quick Start (5 minutes)

### Prerequisites
- Python 3.11+ and Node.js 18+ installed
- Or use Docker (recommended)

### Option 1: Using Docker (Easiest)

```bash
# Clone the project
git clone https://github.com/theogengineer/PracticeHub.git
cd PracticeHub

# Copy environment config
cp .env.example .env

# Start everything (development mode)
docker compose up --build
```

Then open:
- **Frontend (Quiz App):** http://localhost:3000
- **Backend (API):** http://localhost:8000/docs

### Option 2: Run Locally

```bash
# Clone the project
git clone https://github.com/theogengineer/PracticeHub.git
cd PracticeHub
cp .env.example .env

# Terminal 1: Start Backend
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload

# Terminal 2: Start Frontend
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000

---

## Project Structure

```
QUIZ-FORGE/
│
├── frontend/           ← React app (what users see)
│   └── src/
│       ├── app/        Quiz pages
│       └── components/ Quiz forms, questions, etc.
│
├── backend/            ← API server (handles logic)
│   └── app/
│       ├── api/        Quiz endpoints
│       ├── services/   Business logic
│       └── models/     Data schemas
│
└── database/           ← Quiz questions data
    └── seed/
        ├── quiz_easy.json
        ├── quiz_normal.json
        ├── quiz_hard.json
        └── quiz_expert.json
```

---

## Tech Stack

| Part | Technology |
|------|-----------|
| **Frontend** | Next.js 14, React 18, TypeScript, Tailwind CSS |
| **Backend** | FastAPI (Python), Uvicorn |
| **Data** | JSON files (or PostgreSQL via Supabase) |
| **Containers** | Docker & Docker Compose |

---

## Commands

### Backend Development

```bash
cd backend

make lint       # Check code quality
make test       # Run tests
make all        # Run everything
```

### Frontend Development

```bash
cd frontend

npm run dev     # Start dev server
npm run build   # Build for production
npm test        # Run tests
```

---

## API Documentation

When the backend is running (http://localhost:8000), visit:

- **Interactive API Docs:** http://localhost:8000/docs (Swagger UI)
- **Alternative Format:** http://localhost:8000/redoc (ReDoc)

---

## File Locations

| What | Where |
|------|-------|
| Environment variables | `.env.example` (copy to `.env`) |
| Quiz questions | `database/seed/` |
| Backend code | `backend/app/` |
| Frontend code | `frontend/src/` |
| Documentation | `docs/` |

---

## Need Help?

- **Getting started?** → Read [ONBOARDING.md](ONBOARDING.md)
- **Want to contribute?** → Read [CONTRIBUTING.md](CONTRIBUTING.md)
- **Deploying to production?** → Read [docs/deployment.md](docs/deployment.md)
- **Understanding the code?** → Read [docs/architecture.md](docs/architecture.md)

---

## License

MIT License - See [LICENSE]
