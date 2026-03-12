import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { quizQuestions, chapters } from "@/data/mockData";
import { CheckCircle, XCircle, ArrowRight, RotateCcw, Trophy, Zap } from "lucide-react";

export default function StudentQuiz() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [answers, setAnswers] = useState<(number | null)[]>([]);

  const question = quizQuestions[currentIndex];
  const progress = ((currentIndex + 1) / quizQuestions.length) * 100;

  const handleSelect = (idx: number) => {
    if (showResult) return;
    setSelectedAnswer(idx);
  };

  const handleSubmit = () => {
    if (selectedAnswer === null) return;
    setShowResult(true);
    const newAnswers = [...answers, selectedAnswer];
    setAnswers(newAnswers);
    if (selectedAnswer === question.correct) {
      setScore((s) => s + 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < quizQuestions.length - 1) {
      setCurrentIndex((i) => i + 1);
      setSelectedAnswer(null);
      setShowResult(false);
    } else {
      setQuizCompleted(true);
    }
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setSelectedAnswer(null);
    setShowResult(false);
    setScore(0);
    setQuizCompleted(false);
    setAnswers([]);
  };

  const difficultyColor = {
    easy: "bg-green-100 text-green-700 border-green-200",
    medium: "bg-amber-100 text-amber-700 border-amber-200",
    hard: "bg-red-100 text-red-700 border-red-200",
  };

  if (quizCompleted) {
    const percentage = Math.round((score / quizQuestions.length) * 100);
    return (
      <div className="p-6 max-w-2xl mx-auto">
        <Card className="text-center">
          <CardHeader>
            <div className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-accent/20">
              <Trophy className="h-10 w-10 text-accent" />
            </div>
            <CardTitle className="text-2xl">Quiz Complete!</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <p className="text-5xl font-bold text-primary">{score}/{quizQuestions.length}</p>
              <p className="text-muted-foreground mt-1">Questions Correct</p>
            </div>
            <Progress value={percentage} className="h-3" />
            <p className="text-lg">
              {percentage >= 80
                ? "🎉 Excellent! You've mastered this material!"
                : percentage >= 60
                ? "👍 Good job! Keep practicing to improve."
                : "📚 Keep studying! Review the chapters and try again."}
            </p>
          </CardContent>
          <CardFooter className="justify-center">
            <Button onClick={handleRestart} className="gap-2">
              <RotateCcw className="h-4 w-4" />
              Try Again
            </Button>
          </CardFooter>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h1 className="text-xl font-semibold text-foreground">Adaptive Quiz</h1>
          <Badge variant="outline" className="text-sm">
            {currentIndex + 1} / {quizQuestions.length}
          </Badge>
        </div>
        <Progress value={progress} className="h-2" />
      </div>

      {/* Question Card */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <Badge variant="outline" className="text-xs">
              Chapter {question.chapter}: {chapters[question.chapter - 1].name}
            </Badge>
            <Badge className={`text-xs ${difficultyColor[question.difficulty]}`}>
              <Zap className="h-3 w-3 mr-1" />
              {question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1)}
            </Badge>
          </div>
          <CardTitle className="text-lg mt-4 leading-relaxed">{question.question}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {question.options.map((option, idx) => {
            const isSelected = selectedAnswer === idx;
            const isCorrect = question.correct === idx;
            let optionClass = "border-border hover:border-primary/50 cursor-pointer";
            
            if (showResult) {
              if (isCorrect) {
                optionClass = "border-green-500 bg-green-50";
              } else if (isSelected && !isCorrect) {
                optionClass = "border-red-500 bg-red-50";
              }
            } else if (isSelected) {
              optionClass = "border-primary bg-primary/5";
            }

            return (
              <button
                key={idx}
                onClick={() => handleSelect(idx)}
                disabled={showResult}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all ${optionClass}`}
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border-2 text-sm font-medium">
                    {String.fromCharCode(65 + idx)}
                  </span>
                  <span className="text-sm">{option}</span>
                  {showResult && isCorrect && (
                    <CheckCircle className="h-5 w-5 text-green-600 ml-auto" />
                  )}
                  {showResult && isSelected && !isCorrect && (
                    <XCircle className="h-5 w-5 text-red-600 ml-auto" />
                  )}
                </div>
              </button>
            );
          })}
        </CardContent>

        {/* Explanation */}
        {showResult && (
          <CardContent className="pt-0">
            <div className="rounded-lg bg-muted p-4 mt-2">
              <p className="text-sm font-medium text-foreground mb-1">Explanation</p>
              <p className="text-sm text-muted-foreground">{question.explanation}</p>
            </div>
          </CardContent>
        )}

        <CardFooter className="justify-end gap-2">
          {!showResult ? (
            <Button onClick={handleSubmit} disabled={selectedAnswer === null} className="bg-accent text-accent-foreground hover:bg-accent/90">
              Check Answer
            </Button>
          ) : (
            <Button onClick={handleNext} className="gap-2">
              {currentIndex < quizQuestions.length - 1 ? (
                <>
                  Next Question <ArrowRight className="h-4 w-4" />
                </>
              ) : (
                "See Results"
              )}
            </Button>
          )}
        </CardFooter>
      </Card>

      {/* Score tracker */}
      <div className="mt-6 flex items-center justify-center gap-4 text-sm text-muted-foreground">
        <span className="flex items-center gap-1">
          <CheckCircle className="h-4 w-4 text-green-600" /> {score} correct
        </span>
        <span className="flex items-center gap-1">
          <XCircle className="h-4 w-4 text-red-500" /> {answers.length - score} incorrect
        </span>
      </div>
    </div>
  );
}
