#!/usr/bin/env python3
"""
Script to import quiz questions from JSON files into the database.
Run this script to seed the database with questions from the quiz_*.json files.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
import uuid

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
SEED_DIR = PROJECT_ROOT / "database" / "seed"

QUIZ_FILES = {
    "easy": SEED_DIR / "quiz_easy.json",
    "normal": SEED_DIR / "quiz_normal.json",  # Maps to 'medium'
    "hard": SEED_DIR / "quiz_hard.json",
    "expert": SEED_DIR / "quiz_expert.json",
}

DIFFICULTY_MAP = {
    "Easy": "easy",
    "Normal": "medium",
    "Hard": "hard",
    "Expert": "expert",
}

DEFAULT_CATEGORY_ID = "c1000000-0000-0000-0000-000000000001"


def load_questions_from_json(file_path: Path) -> List[Dict[str, Any]]:
    """Load questions from a JSON file."""
    if not file_path.exists():
        print(f"Warning: File not found: {file_path}")
        return []
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def transform_question(raw_question: Dict[str, Any]) -> Dict[str, Any]:
    """Transform a question from JSON format to database format."""
    
    # Convert options from list of strings to list of objects
    options = []
    for i, opt_text in enumerate(raw_question.get("options", [])):
        options.append({
            "id": chr(65 + i),  # A, B, C, D
            "text": opt_text,
        })
    
    # Find correct option ID
    correct_answer = raw_question.get("answer", "")
    correct_option = "A"
    for i, opt_text in enumerate(raw_question.get("options", [])):
        if opt_text == correct_answer:
            correct_option = chr(65 + i)
            break
    
    # Map difficulty
    difficulty = DIFFICULTY_MAP.get(
        raw_question.get("difficulty", "Easy"), 
        "easy"
    )
    
    return {
        "id": str(uuid.uuid4()),
        "external_id": raw_question.get("id", ""),
        "category_id": DEFAULT_CATEGORY_ID,
        "difficulty": difficulty,
        "question_text": raw_question.get("question", ""),
        "options": options,
        "correct_option": correct_option,
        "explanation": raw_question.get("explanation"),
        "tags": [],
        "is_active": True,
        "version": 1,
    }


def generate_sql_insert(question: Dict[str, Any]) -> str:
    """Generate SQL INSERT statement for a question."""
    options_json = json.dumps(question["options"]).replace("'", "''")
    tags_sql = "'{}'::text[]" if not question["tags"] else f"ARRAY{question['tags']}"
    explanation = question.get("explanation", "").replace("'", "''") if question.get("explanation") else "NULL"
    explanation_sql = f"'{explanation}'" if explanation != "NULL" else "NULL"
    
    return f"""INSERT INTO questions (
    id, category_id, difficulty, question_text, options, correct_option, explanation, tags, is_active, version
) VALUES (
    '{question["id"]}',
    '{question["category_id"]}',
    '{question["difficulty"]}',
    '{question["question_text"].replace("'", "''")}',
    '{options_json}'::jsonb,
    '{question["correct_option"]}',
    {explanation_sql},
    {tags_sql},
    true,
    1
);"""


def main():
    """Main function to import questions."""
    all_questions = []
    
    print("Loading questions from JSON files...")
    
    for difficulty, file_path in QUIZ_FILES.items():
        questions = load_questions_from_json(file_path)
        print(f"  - {difficulty}: {len(questions)} questions")
        all_questions.extend(questions)
    
    print(f"\nTotal questions loaded: {len(all_questions)}")
    
    # Transform questions
    transformed = [transform_question(q) for q in all_questions]
    
    # Generate SQL file
    output_file = PROJECT_ROOT / "database" / "questions_seed.sql"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("-- Auto-generated question seed file\n")
        f.write("-- Generated from quiz_*.json files\n\n")
        f.write("BEGIN;\n\n")
        
        for q in transformed:
            f.write(generate_sql_insert(q))
            f.write("\n\n")
        
        f.write("COMMIT;\n")
    
    print(f"\nSQL file generated: {output_file}")
    print(f"Total questions: {len(transformed)}")
    
    # Also generate a JSON file for the API
    json_output = PROJECT_ROOT / "database" / "questions_transformed.json"
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(transformed, f, indent=2)
    
    print(f"JSON file generated: {json_output}")


if __name__ == "__main__":
    main()
