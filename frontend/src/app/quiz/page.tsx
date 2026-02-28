"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { CategorySelector } from "@/components/quiz/CategorySelector";
import { DifficultySelector } from "@/components/quiz/DifficultySelector";
import { QuestionCard } from "@/components/quiz/QuestionCard";
import { QuizProgress } from "@/components/quiz/QuizProgress";
import { QuizSummary } from "@/components/quiz/QuizSummary";
import { 
  Question, 
  Category, 
  Difficulty, 
  QuizState, 
  UserAnswer,
  QuizResult 
} from "@/types";
import { generateSessionId, shuffleArray } from "@/lib/utils";
import { ArrowRight, Play, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function QuizPage() {
  const router = useRouter();
  const { toast } = useToast();
  
  // Loading states
  const [loadingCategories, setLoadingCategories] = React.useState(true);
  const [loadingQuestions, setLoadingQuestions] = React.useState(false);
  const [categories, setCategories] = React.useState<Category[]>([]);
  const [error, setError] = React.useState<string | null>(null);
  
  // Quiz configuration state
  const [selectedCategory, setSelectedCategory] = React.useState<string | null>(null);
  const [selectedDifficulty, setSelectedDifficulty] = React.useState<Difficulty | "mixed" | null>(null);
  const [questionCount, setQuestionCount] = React.useState(10);
  
  // Quiz session state
  const [quizState, setQuizState] = React.useState<QuizState>("idle");
  const [sessionId, setSessionId] = React.useState<string>("");
  const [questions, setQuestions] = React.useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = React.useState(0);
  const [answers, setAnswers] = React.useState<Record<string, UserAnswer>>({});
  const [selectedOption, setSelectedOption] = React.useState<string | null>(null);
  const [showResult, setShowResult] = React.useState(false);
  const [timeElapsed, setTimeElapsed] = React.useState(0);
  const [questionStartTime, setQuestionStartTime] = React.useState<number>(Date.now());
  
  // Fetch categories on mount from backend API
  React.useEffect(() => {
    async function fetchCategories() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/categories`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        const mappedCategories: Category[] = data.map((cat: any) => ({
          id: cat.id,
          name: cat.name,
          description: cat.description || "",
          icon: cat.icon || "file-text",
          display_order: cat.display_order,
          is_active: cat.is_active,
          question_count: cat.question_count || 0,
          created_at: cat.created_at,
          updated_at: cat.updated_at,
        }));

        setCategories(mappedCategories);
      } catch (err) {
        console.error("Error fetching categories:", err);
        setError("Failed to load categories. Please try again.");
      } finally {
        setLoadingCategories(false);
      }
    }

    fetchCategories();
  }, []);
  
  // Timer effect
  React.useEffect(() => {
    let interval: NodeJS.Timeout;
    if (quizState === "active") {
      interval = setInterval(() => {
        setTimeElapsed((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [quizState]);
  
  // Calculate results
  const calculateResults = (): QuizResult => {
    const correctAnswers = Object.values(answers).filter((a) => a.is_correct).length;
    const totalTime = Object.values(answers).reduce((acc, a) => acc + a.time_taken_seconds, 0);
    
    const difficultyBreakdown: Record<Difficulty, { total: number; correct: number }> = {
      easy: { total: 0, correct: 0 },
      medium: { total: 0, correct: 0 },
      hard: { total: 0, correct: 0 },
      expert: { total: 0, correct: 0 },
    };
    
    questions.forEach((q) => {
      const answer = answers[q.id];
      if (difficultyBreakdown[q.difficulty]) {
        difficultyBreakdown[q.difficulty].total++;
        if (answer?.is_correct) {
          difficultyBreakdown[q.difficulty].correct++;
        }
      }
    });
    
    return {
      session_id: sessionId,
      total_questions: questions.length,
      correct_answers: correctAnswers,
      accuracy: (correctAnswers / questions.length) * 100,
      total_time_seconds: totalTime,
      average_time_per_question: totalTime / questions.length,
      difficulty_breakdown: difficultyBreakdown,
      weak_areas: [],
      recommendations: [
        "Practice more questions in the areas you struggled with",
        "Review the explanations for incorrect answers",
      ],
    };
  };
  
  // Start quiz - fetch questions from backend API
  const startQuiz = async () => {
    if (!selectedCategory || !selectedDifficulty) return;
    
    setLoadingQuestions(true);
    setError(null);
    
    try {
      const params = new URLSearchParams();
      if (selectedDifficulty !== "mixed") {
        params.set("difficulty", selectedDifficulty);
      }
      params.set("limit", String(questionCount));

      const res = await fetch(
        `${API_BASE_URL}/api/v1/categories/${selectedCategory}/questions?${params}`
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      if (!data || data.length === 0) {
        setError("No questions found for the selected criteria.");
        setLoadingQuestions(false);
        return;
      }

      // Transform questions from API response
      const transformedQuestions: Question[] = data.map((q: any) => ({
        id: q.id,
        category_id: q.category_id,
        difficulty: q.difficulty as Difficulty,
        question_text: q.question_text,
        options: q.options as { id: string; text: string }[],
        correct_option: q.correct_option,
        explanation: q.explanation || undefined,
        tags: q.tags || [],
        is_active: q.is_active ?? true,
        version: q.version ?? 1,
        created_at: q.created_at || new Date().toISOString(),
        updated_at: q.updated_at || new Date().toISOString(),
      }));

      const shuffled = shuffleArray(transformedQuestions).slice(0, questionCount);
      
      const newSessionId = generateSessionId();
      setSessionId(newSessionId);
      
      setQuestions(shuffled);
      setCurrentIndex(0);
      setAnswers({});
      setSelectedOption(null);
      setShowResult(false);
      setTimeElapsed(0);
      setQuestionStartTime(Date.now());
      setQuizState("active");
    } catch (err) {
      console.error("Error fetching questions:", err);
      setError("Failed to load questions. Please try again.");
    } finally {
      setLoadingQuestions(false);
    }
  };
  
  // Submit answer
  const submitAnswer = () => {
    if (!selectedOption) return;
    
    const currentQuestion = questions[currentIndex];
    const isCorrect = selectedOption === currentQuestion.correct_option;
    const timeTaken = Math.round((Date.now() - questionStartTime) / 1000);
    
    const answer: UserAnswer = {
      question_id: currentQuestion.id,
      selected_option: selectedOption,
      is_correct: isCorrect,
      time_taken_seconds: timeTaken,
      answered_at: new Date().toISOString(),
    };
    
    setAnswers((prev) => ({
      ...prev,
      [currentQuestion.id]: answer,
    }));
    
    setShowResult(true);
  };
  
  // Next question
  const nextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setSelectedOption(null);
      setShowResult(false);
      setQuestionStartTime(Date.now());
    } else {
      toast({
        title: "Quiz Completed!",
        description: "Check your results below.",
      });
      setQuizState("completed");
    }
  };
  
  // Reset quiz
  const resetQuiz = () => {
    setQuizState("idle");
    setSelectedCategory(null);
    setSelectedDifficulty(null);
    setQuestions([]);
    setCurrentIndex(0);
    setAnswers({});
    setSelectedOption(null);
    setShowResult(false);
    setTimeElapsed(0);
    setError(null);
  };
  
  // Loading state for categories
  if (loadingCategories) {
    return (
      <div className="container py-8">
        <div className="flex flex-col items-center justify-center min-h-[400px]">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="mt-4 text-muted-foreground">Loading categories...</p>
        </div>
      </div>
    );
  }
  
  // Render based on quiz state
  if (quizState === "completed") {
    return (
      <div className="container py-8">
        <QuizSummary
          result={calculateResults()}
          onRetry={startQuiz}
          onHome={() => router.push("/")}
          onReview={() => setQuizState("reviewing")}
        />
      </div>
    );
  }
  
  if (quizState === "reviewing") {
    return (
      <div className="container py-8">
        <div className="max-w-3xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Review Answers</h2>
            <Button onClick={() => setQuizState("completed")}>
              Back to Summary
            </Button>
          </div>
          <div className="space-y-6">
            {questions.map((question, index) => {
              const answer = answers[question.id];
              return (
                <QuestionCard
                  key={question.id}
                  question={question}
                  questionNumber={index + 1}
                  totalQuestions={questions.length}
                  selectedOption={answer?.selected_option || null}
                  onSelectOption={() => {}}
                  showResult={true}
                  isCorrect={answer?.is_correct}
                  disabled={true}
                />
              );
            })}
          </div>
        </div>
      </div>
    );
  }
  
  if (quizState === "active") {
    const currentQuestion = questions[currentIndex];
    const correctAnswers = Object.values(answers).filter((a) => a.is_correct).length;
    
    return (
      <div className="container py-8">
        <QuizProgress
          currentQuestion={currentIndex + 1}
          totalQuestions={questions.length}
          correctAnswers={correctAnswers}
          timeElapsed={timeElapsed}
        />
        
        <QuestionCard
          question={currentQuestion}
          questionNumber={currentIndex + 1}
          totalQuestions={questions.length}
          selectedOption={selectedOption}
          onSelectOption={setSelectedOption}
          showResult={showResult}
          isCorrect={answers[currentQuestion.id]?.is_correct}
          disabled={showResult}
        />
        
        <div className="flex justify-center gap-4 mt-6">
          {!showResult ? (
            <Button
              size="lg"
              onClick={submitAnswer}
              disabled={!selectedOption}
              className="min-w-[150px]"
            >
              Submit Answer
            </Button>
          ) : (
            <Button
              size="lg"
              onClick={nextQuestion}
              className="min-w-[150px]"
            >
              {currentIndex < questions.length - 1 ? (
                <>
                  Next Question
                  <ArrowRight className="ml-2 h-4 w-4" />
                </>
              ) : (
                "See Results"
              )}
            </Button>
          )}
        </div>
      </div>
    );
  }
  
  // Idle state - Quiz configuration
  return (
    <div className="container py-8">
      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Start a Quiz</CardTitle>
            <CardDescription>
              Configure your quiz settings and test your knowledge
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {error && (
              <div className="bg-destructive/10 text-destructive px-4 py-3 rounded-lg">
                {error}
              </div>
            )}
            
            {/* Category Selection */}
            <div className="space-y-2">
              <Label>Select Category</Label>
              <CategorySelector
                categories={categories}
                selectedCategory={selectedCategory}
                onSelectCategory={setSelectedCategory}
              />
            </div>
            
            {/* Difficulty Selection */}
            <div className="space-y-2">
              <Label>Select Difficulty</Label>
              <DifficultySelector
                selectedDifficulty={selectedDifficulty}
                onSelectDifficulty={setSelectedDifficulty}
              />
            </div>
            
            {/* Question Count */}
            <div className="space-y-2">
              <Label htmlFor="question-count">Number of Questions</Label>
              <div className="flex gap-2">
                {[5, 10, 15, 20, 25].map((count) => (
                  <Button
                    key={count}
                    variant={questionCount === count ? "default" : "outline"}
                    size="sm"
                    onClick={() => setQuestionCount(count)}
                  >
                    {count}
                  </Button>
                ))}
              </div>
            </div>
            
            {/* Start Button */}
            <Button
              size="lg"
              className="w-full"
              onClick={startQuiz}
              disabled={!selectedCategory || !selectedDifficulty || loadingQuestions}
            >
              {loadingQuestions ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Loading Questions...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  Start Quiz
                </>
              )}
            </Button>
            
            {/* Info */}
            <p className="text-sm text-muted-foreground text-center">
              Questions are randomly selected from the database.
              {selectedDifficulty === "mixed" && " Mixed mode includes all difficulty levels."}
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
