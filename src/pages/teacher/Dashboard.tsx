import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { chapters, heatmapData, students } from "@/data/mockData";
import { AlertTriangle, Users, MessageCircle, TrendingUp } from "lucide-react";

export default function TeacherDashboard() {
  const flaggedStudents = students.filter((s) => s.riskFlag);
  const totalQueries = students.reduce((sum, s) => sum + s.queriesThisWeek, 0);
  const avgEngagement = Math.round(students.reduce((sum, s) => sum + s.engagement, 0) / students.length);

  // Get confusion level color
  const getHeatColor = (value: number) => {
    if (value >= 60) return "bg-red-500";
    if (value >= 40) return "bg-amber-400";
    if (value >= 25) return "bg-yellow-300";
    return "bg-green-400";
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Teacher Dashboard</h1>
        <p className="text-muted-foreground">Class 8A — NCERT Science</p>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <Users className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{students.length}</p>
                <p className="text-sm text-muted-foreground">Active Students</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-accent/20">
                <MessageCircle className="h-6 w-6 text-accent" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{totalQueries}</p>
                <p className="text-sm text-muted-foreground">Queries This Week</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
                <TrendingUp className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{avgEngagement}%</p>
                <p className="text-sm text-muted-foreground">Avg. Engagement</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-red-100">
                <AlertTriangle className="h-6 w-6 text-red-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{flaggedStudents.length}</p>
                <p className="text-sm text-muted-foreground">At-Risk Students</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Heatmap */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Concept Confusion Heatmap</span>
            <div className="flex items-center gap-2 text-xs font-normal">
              <span className="flex items-center gap-1">
                <span className="h-3 w-3 rounded bg-green-400" /> Low
              </span>
              <span className="flex items-center gap-1">
                <span className="h-3 w-3 rounded bg-yellow-300" /> Medium
              </span>
              <span className="flex items-center gap-1">
                <span className="h-3 w-3 rounded bg-amber-400" /> High
              </span>
              <span className="flex items-center gap-1">
                <span className="h-3 w-3 rounded bg-red-500" /> Critical
              </span>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground mb-4">
            Click on a chapter to see which students are struggling
          </p>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {chapters.map((ch) => {
              const confusion = heatmapData[ch.id] || 0;
              return (
                <button
                  key={ch.id}
                  className={`p-4 rounded-lg text-left transition-all hover:scale-105 ${getHeatColor(confusion)}`}
                >
                  <p className="font-semibold text-white text-sm">Ch {ch.id}</p>
                  <p className="text-xs text-white/80 truncate">{ch.name}</p>
                  <p className="mt-2 text-lg font-bold text-white">{confusion}%</p>
                </button>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* At-Risk Students */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-red-500" />
            At-Risk Students
          </CardTitle>
        </CardHeader>
        <CardContent>
          {flaggedStudents.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-6">
              ✅ No at-risk students detected. All students are progressing well!
            </p>
          ) : (
            <div className="space-y-3">
              {flaggedStudents.map((student) => (
                <div
                  key={student.id}
                  className="flex items-center justify-between p-4 rounded-lg border border-red-200 bg-red-50"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-red-100 font-semibold text-red-700">
                      {student.avatar}
                    </div>
                    <div>
                      <p className="font-medium text-foreground">{student.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {student.queriesThisWeek} queries this week • Last active: {student.lastActive}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <Badge variant="destructive" className="text-xs">
                      Repeated Questions
                    </Badge>
                    <p className="text-xs text-muted-foreground mt-1">
                      Weak in Ch {student.weakChapters.join(", ")}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Class Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-start gap-3 text-sm">
              <div className="h-2 w-2 rounded-full bg-accent mt-2" />
              <div>
                <p className="font-medium">Priya Sharma asked about photosynthesis</p>
                <p className="text-muted-foreground text-xs">2 hours ago • Chapter 1</p>
              </div>
            </div>
            <div className="flex items-start gap-3 text-sm">
              <div className="h-2 w-2 rounded-full bg-red-500 mt-2" />
              <div>
                <p className="font-medium">Karan Singh repeated question on synthetic fibres</p>
                <p className="text-muted-foreground text-xs">5 hours ago • Chapter 3 (3rd time)</p>
              </div>
            </div>
            <div className="flex items-start gap-3 text-sm">
              <div className="h-2 w-2 rounded-full bg-green-500 mt-2" />
              <div>
                <p className="font-medium">Meera Nair completed quiz with 92% score</p>
                <p className="text-muted-foreground text-xs">Yesterday • Chapter 2</p>
              </div>
            </div>
            <div className="flex items-start gap-3 text-sm">
              <div className="h-2 w-2 rounded-full bg-accent mt-2" />
              <div>
                <p className="font-medium">Arjun Mehta asked about cell structure</p>
                <p className="text-muted-foreground text-xs">Yesterday • Chapter 8</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
