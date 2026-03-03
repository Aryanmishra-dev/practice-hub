"use client";

import * as React from "react";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { 
  BarChart3, 
  Target, 
  Clock, 
  TrendingUp,
  Trophy,
  BookOpen,
  ArrowRight,
  Loader2,
  Flame,
  Zap,
} from "lucide-react";
import { Difficulty } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface UserProgress {
  total_questions_answered: number;
  overall_accuracy: number;
  total_time_spent_seconds: number;
  current_streak: number;
  longest_streak: number;
  categories_practiced: number;
  favorite_category: string | null;
  improvement_trend: string;
  last_7_days_accuracy: number;
  stats_by_category: Array<{
    id: string;
    category_name: string | null;
    total_attempts: number;
    correct_attempts: number;
    accuracy: number;
    avg_time_seconds: number | null;
  }>;
  stats_by_difficulty: Record<string, { total: number; correct: number; accuracy: number }>;
}

interface QuizHistoryItem {
  id: string;
  category_name: string;
  difficulty: string;
  score: number;
  total_questions: number;
  accuracy: number;
  completed_at: string;
}

function formatTime(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
}

function formatDate(dateString: string): string {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(dateString));
}

function getTrendIcon(trend: string) {
  if (trend === "improving") return { icon: TrendingUp, color: "text-green-500", label: "Improving" };
  if (trend === "declining") return { icon: TrendingUp, color: "text-red-500 rotate-180", label: "Declining" };
  return { icon: Zap, color: "text-yellow-500", label: "Stable" };
}

export default function ProgressPage() {
  const [progress, setProgress] = React.useState<UserProgress | null>(null);
  const [history, setHistory] = React.useState<QuizHistoryItem[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    async function fetchData() {
      try {
        const [progressRes, historyRes] = await Promise.all([
          fetch(`${API_BASE_URL}/api/v1/user/progress`),
          fetch(`${API_BASE_URL}/api/v1/user/history?limit=10`),
        ]);

        if (!progressRes.ok || !historyRes.ok) {
          throw new Error("Failed to fetch progress data");
        }

        const progressData = await progressRes.json();
        const historyData = await historyRes.json();

        setProgress(progressData);
        setHistory(historyData.items || []);
      } catch (err) {
        console.error("Error fetching progress:", err);
        setError("Could not load progress data. Make sure the backend is running.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="container py-8">
        <div className="max-w-6xl mx-auto space-y-6">
          <div>
            <Skeleton className="h-9 w-48 mb-2" />
            <Skeleton className="h-5 w-80" />
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} className="h-32 rounded-lg" />
            ))}
          </div>
          <Skeleton className="h-64 rounded-lg" />
          <Skeleton className="h-48 rounded-lg" />
        </div>
      </div>
    );
  }

  if (error || !progress) {
    return (
      <div className="container py-8">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Your Progress</h1>
            <p className="text-muted-foreground">
              Track your learning journey and identify areas for improvement
            </p>
          </div>
          <Card>
            <CardContent className="pt-6">
              <div className="text-center py-8">
                <Trophy className="h-16 w-16 mx-auto mb-4 text-primary opacity-80" />
                <h2 className="text-2xl font-bold mb-2">Progress Tracking</h2>
                <p className="text-muted-foreground max-w-md mx-auto mb-2">
                  {error || "Start a quiz to see your progress here!"}
                </p>
                <Link href="/quiz">
                  <Button size="lg" className="gap-2 mt-4">
                    Start a Quiz
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  const trendInfo = getTrendIcon(progress.improvement_trend);
  const TrendIcon = trendInfo.icon;

  return (
    <div className="container py-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Your Progress</h1>
          <p className="text-muted-foreground">
            Track your learning journey and identify areas for improvement
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardContent className="pt-6 text-center">
              <Target className="h-8 w-8 mx-auto mb-2 text-primary" />
              <p className="text-3xl font-bold">{progress.total_questions_answered}</p>
              <p className="text-sm text-muted-foreground">Questions Answered</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <BarChart3 className="h-8 w-8 mx-auto mb-2 text-primary" />
              <p className="text-3xl font-bold">{Math.round(progress.overall_accuracy)}%</p>
              <p className="text-sm text-muted-foreground">Overall Accuracy</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <Clock className="h-8 w-8 mx-auto mb-2 text-primary" />
              <p className="text-3xl font-bold">{formatTime(progress.total_time_spent_seconds)}</p>
              <p className="text-sm text-muted-foreground">Total Study Time</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <Flame className="h-8 w-8 mx-auto mb-2 text-orange-500" />
              <p className="text-3xl font-bold">{progress.current_streak}</p>
              <p className="text-sm text-muted-foreground">Day Streak</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Performance by Difficulty */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Performance by Difficulty
              </CardTitle>
              <CardDescription>
                Your accuracy across difficulty levels
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {(["easy", "medium", "hard", "expert"] as const).map((diff) => {
                const stats = progress.stats_by_difficulty[diff];
                if (!stats) return null;
                return (
                  <div key={diff} className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <Badge variant={diff as any} className="capitalize">
                        {diff}
                      </Badge>
                      <span className="text-sm text-muted-foreground">
                        {stats.correct}/{stats.total} ({Math.round(stats.accuracy)}%)
                      </span>
                    </div>
                    <Progress
                      value={stats.accuracy}
                      className="h-2"
                      indicatorClassName={
                        stats.accuracy >= 70
                          ? "bg-green-500"
                          : stats.accuracy >= 50
                          ? "bg-yellow-500"
                          : "bg-red-500"
                      }
                    />
                  </div>
                );
              })}
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Trophy className="h-5 w-5" />
                Highlights
              </CardTitle>
              <CardDescription>Key metrics at a glance</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted">
                <span className="text-sm font-medium">7-Day Accuracy</span>
                <span className="font-bold">{Math.round(progress.last_7_days_accuracy)}%</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted">
                <span className="text-sm font-medium">Longest Streak</span>
                <span className="font-bold">{progress.longest_streak} days</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted">
                <span className="text-sm font-medium">Categories Practiced</span>
                <span className="font-bold">{progress.categories_practiced}</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-muted">
                <span className="text-sm font-medium">Trend</span>
                <span className={`font-bold flex items-center gap-1 ${trendInfo.color}`}>
                  <TrendIcon className="h-4 w-4" />
                  {trendInfo.label}
                </span>
              </div>
              {progress.favorite_category && (
                <div className="flex items-center justify-between p-3 rounded-lg bg-muted">
                  <span className="text-sm font-medium">Favorite Category</span>
                  <span className="font-bold text-sm">{progress.favorite_category}</span>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Recent Quiz History */}
        {history.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                Recent Quizzes
              </CardTitle>
              <CardDescription>Your last {history.length} quiz sessions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {history.map((quiz) => (
                  <div
                    key={quiz.id}
                    className="flex items-center justify-between p-3 rounded-lg border"
                  >
                    <div className="flex items-center gap-3">
                      <Badge variant={quiz.difficulty as any} className="capitalize">
                        {quiz.difficulty}
                      </Badge>
                      <div>
                        <p className="font-medium text-sm">{quiz.category_name}</p>
                        <p className="text-xs text-muted-foreground">
                          {formatDate(quiz.completed_at)}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold">
                        {quiz.score}/{quiz.total_questions}
                      </p>
                      <p
                        className={`text-xs font-medium ${
                          quiz.accuracy >= 70
                            ? "text-green-600 dark:text-green-400"
                            : quiz.accuracy >= 50
                            ? "text-yellow-600 dark:text-yellow-400"
                            : "text-red-600 dark:text-red-400"
                        }`}
                      >
                        {Math.round(quiz.accuracy)}%
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* CTA */}
        <div className="mt-8 text-center">
          <Link href="/quiz">
            <Button size="lg" className="gap-2">
              Continue Practicing
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
