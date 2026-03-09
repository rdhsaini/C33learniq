
## LearnIQ — AI-Powered Personalised Learning Platform (Frontend MVP)

A professional, multi-role SaaS web app based on the LearnIQ business canvas. Frontend-only with realistic mock data — no backend yet.

---

### Pages & Routes

**Public / Marketing**
- `/` — Landing page with hero ("Every child deserves a great teacher"), problem stats (ASER 2023 data), feature highlights, pricing tiers (₹299/student, ₹20K–50K/school), and a "Request Demo" CTA
- `/pricing` — Three-tier pricing cards: Student, School SaaS, Publisher API

**Auth**
- `/login` — Role-aware login (Student / Teacher / School Admin tabs)
- `/signup` — Registration with role selection

**Student Dashboard** (after login as Student)
- `/student/chat` — "Ask LearnIQ" — Conversational chat UI with chapter-cited answer bubbles, subject/chapter selector sidebar, voice input button (UI only), source citation badges (e.g., "Chapter 1: Crop Production")
- `/student/quiz` — "Quiz Me" — Adaptive MCQ quiz screen with difficulty indicator, answer feedback, score tracker, and progress bar per chapter
- `/student/progress` — Personal progress: chapters covered, quiz scores over time, weak areas summary card

**Teacher Dashboard** (after login as Teacher)
- `/teacher/dashboard` — Class heatmap (concept confusion map by chapter), student risk flags (asked same question 3+ times), class activity feed
- `/teacher/students` — Student list with individual progress summaries, engagement scores, flagged students highlighted

**School Admin Panel** (after login as Admin)
- `/admin/overview` — School-level stats: active students, teachers, queries this month, license usage
- `/admin/classes` — Class management table (add/edit classes and teachers)
- `/admin/billing` — License tier, renewal date, usage vs. plan limits

---

### UI & Design System

- **Color palette**: Deep navy primary (`#1B2B65`) + amber accent (`#F5A623`) — professional Indian EdTech feel
- **Typography**: Clean sans-serif, readable for students and teachers alike
- **Layout**: Collapsible sidebar navigation (role-aware menu items), top header with user avatar + role badge
- **Components**: Chat bubbles with source citation badges, chapter heatmap grid (colored cells by confusion %), progress ring charts, adaptive quiz card with animated difficulty indicator
- **Responsive**: Works on tablet (school computer labs) and desktop

---

### Mock Data

- 10 NCERT Grade 8 Science chapters as navigation items
- 5 sample student profiles with varied quiz scores and engagement
- Pre-seeded chat Q&A conversations (photosynthesis, cell division, etc.) with mock cited answers
- Teacher heatmap data showing high confusion on Chapters 3 and 7
- Realistic pricing in INR, school license usage percentages

---

### Key UX Flows

1. **Student flow**: Login → Chat with AI tutor → Get cited answer → Take adaptive quiz → View personal progress
2. **Teacher flow**: Login → See class heatmap → Click chapter cell → See which students are confused → View flagged students
3. **Admin flow**: Login → See school overview → Manage classes → Check license usage

---

### Implementation Order

1. Design system (colors, typography, CSS variables)
2. Landing page + pricing page
3. Auth pages (login/signup with role tabs)
4. Shared layout: sidebar + header with role-aware navigation
5. Student: Chat page (mock AI responses with citation UI)
6. Student: Quiz page (MCQ with adaptive difficulty UI)
7. Student: Progress page
8. Teacher: Dashboard with heatmap + risk flags
9. Teacher: Students list
10. School Admin: Overview + Classes + Billing pages
