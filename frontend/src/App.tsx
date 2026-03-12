import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import Landing from "./pages/Landing";
import Pricing from "./pages/Pricing";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import DashboardLayout from "./layouts/DashboardLayout";
import StudentChat from "./pages/student/Chat";
import StudentQuiz from "./pages/student/Quiz";
import StudentProgress from "./pages/student/Progress";
import TeacherDashboard from "./pages/teacher/Dashboard";
import TeacherStudents from "./pages/teacher/Students";
import AdminOverview from "./pages/admin/Overview";
import AdminClasses from "./pages/admin/Classes";
import AdminBilling from "./pages/admin/Billing";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            {/* Public */}
            <Route path="/" element={<Landing />} />
            <Route path="/pricing" element={<Pricing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />

            {/* Student Dashboard */}
            <Route element={<DashboardLayout />}>
              <Route path="/student/chat" element={<StudentChat />} />
              <Route path="/student/quiz" element={<StudentQuiz />} />
              <Route path="/student/progress" element={<StudentProgress />} />
            </Route>

            {/* Teacher Dashboard */}
            <Route element={<DashboardLayout />}>
              <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
              <Route path="/teacher/students" element={<TeacherStudents />} />
            </Route>

            {/* Admin Dashboard */}
            <Route element={<DashboardLayout />}>
              <Route path="/admin/overview" element={<AdminOverview />} />
              <Route path="/admin/classes" element={<AdminClasses />} />
              <Route path="/admin/billing" element={<AdminBilling />} />
            </Route>

            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
