import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { adminStats } from "@/data/mockData";
import { Users, GraduationCap, MessageCircle, CreditCard } from "lucide-react";

export default function AdminOverview() {
  const licenseUsage = Math.round((adminStats.usedLicenses / adminStats.licenseCount) * 100);

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">School Overview</h1>
        <p className="text-muted-foreground">{adminStats.school}</p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <GraduationCap className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{adminStats.activeStudents}</p>
                <p className="text-sm text-muted-foreground">Active Students</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-accent/20">
                <Users className="h-6 w-6 text-accent" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{adminStats.activeTeachers}</p>
                <p className="text-sm text-muted-foreground">Active Teachers</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100">
                <MessageCircle className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{adminStats.queriesThisMonth.toLocaleString()}</p>
                <p className="text-sm text-muted-foreground">Queries This Month</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100">
                <CreditCard className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{adminStats.monthlyCost}</p>
                <p className="text-sm text-muted-foreground">Monthly Cost</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* License Usage */}
      <Card>
        <CardHeader>
          <CardTitle>License Usage</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">
              {adminStats.usedLicenses} of {adminStats.licenseCount} licenses used
            </span>
            <span className="text-sm font-medium">{licenseUsage}%</span>
          </div>
          <Progress value={licenseUsage} className="h-3" />
          <p className="text-xs text-muted-foreground">
            {adminStats.licenseCount - adminStats.usedLicenses} licenses remaining
          </p>
        </CardContent>
      </Card>

      {/* Quick Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Usage Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Total Queries (All Time)</span>
                <span className="font-medium">{adminStats.totalQueries.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Queries This Month</span>
                <span className="font-medium">{adminStats.queriesThisMonth.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Avg. Queries per Student</span>
                <span className="font-medium">
                  {Math.round(adminStats.queriesThisMonth / adminStats.activeStudents)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Teacher-Student Ratio</span>
                <span className="font-medium">
                  1:{Math.round(adminStats.activeStudents / adminStats.activeTeachers)}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Plan Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Current Plan</span>
                <span className="font-medium text-primary">{adminStats.plan}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">License Capacity</span>
                <span className="font-medium">{adminStats.licenseCount} students</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Monthly Cost</span>
                <span className="font-medium">{adminStats.monthlyCost}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Renewal Date</span>
                <span className="font-medium">{adminStats.renewalDate}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
