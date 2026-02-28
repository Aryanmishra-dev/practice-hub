import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  BookOpen, 
  BarChart3, 
  Target, 
  Zap, 
  CheckCircle2, 
  ArrowRight,
  Brain,
  Trophy,
  Clock
} from "lucide-react";

export default function HomePage() {
  const features = [
    {
      icon: BookOpen,
      title: "Curated Questions",
      description: "Expert-verified questions organized by category and difficulty level.",
    },
    {
      icon: BarChart3,
      title: "Track Progress",
      description: "Detailed analytics to identify strengths and areas for improvement.",
    },
    {
      icon: Target,
      title: "Smart Practice",
      description: "Personalized recommendations based on your performance.",
    },
    {
      icon: Zap,
      title: "Instant Feedback",
      description: "Learn from detailed explanations after each question.",
    },
  ];

  const stats = [
    { value: "100+", label: "Questions" },
    { value: "4", label: "Difficulty Levels" },
    { value: "Real-time", label: "Analytics" },
    { value: "Free", label: "To Use" },
  ];

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="container py-12 md:py-24 lg:py-32">
        <div className="flex flex-col items-center text-center space-y-8">
          <Badge variant="secondary" className="px-4 py-1">
            🎯 Exam Preparation Made Easy
          </Badge>
          
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight max-w-3xl">
            Master Your Exams with{" "}
            <span className="text-primary">Smart MCQ Practice</span>
          </h1>
          
          <p className="text-xl text-muted-foreground max-w-2xl">
            Practice smarter, not harder. Our curated question bank and intelligent 
            analytics help you focus on what matters most.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <Link href="/quiz">
              <Button size="xl" className="gap-2">
                Start Practicing
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
            <Link href="/progress">
              <Button size="xl" variant="outline" className="gap-2">
                View Progress
                <BarChart3 className="h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="border-y bg-muted/50">
        <div className="container py-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <p className="text-3xl md:text-4xl font-bold text-primary">
                  {stat.value}
                </p>
                <p className="text-muted-foreground">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container py-12 md:py-24">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">
            Everything You Need to Succeed
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Our platform is designed to help you prepare efficiently with tools 
            that adapt to your learning style.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card key={index} className="border-2 hover:border-primary/50 transition-colors">
                <CardHeader>
                  <div className="p-2 rounded-lg bg-primary/10 w-fit mb-2">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>{feature.description}</CardDescription>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-muted/50 py-12 md:py-24">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">How It Works</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Three simple steps to start improving your exam scores today.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="flex items-center justify-center w-16 h-16 rounded-full bg-primary text-primary-foreground text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="font-semibold text-lg mb-2">Choose a Topic</h3>
              <p className="text-muted-foreground">
                Select from our curated categories and pick your difficulty level.
              </p>
            </div>
            
            <div className="text-center">
              <div className="flex items-center justify-center w-16 h-16 rounded-full bg-primary text-primary-foreground text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="font-semibold text-lg mb-2">Practice Questions</h3>
              <p className="text-muted-foreground">
                Answer questions and get instant feedback with detailed explanations.
              </p>
            </div>
            
            <div className="text-center">
              <div className="flex items-center justify-center w-16 h-16 rounded-full bg-primary text-primary-foreground text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="font-semibold text-lg mb-2">Track & Improve</h3>
              <p className="text-muted-foreground">
                Review your analytics and focus on areas that need improvement.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container py-12 md:py-24">
        <Card className="bg-primary text-primary-foreground">
          <CardContent className="py-12 text-center">
            <Trophy className="h-12 w-12 mx-auto mb-4" />
            <h2 className="text-3xl font-bold mb-4">
              Ready to Ace Your Exam?
            </h2>
            <p className="text-primary-foreground/80 max-w-xl mx-auto mb-6">
              Join thousands of students who have improved their scores with our 
              smart practice platform.
            </p>
            <Link href="/quiz">
              <Button size="lg" variant="secondary" className="gap-2">
                Start Your First Quiz
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
