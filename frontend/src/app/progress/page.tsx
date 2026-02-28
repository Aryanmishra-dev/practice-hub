"use client";

import * as React from "react";
import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { 
  BarChart3, 
  Target, 
  Clock, 
  TrendingUp,
  Trophy,
  BookOpen,
  ArrowRight,
} from "lucide-react";
import { Difficulty } from "@/types";

export default function ProgressPage() {
  return (
    <div className="container py-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Your Progress</h1>
          <p className="text-muted-foreground">
            Track your learning journey and identify areas for improvement
          </p>
        </div>

        {/* Info Card */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="text-center py-8">
              <Trophy className="h-16 w-16 mx-auto mb-4 text-primary opacity-80" />
              <h2 className="text-2xl font-bold mb-2">Progress Tracking</h2>
              <p className="text-muted-foreground max-w-md mx-auto mb-6">
                Your quiz results are shown at the end of each quiz session. 
                Start a quiz to practice and see your performance!
              </p>
              <Link href="/quiz">
                <Button size="lg" className="gap-2">
                  Start a Quiz
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Difficulty Guide */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Difficulty Levels Guide
            </CardTitle>
            <CardDescription>
              Understand the difficulty levels to plan your practice
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {(["easy", "medium", "hard", "expert"] as Difficulty[]).map((difficulty) => {
              const descriptions: Record<Difficulty, string> = {
                easy: "Foundational concepts and basic recall questions. Great for getting started.",
                medium: "Intermediate questions requiring understanding of concepts and their applications.",
                hard: "Advanced questions that test deeper knowledge and problem-solving skills.",
                expert: "The most challenging questions covering edge cases and expert-level scenarios.",
              };
              return (
                <div key={difficulty} className="flex items-start gap-4 p-4 rounded-lg border">
                  <Badge variant={difficulty as any} className="mt-0.5 capitalize">
                    {difficulty}
                  </Badge>
                  <p className="text-sm text-muted-foreground">{descriptions[difficulty]}</p>
                </div>
              );
            })}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
