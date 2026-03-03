"use client";

import * as React from "react";
import { QuizResult } from "@/types";
import { cn, formatTime, calculatePercentage } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  Trophy, 
  Clock, 
  Target, 
  TrendingUp, 
  RotateCcw, 
  Home,
  CheckCircle2,
  XCircle,
  AlertTriangle
} from "lucide-react";

interface QuizSummaryProps {
  result: QuizResult;
  onRetry: () => void;
  onHome: () => void;
  onReview: () => void;
}

export function QuizSummary({ result, onRetry, onHome, onReview }: QuizSummaryProps) {
  const getScoreMessage = (accuracy: number) => {
    if (accuracy >= 90) return { message: "Excellent!", icon: Trophy, color: "text-yellow-500" };
    if (accuracy >= 70) return { message: "Good Job!", icon: CheckCircle2, color: "text-green-500" };
    if (accuracy >= 50) return { message: "Keep Practicing!", icon: TrendingUp, color: "text-blue-500" };
    return { message: "Needs Improvement", icon: AlertTriangle, color: "text-orange-500" };
  };

  const scoreInfo = getScoreMessage(result.accuracy);
  const ScoreIcon = scoreInfo.icon;

  return (
    <div className="w-full max-w-3xl mx-auto space-y-6">
      {/* Main Score Card */}
      <Card>
        <CardHeader className="text-center pb-2">
          <div className="flex justify-center mb-4">
            <div className={cn("p-4 rounded-full bg-muted", scoreInfo.color)}>
              <ScoreIcon className="h-12 w-12" />
            </div>
          </div>
          <CardTitle className="text-3xl">{scoreInfo.message}</CardTitle>
          <CardDescription className="text-lg">
            You scored {result.correct_answers} out of {result.total_questions}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center mb-6">
            <div className="relative w-40 h-40">
              <svg className="w-full h-full transform -rotate-90" role="img" aria-label={`Score: ${Math.round(result.accuracy)}%`}>
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  className="stroke-muted fill-none"
                  strokeWidth="12"
                />
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  className={cn(
                    "fill-none transition-all duration-1000",
                    result.accuracy >= 70 ? "stroke-green-500" :
                    result.accuracy >= 50 ? "stroke-yellow-500" :
                    "stroke-red-500"
                  )}
                  strokeWidth="12"
                  strokeLinecap="round"
                  strokeDasharray={`${result.accuracy * 4.4} 440`}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-4xl font-bold">{Math.round(result.accuracy)}%</span>
              </div>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center p-4 bg-muted rounded-lg">
              <Target className="h-6 w-6 mx-auto mb-2 text-primary" />
              <p className="text-2xl font-bold">{result.correct_answers}</p>
              <p className="text-sm text-muted-foreground">Correct</p>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <XCircle className="h-6 w-6 mx-auto mb-2 text-destructive" />
              <p className="text-2xl font-bold">{result.total_questions - result.correct_answers}</p>
              <p className="text-sm text-muted-foreground">Incorrect</p>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <Clock className="h-6 w-6 mx-auto mb-2 text-blue-500" />
              <p className="text-2xl font-bold">{formatTime(result.total_time_seconds)}</p>
              <p className="text-sm text-muted-foreground">Total Time</p>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <TrendingUp className="h-6 w-6 mx-auto mb-2 text-green-500" />
              <p className="text-2xl font-bold">{Math.round(result.average_time_per_question)}s</p>
              <p className="text-sm text-muted-foreground">Avg Time</p>
            </div>
          </div>

          {/* Difficulty Breakdown */}
          {Object.keys(result.difficulty_breakdown).length > 0 && (
            <div className="mb-6">
              <h4 className="font-semibold mb-3">Performance by Difficulty</h4>
              <div className="space-y-3">
                {Object.entries(result.difficulty_breakdown).map(([difficulty, stats]) => (
                  <div key={difficulty} className="flex items-center gap-3">
                    <Badge variant={difficulty as "easy" | "medium" | "hard" | "expert"} className="w-16 justify-center">
                      {difficulty}
                    </Badge>
                    <Progress 
                      value={stats.total > 0 ? (stats.correct / stats.total) * 100 : 0} 
                      className="flex-1 h-2"
                    />
                    <span className="text-sm text-muted-foreground w-16 text-right">
                      {stats.correct}/{stats.total}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations */}
          {result.recommendations && result.recommendations.length > 0 && (
            <div className="bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-6">
              <h4 className="font-semibold text-blue-800 dark:text-blue-300 mb-2">💡 Recommendations</h4>
              <ul className="space-y-1">
                {result.recommendations.map((rec, index) => (
                  <li key={index} className="text-sm text-blue-700 dark:text-blue-400">• {rec}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-3">
            <Button onClick={onReview} variant="outline" className="flex-1">
              <CheckCircle2 className="h-4 w-4 mr-2" />
              Review Answers
            </Button>
            <Button onClick={onRetry} variant="secondary" className="flex-1">
              <RotateCcw className="h-4 w-4 mr-2" />
              Try Again
            </Button>
            <Button onClick={onHome} className="flex-1">
              <Home className="h-4 w-4 mr-2" />
              Back to Home
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
