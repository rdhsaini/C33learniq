import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { progressData, chapterProgress } from "@/data/mockData";
import { TrendingUp, BookOpen, Target, Award } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function StudentProgress() {
  const overallProgress = Math.round(
    chapterProgress.reduce((sum, ch) => sum + ch.progress, 0) / chapterProgress.length
  );
  const avgQuizScore = Math.round(
    chapterProgress.filter((ch) => ch.quizScore > 0).reduce((sum, ch) => sum + ch.quizScore, 0) /
      chapterProgress.filter((ch) => ch.quizScore > 0).length
  );
  const completedChapters = chapterProgress.filter((ch) => ch.progress === 100).length;

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">My Progress</h1>
        <p className="text-muted-foreground">Track your learning journey</p>
      </div>

      {/* Stats cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <TrendingUp className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{overallProgress}%</p>
                <p className="text-sm text-muted-foreground">Overall Progress</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-accent/20">
                <Target className="h-6 w-6 text-accent" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{avgQuizScore}%</p>
                <p className="text-sm text-muted-foreground">Avg. Quiz Score</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
                <BookOpen className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{completedChapters}/8</p>
                <p className="text-sm text-muted-foreground">Chapters Done</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100">
                <Award className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">18</p>
                <p className="text-sm text-muted-foreground">Questions Asked</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Progress Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Quiz Scores Over Time</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={progressData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="week" className="text-xs" />
                <YAxis domain={[0, 100]} className="text-xs" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="quizScore"
                  stroke="hsl(var(--primary))"
                  strokeWidth={2}
                  dot={{ fill: "hsl(var(--primary))" }}
                  name="Quiz Score %"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Chapter Progress */}
      <Card>
        <CardHeader>
          <CardTitle>Chapter-wise Progress</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {chapterProgress.map((ch, idx) => (
            <div key={idx} className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-foreground">{ch.chapter}</span>
                <div className="flex items-center gap-2">
                  {ch.quizScore > 0 && (
                    <Badge
                      variant="outline"
                      className={
                        ch.quizScore >= 80
                          ? "border-green-500 text-green-600"
                          : ch.quizScore >= 60
                          ? "border-amber-500 text-amber-600"
                          : "border-red-500 text-red-600"
                      }
                    >
                      Quiz: {ch.quizScore}%
                    </Badge>
                  )}
                  <span className="text-sm text-muted-foreground w-12 text-right">{ch.progress}%</span>
                </div>
              </div>
              <Progress value={ch.progress} className="h-2" />
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Weak Areas */}
      <Card>
        <CardHeader>
          <CardTitle>Areas to Improve</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {chapterProgress
              .filter((ch) => ch.quizScore > 0 && ch.quizScore < 70)
              .map((ch, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-red-50 border border-red-100">
                  <span className="text-sm font-medium text-red-800">{ch.chapter}</span>
                  <Badge variant="destructive" className="text-xs">
                    Needs Practice
                  </Badge>
                </div>
              ))}
            {chapterProgress.filter((ch) => ch.quizScore > 0 && ch.quizScore < 70).length === 0 && (
              <p className="text-sm text-muted-foreground text-center py-4">
                🎉 Great job! No weak areas identified. Keep it up!
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
