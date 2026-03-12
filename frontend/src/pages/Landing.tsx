import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  MessageCircle,
  Brain,
  BarChart3,
  GraduationCap,
  Users,
  School,
  ChevronRight,
  Zap,
  BookOpen,
  Shield,
} from "lucide-react";

const stats = [
  { value: "50%", label: "Grade 5 students can't read Grade 2 text (ASER 2023)" },
  { value: "1:40", label: "Average teacher-student ratio in govt. schools" },
  { value: "₹80K Cr", label: "Annual private tuition market in India" },
];

const features = [
  {
    icon: MessageCircle,
    title: "AI Tutor — Ask Anything",
    description:
      "Students chat in Hindi or English. LearnIQ answers with chapter citations so teachers can trust the source.",
  },
  {
    icon: Brain,
    title: "Adaptive Quiz Engine",
    description:
      "MCQs adjust difficulty in real-time. Struggling? Get easier questions. Acing it? Level up automatically.",
  },
  {
    icon: BarChart3,
    title: "Confusion Heatmap for Teachers",
    description:
      "See which chapters confuse your class most. Identify at-risk students before they fall behind.",
  },
  {
    icon: BookOpen,
    title: "NCERT-Aligned Curriculum",
    description:
      "Every answer cites the official NCERT textbook. Grounded in your syllabus, not random internet content.",
  },
];

const audiences = [
  {
    icon: GraduationCap,
    title: "Students",
    description: "24/7 personal tutor that speaks your language and cites your textbook.",
  },
  {
    icon: Users,
    title: "Teachers",
    description: "See what confuses your class. Intervene with flagged students before exams.",
  },
  {
    icon: School,
    title: "Schools",
    description: "Deploy across classrooms. Track usage, manage licenses, and measure impact.",
  },
];

export default function Landing() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <Link to="/" className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold">
              L
            </div>
            <span className="text-xl font-bold text-primary">LearnIQ</span>
          </Link>
          <nav className="hidden gap-6 md:flex">
            <Link to="/pricing" className="text-sm font-medium text-muted-foreground hover:text-foreground transition">
              Pricing
            </Link>
            <a href="#features" className="text-sm font-medium text-muted-foreground hover:text-foreground transition">
              Features
            </a>
            <a href="#who" className="text-sm font-medium text-muted-foreground hover:text-foreground transition">
              Who It's For
            </a>
          </nav>
          <div className="flex items-center gap-3">
            <Button variant="ghost" asChild>
              <Link to="/login">Log in</Link>
            </Button>
            <Button asChild className="bg-accent text-accent-foreground hover:bg-accent/90">
              <Link to="/signup">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="hero-gradient py-20 text-white md:py-28">
        <div className="container mx-auto px-4 text-center">
          <div className="mx-auto max-w-3xl">
            <h1 className="text-4xl font-bold leading-tight tracking-tight md:text-5xl lg:text-6xl">
              Every Child Deserves a <span className="text-amber-300">Great Teacher</span>
            </h1>
            <p className="mt-6 text-lg text-white/80 md:text-xl">
              LearnIQ is an AI-powered tutor that gives every student personalised help — in Hindi or
              English — while showing teachers exactly where their class struggles.
            </p>
            <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button size="lg" className="bg-accent text-accent-foreground hover:bg-accent/90" asChild>
                <Link to="/signup">
                  Start Free Trial <ChevronRight className="ml-1 h-4 w-4" />
                </Link>
              </Button>
              <Button size="lg" variant="secondary" asChild>
                <Link to="/pricing">Request School Demo</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="border-b bg-muted py-12">
        <div className="container mx-auto px-4">
          <p className="mb-8 text-center text-sm font-medium text-muted-foreground uppercase tracking-wider">
            The learning crisis in India
          </p>
          <div className="grid gap-6 md:grid-cols-3">
            {stats.map((stat) => (
              <div key={stat.value} className="text-center">
                <p className="text-3xl font-bold text-primary md:text-4xl">{stat.value}</p>
                <p className="mt-2 text-sm text-muted-foreground">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-foreground md:text-4xl">How LearnIQ Works</h2>
            <p className="mt-4 text-muted-foreground">
              Built for Indian classrooms. Aligned with NCERT. Designed for low-bandwidth.
            </p>
          </div>
          <div className="mt-14 grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <Card key={feature.title} className="card-hover border-0 shadow">
                <CardContent className="pt-6">
                  <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                    <feature.icon className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="font-semibold text-foreground">{feature.title}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Who It's For */}
      <section id="who" className="border-t bg-muted/50 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-foreground md:text-4xl">Who It's For</h2>
            <p className="mt-4 text-muted-foreground">
              Three dashboards. One platform. Personalized for each role.
            </p>
          </div>
          <div className="mt-14 grid gap-8 md:grid-cols-3">
            {audiences.map((aud) => (
              <Card key={aud.title} className="card-hover text-center">
                <CardContent className="pt-8 pb-8">
                  <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-accent/20">
                    <aud.icon className="h-7 w-7 text-accent" />
                  </div>
                  <h3 className="text-lg font-semibold text-foreground">{aud.title}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">{aud.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="hero-gradient py-16 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold md:text-4xl">Ready to Transform Learning?</h2>
          <p className="mx-auto mt-4 max-w-xl text-white/80">
            Join schools across India who are closing the learning gap with AI-powered personalised tutoring.
          </p>
          <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Button size="lg" className="bg-accent text-accent-foreground hover:bg-accent/90" asChild>
              <Link to="/signup">Start Free Trial</Link>
            </Button>
            <Button size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10" asChild>
              <Link to="/pricing">View Pricing</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-12">
        <div className="container mx-auto flex flex-col items-center justify-between gap-6 px-4 md:flex-row">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold text-sm">
              L
            </div>
            <span className="font-semibold text-primary">LearnIQ</span>
          </div>
          <div className="flex gap-6 text-sm text-muted-foreground">
            <Link to="/pricing" className="hover:text-foreground">Pricing</Link>
            <a href="#" className="hover:text-foreground">Privacy</a>
            <a href="#" className="hover:text-foreground">Terms</a>
            <a href="#" className="hover:text-foreground">Contact</a>
          </div>
          <p className="text-xs text-muted-foreground">© 2026 LearnIQ. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
