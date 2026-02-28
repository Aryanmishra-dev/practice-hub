"use client";

import * as React from "react";
import { Progress } from "@/components/ui/progress";
import { cn, formatTime } from "@/lib/utils";

interface QuizProgressProps {
  currentQuestion: number;
  totalQuestions: number;
  correctAnswers: number;
  timeElapsed: number;
  className?: string;
}

export function QuizProgress({
  currentQuestion,
  totalQuestions,
  correctAnswers,
  timeElapsed,
  className,
}: QuizProgressProps) {
  const progressPercentage = ((currentQuestion - 1) / totalQuestions) * 100;
  const accuracyPercentage = currentQuestion > 1 
    ? Math.round((correctAnswers / (currentQuestion - 1)) * 100) 
    : 0;

  return (
    <div className={cn("w-full max-w-3xl mx-auto mb-6", className)}>
      <div className="flex justify-between items-center mb-2 text-sm">
        <span className="text-muted-foreground">
          Progress: {currentQuestion - 1} / {totalQuestions} answered
        </span>
        <div className="flex items-center gap-4">
          <span className="text-muted-foreground">
            Accuracy: <span className="font-semibold text-foreground">{accuracyPercentage}%</span>
          </span>
          <span className="text-muted-foreground">
            Time: <span className="font-semibold text-foreground">{formatTime(timeElapsed)}</span>
          </span>
        </div>
      </div>
      <Progress 
        value={progressPercentage} 
        className="h-2"
        indicatorClassName={cn(
          accuracyPercentage >= 70 ? "bg-green-500" :
          accuracyPercentage >= 50 ? "bg-yellow-500" :
          "bg-red-500"
        )}
      />
    </div>
  );
}
