"use client";

import * as React from "react";
import { Difficulty } from "@/types";
import { cn } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Zap, Brain, Flame, Skull } from "lucide-react";

interface DifficultyOption {
  value: Difficulty | "mixed";
  label: string;
  description: string;
  icon: React.ElementType;
  color: string;
}

const difficultyOptions: DifficultyOption[] = [
  {
    value: "easy",
    label: "Easy",
    description: "Foundational concepts and basic recall",
    icon: Zap,
    color: "text-green-500 bg-green-50 border-green-200",
  },
  {
    value: "medium",
    label: "Medium",
    description: "Applied knowledge and reasoning",
    icon: Brain,
    color: "text-yellow-500 bg-yellow-50 border-yellow-200",
  },
  {
    value: "hard",
    label: "Hard",
    description: "Advanced concepts and analysis",
    icon: Flame,
    color: "text-orange-500 bg-orange-50 border-orange-200",
  },
  {
    value: "expert",
    label: "Expert",
    description: "Master-level challenges",
    icon: Skull,
    color: "text-red-500 bg-red-50 border-red-200",
  },
  {
    value: "mixed",
    label: "Mixed",
    description: "Random mix of all difficulties",
    icon: Brain,
    color: "text-purple-500 bg-purple-50 border-purple-200",
  },
];

interface DifficultySelectorProps {
  selectedDifficulty: Difficulty | "mixed" | null;
  onSelectDifficulty: (difficulty: Difficulty | "mixed") => void;
}

export function DifficultySelector({
  selectedDifficulty,
  onSelectDifficulty,
}: DifficultySelectorProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
      {difficultyOptions.map((option) => {
        const Icon = option.icon;
        const isSelected = selectedDifficulty === option.value;

        return (
          <Card
            key={option.value}
            className={cn(
              "cursor-pointer transition-all border-2",
              isSelected
                ? option.color + " ring-2 ring-offset-2"
                : "hover:border-muted-foreground/50"
            )}
            onClick={() => onSelectDifficulty(option.value)}
          >
            <CardContent className="p-4 text-center">
              <Icon className={cn("h-8 w-8 mx-auto mb-2", option.color.split(" ")[0])} />
              <p className="font-semibold">{option.label}</p>
              <p className="text-xs text-muted-foreground mt-1 hidden md:block">
                {option.description}
              </p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
