"use client";

import * as React from "react";
import { Category } from "@/types";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FileText, BookOpen, GraduationCap, Briefcase, Globe, ChevronRight } from "lucide-react";

interface CategorySelectorProps {
  categories: Category[];
  selectedCategory: string | null;
  onSelectCategory: (categoryId: string) => void;
  loading?: boolean;
}

const iconMap: Record<string, React.ElementType> = {
  "file-text": FileText,
  "book-open": BookOpen,
  "graduation-cap": GraduationCap,
  "briefcase": Briefcase,
  "globe": Globe,
};

export function CategorySelector({
  categories,
  selectedCategory,
  onSelectCategory,
  loading = false,
}: CategorySelectorProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="animate-pulse">
            <CardHeader>
              <div className="h-6 bg-muted rounded w-3/4"></div>
              <div className="h-4 bg-muted rounded w-1/2 mt-2"></div>
            </CardHeader>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {categories.map((category) => {
        const Icon = iconMap[category.icon || "file-text"] || FileText;
        const isSelected = selectedCategory === category.id;

        return (
          <Card
            key={category.id}
            className={cn(
              "cursor-pointer transition-all hover:shadow-md hover:border-primary/50",
              isSelected && "border-primary ring-2 ring-primary/20"
            )}
            onClick={() => onSelectCategory(category.id)}
          >
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="p-2 rounded-lg bg-primary/10">
                  <Icon className="h-6 w-6 text-primary" />
                </div>
                {category.question_count !== undefined && (
                  <Badge variant="secondary">
                    {category.question_count} questions
                  </Badge>
                )}
              </div>
              <CardTitle className="text-lg mt-3">{category.name}</CardTitle>
              {category.description && (
                <CardDescription className="line-clamp-2">
                  {category.description}
                </CardDescription>
              )}
            </CardHeader>
            <CardContent className="pt-0">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">
                  {isSelected ? "Selected" : "Click to select"}
                </span>
                <ChevronRight className={cn(
                  "h-4 w-4 transition-transform",
                  isSelected && "text-primary"
                )} />
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
