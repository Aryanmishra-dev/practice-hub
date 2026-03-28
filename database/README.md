# Database Directory

This directory contains database schema definitions, seed data, and utilities for the QUIZ-FORGE platform.

## Structure

```
database/
├── seed/                    # Quiz question seed data (JSON files)
│   ├── README.md           # Seed data documentation
│   ├── quiz_bank.json      # Master question bank
│   ├── quiz_easy.json      # Easy difficulty questions
│   ├── quiz_normal.json    # Normal difficulty questions
│   ├── quiz_hard.json      # Hard difficulty questions
│   └── quiz_expert.json    # Expert difficulty questions
├── schema.sql              # Database schema definition
├── seed.sql                # Initial database population SQL
└── import_questions.py     # Python script to import JSON questions to database
```

## Files

### `schema.sql`
Database schema definition for Supabase PostgreSQL. Contains:
- Table definitions for users, quizzes, questions, answers, progress tracking
- Indexes for query performance
- Foreign key relationships
- Row-level security (RLS) policies

### `seed.sql`
Initial data population SQL script. Loads:
- system categories
- Base configuration data
- Test users (if applicable)

Run this after creating tables via `schema.sql`.

### `import_questions.py`
Python utility to insert quiz questions from JSON files into the database.

**Usage:**
```bash
python database/import_questions.py
```

**Features:**
- Reads all JSON files from `seed/` directory
- Transforms and validates questions
- Inserts into Supabase PostgreSQL
- Handles duplicates and errors gracefully

**Requirements:**
- Python 3.11+
- Supabase connection (requires env vars: `SUPABASE_URL`, `SUPABASE_KEY`)

### `seed/` Directory
Contains all quiz question data in JSON format. Each file represents a difficulty level.

See [seed/README.md](seed/README.md) for detailed information about quiz data structure and format.

## Workflow

### 1. First Setup
```bash
# 1. Apply schema to create tables
# (Usually done via Supabase dashboard or migrations)

# 2. Load initial data
psql $DATABASE_URL < database/seed.sql

# 3. Import quiz questions from JSON
python database/import_questions.py
```

### 2. Adding Questions
- Edit JSON files in `seed/` directory
- Run import script to sync with database:
  ```bash
  python database/import_questions.py
  ```

### 3. Backing Up
```bash
# Export quiz questions to JSON
pg_dump --data-only --table=questions $DATABASE_URL > backup.sql
```

## Notes

- All quiz JSON files are read-only in containerized environments
- The backend can run in two modes:
  - **In-memory JSON**: Fast, good for development (no database needed)
  - **Database-backed**: Persistent, scalable for production
- Current setup uses JSON files; migration to full database is optional but recommended for production

## Related Files

- Backend repository code: [`backend/app/repositories/quiz_repository.py`](../backend/app/repositories/quiz_repository.py)
- Docker configuration: See `docker-compose.yml` for how seed data is mounted
