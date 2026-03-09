import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { adminStats } from "@/data/mockData";
import { CreditCard, Calendar, TrendingUp, AlertCircle, Check } from "lucide-react";

export default function AdminBilling() {
  const licenseUsage = Math.round((adminStats.usedLicenses / adminStats.licenseCount) * 100);

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Billing & Licenses</h1>
        <p className="text-muted-foreground">{adminStats.school}</p>
      </div>

      {/* Current Plan */}
      <Card className="border-primary">
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle className="text-xl">{adminStats.plan}</CardTitle>
            <p className="text-sm text-muted-foreground mt-1">Your current subscription</p>
          </div>
          <Badge className="bg-primary text-primary-foreground">Active</Badge>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent/20">
                <CreditCard className="h-5 w-5 text-accent" />
              </div>
              <div>
                <p className="text-2xl font-bold">{adminStats.monthlyCost}</p>
                <p className="text-xs text-muted-foreground">per month</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                <Calendar className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-lg font-bold">{adminStats.renewalDate}</p>
                <p className="text-xs text-muted-foreground">Next renewal</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-100">
                <TrendingUp className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="text-lg font-bold">{adminStats.licenseCount}</p>
                <p className="text-xs text-muted-foreground">Total licenses</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* License Usage */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>License Usage</span>
            {licenseUsage > 90 && (
              <Badge variant="destructive" className="flex items-center gap-1">
                <AlertCircle className="h-3 w-3" />
                Near Limit
              </Badge>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">
              {adminStats.usedLicenses} of {adminStats.licenseCount} licenses used
            </span>
            <span className="font-medium">{licenseUsage}%</span>
          </div>
          <Progress value={licenseUsage} className="h-4" />
          <div className="flex items-center justify-between">
            <p className="text-sm text-muted-foreground">
              {adminStats.licenseCount - adminStats.usedLicenses} licenses available
            </p>
            <Button variant="outline" size="sm">
              Upgrade Licenses
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Plan Features */}
      <Card>
        <CardHeader>
          <CardTitle>Plan Features</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 md:grid-cols-2">
            {[
              "Up to 500 student licenses",
              "Unlimited AI queries",
              "Teacher dashboard & heatmap",
              "Class confusion analytics",
              "Admin panel & license management",
              "NCERT + custom content upload",
              "Dedicated onboarding support",
              "Fortnightly usage reports",
            ].map((feature) => (
              <div key={feature} className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-600" />
                <span className="text-sm">{feature}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Billing History */}
      <Card>
        <CardHeader>
          <CardTitle>Billing History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 rounded-lg border">
              <div>
                <p className="font-medium">February 2026</p>
                <p className="text-sm text-muted-foreground">School SaaS — Pro</p>
              </div>
              <div className="text-right">
                <p className="font-medium">{adminStats.monthlyCost}</p>
                <Badge variant="outline" className="text-green-600 border-green-200 bg-green-50">
                  Paid
                </Badge>
              </div>
            </div>
            <div className="flex items-center justify-between p-4 rounded-lg border">
              <div>
                <p className="font-medium">January 2026</p>
                <p className="text-sm text-muted-foreground">School SaaS — Pro</p>
              </div>
              <div className="text-right">
                <p className="font-medium">{adminStats.monthlyCost}</p>
                <Badge variant="outline" className="text-green-600 border-green-200 bg-green-50">
                  Paid
                </Badge>
              </div>
            </div>
            <div className="flex items-center justify-between p-4 rounded-lg border">
              <div>
                <p className="font-medium">December 2025</p>
                <p className="text-sm text-muted-foreground">School SaaS — Pro</p>
              </div>
              <div className="text-right">
                <p className="font-medium">{adminStats.monthlyCost}</p>
                <Badge variant="outline" className="text-green-600 border-green-200 bg-green-50">
                  Paid
                </Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Actions */}
      <div className="flex gap-3">
        <Button variant="outline">Download Invoice</Button>
        <Button variant="outline">Update Payment Method</Button>
        <Button className="bg-primary text-primary-foreground">Upgrade Plan</Button>
      </div>
    </div>
  );
}
