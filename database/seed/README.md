# Quiz Data Seeds

This directory contains the seed data for the QUIZ-FORGE platform — all quiz questions organized by difficulty level.

## Files

| File | Description | Purpose |
|------|-------------|---------|
| `quiz_bank.json` | Master question bank | Contains all available questions |
| `quiz_easy.json` | Easy difficulty questions | For beginner-level practice |
| `quiz_normal.json` | Medium difficulty questions | For intermediate-level practice |
| `quiz_hard.json` | Hard difficulty questions | For advanced-level practice |
| `quiz_expert.json` | Expert difficulty questions | For expert-level practice |

## Usage

### Local Development
The quiz JSON files are automatically mounted from this directory when running with Docker Compose:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Backend Code
The backend looks for these files using the `_resolve_data_file()` function in [`backend/app/repositories/quiz_repository.py`](../../backend/app/repositories/quiz_repository.py), which checks:
1. Docker mounted path: `/app/data/`
2. Seed directory: `database/seed/`
3. Project root: `QUIZ-FORGE/` (fallback)

### Importing Questions to Database
To import questions from these JSON files into a Supabase database:
```bash
python database/import_questions.py
```

## JSON Schema

Each quiz JSON file follows this structure:

```json
{
  "questions": [
    {
      "id": "unique-id",
      "category": "category-name",
      "difficulty": "easy|normal|hard|expert",
      "question": "Question text here?",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": 0,
      "explanation": "Explanation of the correct answer"
    }
  ]
}
```

## Adding New Questions

To add new questions:
1. Edit the appropriate JSON file (`quiz_easy.json`, `quiz_normal.json`, etc.)
2. Follow the schema above
3. Ensure unique IDs across all files
4. Run import script if using database backend:
   ```bash
   python database/import_questions.py
   ```

## Notes

- All JSON files are mounted as **read-only** in Docker for data integrity
- The backend automatically caches loaded questions in memory
- Question IDs should be unique across all files
- This data is used for in-memory storage; for persistent storage, use the `import_questions.py` script
