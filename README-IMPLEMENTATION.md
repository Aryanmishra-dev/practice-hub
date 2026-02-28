# 🎯 MCQ Practice Platform

A production-ready Multiple Choice Question practice platform with analytics, built with **Next.js 14**, **FastAPI**, and **Supabase**.

## 📋 Overview

This platform helps users prepare for exams through curated MCQ practice with:
- **Smart Practice**: Questions organized by category and difficulty
- **Instant Feedback**: Detailed explanations for each answer
- **Progress Tracking**: Analytics to identify strengths and weaknesses
- **Personalized Recommendations**: AI-driven suggestions for improvement

## 🏗️ Project Structure

```
Project-00/
├── frontend/                 # Next.js 14 frontend application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities and API client
│   │   └── types/           # TypeScript types
│   └── package.json
│
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/            # Config and security
│   │   └── models/          # Pydantic schemas
│   └── pyproject.toml
│
├── database/                 # Database schema and migrations
│   ├── schema.sql           # PostgreSQL schema
│   ├── seed.sql             # Initial data
│   └── import_questions.py  # Question import script
│
├── quiz_*.json              # Question bank files
├── .cursorrules             # MCP rules for AI assistance
└── MCQ_Platform_Master_Prompt.md  # Development guide
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (or Supabase account)

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your configuration
npm run dev
```

Frontend will be available at http://localhost:3000

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

Backend API will be available at http://localhost:8000
API docs at http://localhost:8000/docs

### Database Setup (Supabase)

1. Create a new Supabase project at https://supabase.com
2. Run the SQL in `database/schema.sql` in the Supabase SQL editor
3. Run `database/seed.sql` to add initial data
4. Update environment variables with your Supabase credentials

## 🎮 Features

### For Users
- **Practice Quizzes**: Select category, difficulty, and question count
- **Instant Feedback**: See if your answer is correct with explanations
- **Progress Dashboard**: Track accuracy, streaks, and improvement
- **Review Mode**: Review all questions after completing a quiz

### For Admins
- **Bulk Upload**: Import questions via JSON
- **Question Management**: Edit, delete, and deactivate questions
- **Analytics Dashboard**: View platform-wide statistics

## 📊 Question Format

Questions are stored in JSON files with the following format:

```json
{
  "id": "easy_01",
  "question": "What is the minimum recommended CPU speed?",
  "options": [
    "1.5 GHz",
    "2.0 GHz",
    "2.2 GHz",
    "3.0 GHz"
  ],
  "answer": "2.2 GHz",
  "difficulty": "Easy",
  "explanation": "According to sizing considerations..."
}
```

## 🔧 Configuration

### Frontend Environment Variables

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend Environment Variables

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_service_role_key
SECRET_KEY=your_secret_key
CORS_ORIGINS=http://localhost:3000
```

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI**: Tailwind CSS + Radix UI
- **State**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod

### Backend
- **Framework**: FastAPI
- **Validation**: Pydantic
- **Auth**: JWT + Supabase Auth

### Database
- **PostgreSQL** via Supabase
- **Row Level Security** (RLS)
- **Real-time subscriptions** (optional)

## 📝 MCP Rules

See `.cursorrules` for development guidelines including:
- Single Responsibility Components
- Data Flow Integrity
- Security-First Design
- Performance Standards
- Code Quality Gates

## 🧪 Testing

### Frontend
```bash
cd frontend
npm test
```

### Backend
```bash
cd backend
pytest
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/categories` | List all categories |
| GET | `/api/v1/categories/{id}/questions` | Get questions by category |
| POST | `/api/v1/quiz/start` | Start a new quiz |
| POST | `/api/v1/quiz/submit` | Submit an answer |
| GET | `/api/v1/user/progress` | Get user progress |

## 🚢 Deployment

### Frontend (Vercel)
1. Push to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy

### Backend (Railway/Render)
1. Push to GitHub
2. Create new service
3. Set environment variables
4. Deploy

### Database (Supabase)
1. Use production Supabase project
2. Enable RLS policies
3. Set up backups

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For questions or issues, please open a GitHub issue.

---

Built with ❤️ for exam preparation
