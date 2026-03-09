import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { students } from "@/data/mockData";
import { Search, AlertTriangle, TrendingUp, TrendingDown } from "lucide-react";

export default function TeacherStudents() {
  const [search, setSearch] = useState("");

  const filteredStudents = students.filter((s) =>
    s.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Students</h1>
          <p className="text-muted-foreground">Class 8A — {students.length} students</p>
        </div>
        <div className="relative w-full md:w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search students..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">High Performers</p>
            <p className="text-2xl font-bold text-green-600">
              {students.filter((s) => s.quizAvg >= 80).length}
            </p>
            <p className="text-xs text-muted-foreground mt-1">Quiz avg ≥ 80%</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">Needs Attention</p>
            <p className="text-2xl font-bold text-amber-600">
              {students.filter((s) => s.quizAvg >= 50 && s.quizAvg < 80).length}
            </p>
            <p className="text-xs text-muted-foreground mt-1">Quiz avg 50-79%</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">At Risk</p>
            <p className="text-2xl font-bold text-red-600">
              {students.filter((s) => s.quizAvg < 50).length}
            </p>
            <p className="text-xs text-muted-foreground mt-1">Quiz avg &lt; 50%</p>
          </CardContent>
        </Card>
      </div>

      {/* Students Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Students</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Student</TableHead>
                <TableHead>Grade</TableHead>
                <TableHead>Quiz Avg</TableHead>
                <TableHead>Engagement</TableHead>
                <TableHead>Queries</TableHead>
                <TableHead>Weak Areas</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredStudents.map((student) => (
                <TableRow key={student.id} className={student.riskFlag ? "bg-red-50/50" : ""}>
                  <TableCell>
                    <div className="flex items-center gap-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10 font-semibold text-primary text-sm">
                        {student.avatar}
                      </div>
                      <div>
                        <p className="font-medium">{student.name}</p>
                        <p className="text-xs text-muted-foreground">{student.lastActive}</p>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>{student.grade}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span
                        className={`font-medium ${
                          student.quizAvg >= 80
                            ? "text-green-600"
                            : student.quizAvg >= 50
                            ? "text-amber-600"
                            : "text-red-600"
                        }`}
                      >
                        {student.quizAvg}%
                      </span>
                      {student.quizAvg >= 80 ? (
                        <TrendingUp className="h-4 w-4 text-green-500" />
                      ) : student.quizAvg < 50 ? (
                        <TrendingDown className="h-4 w-4 text-red-500" />
                      ) : null}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="w-24">
                      <Progress value={student.engagement} className="h-2" />
                      <span className="text-xs text-muted-foreground">{student.engagement}%</span>
                    </div>
                  </TableCell>
                  <TableCell>{student.queriesThisWeek}</TableCell>
                  <TableCell>
                    {student.weakChapters.length > 0 ? (
                      <div className="flex flex-wrap gap-1">
                        {student.weakChapters.map((ch) => (
                          <Badge key={ch} variant="outline" className="text-xs">
                            Ch {ch}
                          </Badge>
                        ))}
                      </div>
                    ) : (
                      <span className="text-xs text-muted-foreground">None</span>
                    )}
                  </TableCell>
                  <TableCell>
                    {student.riskFlag ? (
                      <Badge variant="destructive" className="flex items-center gap-1 w-fit">
                        <AlertTriangle className="h-3 w-3" />
                        At Risk
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                        On Track
                      </Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
