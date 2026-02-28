import {
  ApiResponse,
  Category,
  Question,
  QuizConfig,
  QuizResult,
  UserProgress,
  UserAnswer,
  QuizHistory,
  PaginatedResponse,
  BulkUploadResult,
  AdminStats,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Base API fetch function with error handling
 */
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}/api/v1${endpoint}`;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "An error occurred" }));
    throw new Error(error.detail || `API Error: ${response.status}`);
  }

  return response.json();
}

// ============= Categories API =============

export const categoriesApi = {
  /**
   * Get all active categories
   */
  getAll: () => apiFetch<Category[]>("/categories"),

  /**
   * Get category by ID
   */
  getById: (id: string) => apiFetch<Category>(`/categories/${id}`),

  /**
   * Get category with question count
   */
  getWithStats: () => apiFetch<Category[]>("/categories/stats"),
};

// ============= Questions API =============

export const questionsApi = {
  /**
   * Get questions by category with optional filters
   */
  getByCategory: (
    categoryId: string,
    params?: {
      difficulty?: string;
      limit?: number;
      exclude_answered?: boolean;
    }
  ) => {
    const searchParams = new URLSearchParams();
    if (params?.difficulty) searchParams.set("difficulty", params.difficulty);
    if (params?.limit) searchParams.set("limit", params.limit.toString());
    if (params?.exclude_answered !== undefined) {
      searchParams.set("exclude_answered", params.exclude_answered.toString());
    }
    const query = searchParams.toString();
    return apiFetch<Question[]>(
      `/categories/${categoryId}/questions${query ? `?${query}` : ""}`
    );
  },

  /**
   * Get single question by ID
   */
  getById: (id: string) => apiFetch<Question>(`/questions/${id}`),

  /**
   * Start a quiz session
   */
  startQuiz: (config: QuizConfig) =>
    apiFetch<{ session_id: string; questions: Question[] }>("/quiz/start", {
      method: "POST",
      body: JSON.stringify(config),
    }),
};

// ============= Quiz API =============

export const quizApi = {
  /**
   * Submit an answer
   */
  submitAnswer: (data: {
    question_id: string;
    selected_option: string;
    time_taken_seconds: number;
  }) =>
    apiFetch<{
      is_correct: boolean;
      correct_option: string;
      explanation: string | null;
    }>("/quiz/submit", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  /**
   * Complete a quiz session
   */
  completeQuiz: (sessionId: string, answers: UserAnswer[]) =>
    apiFetch<QuizResult>(`/quiz/${sessionId}/complete`, {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),

  /**
   * Get quiz result
   */
  getResult: (sessionId: string) =>
    apiFetch<QuizResult>(`/quiz/${sessionId}/result`),
};

// ============= User API =============

export const userApi = {
  /**
   * Get user progress overview
   */
  getProgress: () => apiFetch<UserProgress>("/user/progress"),

  /**
   * Get user analytics for a specific category
   */
  getCategoryAnalytics: (categoryId: string) =>
    apiFetch<UserProgress>(`/user/analytics/${categoryId}`),

  /**
   * Get quiz history
   */
  getHistory: (params?: { limit?: number; offset?: number }) => {
    const searchParams = new URLSearchParams();
    if (params?.limit) searchParams.set("limit", params.limit.toString());
    if (params?.offset) searchParams.set("offset", params.offset.toString());
    const query = searchParams.toString();
    return apiFetch<PaginatedResponse<QuizHistory>>(
      `/user/history${query ? `?${query}` : ""}`
    );
  },

  /**
   * Get personalized recommendations
   */
  getRecommendations: () =>
    apiFetch<{
      recommended_category: string;
      recommended_difficulty: string;
      reason: string;
    }>("/user/recommendations"),
};

// ============= Admin API =============

export const adminApi = {
  /**
   * Bulk upload categories
   */
  uploadCategories: (categories: Partial<Category>[]) =>
    apiFetch<BulkUploadResult>("/admin/categories/bulk", {
      method: "POST",
      body: JSON.stringify({ categories }),
    }),

  /**
   * Bulk upload questions
   */
  uploadQuestions: (questions: Partial<Question>[]) =>
    apiFetch<BulkUploadResult>("/admin/questions/bulk", {
      method: "POST",
      body: JSON.stringify({ questions }),
    }),

  /**
   * Get all questions (admin view)
   */
  getAllQuestions: (params?: {
    page?: number;
    page_size?: number;
    category_id?: string;
    difficulty?: string;
  }) => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.set("page", params.page.toString());
    if (params?.page_size) searchParams.set("page_size", params.page_size.toString());
    if (params?.category_id) searchParams.set("category_id", params.category_id);
    if (params?.difficulty) searchParams.set("difficulty", params.difficulty);
    const query = searchParams.toString();
    return apiFetch<PaginatedResponse<Question>>(
      `/admin/questions${query ? `?${query}` : ""}`
    );
  },

  /**
   * Update a question
   */
  updateQuestion: (id: string, data: Partial<Question>) =>
    apiFetch<Question>(`/admin/questions/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  /**
   * Delete a question (soft delete)
   */
  deleteQuestion: (id: string) =>
    apiFetch<void>(`/admin/questions/${id}`, {
      method: "DELETE",
    }),

  /**
   * Get admin dashboard stats
   */
  getStats: () => apiFetch<AdminStats>("/admin/stats"),
};

const api = {
  categories: categoriesApi,
  questions: questionsApi,
  quiz: quizApi,
  user: userApi,
  admin: adminApi,
};

export default api;
