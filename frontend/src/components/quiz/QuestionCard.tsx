"use client";

import * as React from "react";
import { Question, Option } from "@/types";
import { cn, indexToOptionLetter } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CheckCircle2, XCircle, Clock } from "lucide-react";

interface QuestionCardProps {
  question: Question;
  questionNumber: number;
  totalQuestions: number;
  selectedOption: string | null;
  onSelectOption: (optionId: string) => void;
  showResult?: boolean;
  isCorrect?: boolean;
  disabled?: boolean;
  timeRemaining?: number;
}

export function QuestionCard({
  question,
  questionNumber,
  totalQuestions,
  selectedOption,
  onSelectOption,
  showResult = false,
  isCorrect,
  disabled = false,
  timeRemaining,
}: QuestionCardProps) {
  const getDifficultyVariant = (difficulty: string) => {
    const variants: Record<string, "easy" | "medium" | "hard" | "expert"> = {
      easy: "easy",
      medium: "medium",
      hard: "hard",
      expert: "expert",
    };
    return variants[difficulty.toLowerCase()] || "secondary";
  };

  return (
    <Card className="w-full max-w-3xl mx-auto">
      <CardHeader>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">
              Question {questionNumber} of {totalQuestions}
            </span>
            <Badge variant={getDifficultyVariant(question.difficulty)}>
              {question.difficulty}
            </Badge>
          </div>
          {timeRemaining !== undefined && (
            <div className="flex items-center gap-1 text-sm">
              <Clock className="h-4 w-4" />
              <span className={cn(timeRemaining < 10 && "text-destructive font-bold")}>
                {Math.floor(timeRemaining / 60)}:{(timeRemaining % 60).toString().padStart(2, "0")}
              </span>
            </div>
          )}
        </div>
        <CardTitle className="text-xl leading-relaxed">
          {question.question_text}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {question.options.map((option, index) => {
            const optionLetter = indexToOptionLetter(index);
            const isSelected = selectedOption === option.id || selectedOption === optionLetter;
            const isCorrectOption = question.correct_option === option.id || question.correct_option === optionLetter;

            let optionClassName = "quiz-option";
            
            if (showResult) {
              if (isCorrectOption) {
                optionClassName += " correct";
              } else if (isSelected && !isCorrectOption) {
                optionClassName += " incorrect";
              }
            } else if (isSelected) {
              optionClassName += " selected";
            }

            if (disabled) {
              optionClassName += " disabled";
            }

            return (
              <button
                key={option.id}
                className={optionClassName}
                onClick={() => !disabled && onSelectOption(option.id)}
                disabled={disabled}
                aria-label={`Option ${optionLetter}: ${option.text}`}
                aria-pressed={isSelected}
              >
                <span className="flex h-8 w-8 items-center justify-center rounded-full border-2 border-current mr-3 font-semibold">
                  {optionLetter}
                </span>
                <span className="flex-1 text-left">{option.text}</span>
                {showResult && isCorrectOption && (
                  <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400 ml-2" />
                )}
                {showResult && isSelected && !isCorrectOption && (
                  <XCircle className="h-5 w-5 text-red-600 dark:text-red-400 ml-2" />
                )}
              </button>
            );
          })}
        </div>

        {showResult && question.explanation && (
          <div className={cn(
            "mt-6 p-4 rounded-lg",
            isCorrect
              ? "bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800"
              : "bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800"
          )}>
            <div className="flex items-start gap-2">
              {isCorrect ? (
                <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400 mt-0.5" />
              ) : (
                <XCircle className="h-5 w-5 text-red-600 dark:text-red-400 mt-0.5" />
              )}
              <div>
                <p className={cn("font-semibold", isCorrect ? "text-green-800 dark:text-green-300" : "text-red-800 dark:text-red-300")}>
                  {isCorrect ? "Correct!" : "Incorrect"}
                </p>
                <p className="text-sm text-muted-foreground mt-1">{question.explanation}</p>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
