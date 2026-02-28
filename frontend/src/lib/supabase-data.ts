import { supabase } from "./supabase";
import { Question, Category, Difficulty } from "@/types";

/**
 * Direct Supabase data access layer
 * Fetches data directly from Supabase (no auth required)
 */

// ============= Categories =============

export async function getCategories(): Promise<Category[]> {
  const { data, error } = await supabase
    .from("categories")
    .select("*")
    .eq("is_active", true)
    .order("display_order", { ascending: true });

  if (error) {
    console.error("Error fetching categories:", error);
    throw error;
  }

  return data as Category[];
}

export async function getCategoryWithStats(): Promise<(Category & { question_count: number })[]> {
  const { data, error } = await supabase.from("category_stats").select("*");

  if (error) {
    console.error("Error fetching category stats:", error);
    throw error;
  }

  return data as (Category & { question_count: number })[];
}

// ============= Questions =============

export async function getQuestions(params?: {
  categoryId?: string;
  difficulty?: string;
  limit?: number;
  randomize?: boolean;
}): Promise<Question[]> {
  let query = supabase
    .from("questions")
    .select("*")
    .eq("is_active", true);

  if (params?.categoryId) {
    query = query.eq("category_id", params.categoryId);
  }

  if (params?.difficulty) {
    query = query.eq("difficulty", params.difficulty);
  }

  if (params?.limit) {
    query = query.limit(params.limit);
  }

  const { data, error } = await query;

  if (error) {
    console.error("Error fetching questions:", error);
    throw error;
  }

  let questions = data as Question[];

  // Randomize if requested
  if (params?.randomize) {
    questions = questions.sort(() => Math.random() - 0.5);
  }

  return questions;
}

export async function getQuestionById(id: string): Promise<Question | null> {
  const { data, error } = await supabase
    .from("questions")
    .select("*")
    .eq("id", id)
    .single();

  if (error) {
    console.error("Error fetching question:", error);
    return null;
  }

  return data as Question;
}

// ============= Quiz Sessions =============

export async function createQuizSession(params: {
  categoryId?: string;
  difficulty?: string;
  questionCount: number;
}): Promise<{ sessionId: string; questions: Question[] }> {
  // Fetch questions based on params
  const questions = await getQuestions({
    categoryId: params.categoryId,
    difficulty: params.difficulty,
    limit: params.questionCount,
    randomize: true,
  });

  const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  return {
    sessionId,
    questions,
  };
}

const supabaseData = {
  getCategories,
  getCategoryWithStats,
  getQuestions,
  getQuestionById,
  createQuizSession,
};

export default supabaseData;
