import { Outlet, Navigate, useLocation } from "react-router-dom";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { useAuth } from "@/contexts/AuthContext";
import { Badge } from "@/components/ui/badge";

export default function DashboardLayout() {
  const { user } = useAuth();
  const location = useLocation();

  // If no user, redirect to login
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Role-based route protection
  const path = location.pathname;
  if (path.startsWith("/student") && user.role !== "student") {
    return <Navigate to={`/${user.role === "teacher" ? "teacher/dashboard" : "admin/overview"}`} replace />;
  }
  if (path.startsWith("/teacher") && user.role !== "teacher") {
    return <Navigate to={`/${user.role === "student" ? "student/chat" : "admin/overview"}`} replace />;
  }
  if (path.startsWith("/admin") && user.role !== "admin") {
    return <Navigate to={`/${user.role === "student" ? "student/chat" : "teacher/dashboard"}`} replace />;
  }

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <AppSidebar />

        <div className="flex-1 flex flex-col">
          {/* Header */}
          <header className="sticky top-0 z-40 h-14 flex items-center justify-between border-b bg-background/95 backdrop-blur px-4">
            <div className="flex items-center gap-2">
              <SidebarTrigger className="h-8 w-8" />
              <span className="text-sm font-medium text-muted-foreground">
                {user.school}
              </span>
            </div>
            <div className="flex items-center gap-3">
              <Badge
                variant="outline"
                className={
                  user.role === "student"
                    ? "border-accent text-accent"
                    : user.role === "teacher"
                    ? "border-primary text-primary"
                    : "border-muted-foreground text-muted-foreground"
                }
              >
                {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
              </Badge>
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground font-semibold text-xs">
                {user.avatar}
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="flex-1 overflow-auto bg-muted/30">
            <Outlet />
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}
