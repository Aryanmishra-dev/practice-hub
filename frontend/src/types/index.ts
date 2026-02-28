// Question and Quiz Types
export type Difficulty = 'easy' | 'medium' | 'hard' | 'expert';

export interface Option {
  id: string;
  text: string;
}

export interface Question {
  id: string;
  category_id: string;
  difficulty: Difficulty;
  question_text: string;
  options: Option[];
  correct_option: string;
  explanation: string | null;
  tags: string[];
  is_active: boolean;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: string;
  name: string;
  description: string | null;
  icon: string | null;
  display_order: number;
  is_active: boolean;
  question_count?: number;
  created_at: string;
  updated_at: string;
}

// Quiz Session Types
export type QuizState = 'idle' | 'loading' | 'active' | 'reviewing' | 'completed';

export interface UserAnswer {
  question_id: string;
  selected_option: string;
  is_correct: boolean;
  time_taken_seconds: number;
  answered_at: string;
}

export interface QuizSession {
  id: string;
  category_id: string;
  category_name: string;
  difficulty: Difficulty | 'mixed';
  questions: Question[];
  current_index: number;
  answers: Record<string, UserAnswer>;
  state: QuizState;
  started_at: string;
  completed_at: string | null;
  time_limit_seconds: number | null;
  time_elapsed_seconds: number;
}

export interface QuizConfig {
  category_id: string;
  difficulty: Difficulty | 'mixed';
  question_count: number;
  time_limit_seconds: number | null;
  exclude_answered: boolean;
}

export interface QuizResult {
  session_id: string;
  total_questions: number;
  correct_answers: number;
  accuracy: number;
  total_time_seconds: number;
  average_time_per_question: number;
  difficulty_breakdown: Record<Difficulty, { total: number; correct: number }>;
  weak_areas: string[];
  recommendations: string[];
}

// User and Analytics Types
export interface User {
  id: string;
  email: string;
  full_name: string | null;
  avatar_url: string | null;
  role: 'user' | 'admin';
  created_at: string;
}

export interface UserStats {
  id: string;
  user_id: string;
  category_id: string | null;
  category_name: string | null;
  difficulty: Difficulty | null;
  total_attempts: number;
  correct_attempts: number;
  accuracy: number;
  avg_time_seconds: number;
  last_practiced_at: string | null;
}

export interface UserProgress {
  total_questions_answered: number;
  overall_accuracy: number;
  total_time_spent_seconds: number;
  current_streak: number;
  longest_streak: number;
  categories_practiced: number;
  favorite_category: string | null;
  improvement_trend: 'improving' | 'stable' | 'declining';
  last_7_days_accuracy: number;
  stats_by_category: UserStats[];
  stats_by_difficulty: Record<Difficulty, { total: number; correct: number; accuracy: number }>;
}

export interface QuizHistory {
  id: string;
  category_name: string;
  difficulty: Difficulty;
  score: number;
  total_questions: number;
  accuracy: number;
  completed_at: string;
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Admin Types
export interface BulkUploadResult {
  success_count: number;
  error_count: number;
  errors: Array<{
    row: number;
    message: string;
  }>;
}

export interface AdminStats {
  total_questions: number;
  total_categories: number;
  total_users: number;
  questions_by_difficulty: Record<Difficulty, number>;
  questions_by_category: Record<string, number>;
  active_users_today: number;
  quizzes_taken_today: number;
}
