// ===================== NCERT Grade 8 Science Chapters =====================
export const chapters = [
  { id: 1, name: "Crop Production and Management", subject: "Science" },
  { id: 2, name: "Microorganisms: Friend and Foe", subject: "Science" },
  { id: 3, name: "Synthetic Fibres and Plastics", subject: "Science" },
  { id: 4, name: "Materials: Metals and Non-Metals", subject: "Science" },
  { id: 5, name: "Coal and Petroleum", subject: "Science" },
  { id: 6, name: "Combustion and Flame", subject: "Science" },
  { id: 7, name: "Conservation of Plants and Animals", subject: "Science" },
  { id: 8, name: "Cell — Structure and Functions", subject: "Science" },
  { id: 9, name: "Reproduction in Animals", subject: "Science" },
  { id: 10, name: "Reaching the Age of Adolescence", subject: "Science" },
];

// ===================== Students =====================
export const students = [
  {
    id: "s1",
    name: "Priya Sharma",
    grade: "8A",
    avatar: "PS",
    quizAvg: 84,
    engagement: 92,
    queriesThisWeek: 18,
    weakChapters: [3, 7],
    riskFlag: false,
    lastActive: "2 hours ago",
  },
  {
    id: "s2",
    name: "Arjun Mehta",
    grade: "8A",
    avatar: "AM",
    quizAvg: 56,
    engagement: 61,
    queriesThisWeek: 31,
    weakChapters: [3, 6, 7],
    riskFlag: true,
    lastActive: "1 day ago",
  },
  {
    id: "s3",
    name: "Riya Patel",
    grade: "8B",
    avatar: "RP",
    quizAvg: 78,
    engagement: 85,
    queriesThisWeek: 9,
    weakChapters: [5],
    riskFlag: false,
    lastActive: "3 hours ago",
  },
  {
    id: "s4",
    name: "Karan Singh",
    grade: "8B",
    avatar: "KS",
    quizAvg: 45,
    engagement: 42,
    queriesThisWeek: 44,
    weakChapters: [2, 3, 7, 8],
    riskFlag: true,
    lastActive: "5 days ago",
  },
  {
    id: "s5",
    name: "Meera Nair",
    grade: "8C",
    avatar: "MN",
    quizAvg: 91,
    engagement: 97,
    queriesThisWeek: 6,
    weakChapters: [],
    riskFlag: false,
    lastActive: "30 min ago",
  },
];

// ===================== Teacher Heatmap (confusion % per chapter) =====================
export const heatmapData: Record<number, number> = {
  1: 18,
  2: 35,
  3: 72, // high confusion
  4: 29,
  5: 41,
  6: 55,
  7: 68, // high confusion
  8: 33,
  9: 22,
  10: 44,
};

// ===================== Chat Mock Conversations =====================
export const mockChatHistory = [
  {
    id: "m1",
    role: "user" as const,
    content: "What is photosynthesis? Explain simply.",
    timestamp: "10:02 AM",
  },
  {
    id: "m2",
    role: "assistant" as const,
    content:
      "Photosynthesis is the process by which green plants make their own food using sunlight. Plants absorb carbon dioxide (CO₂) from the air and water (H₂O) from the soil. Using energy from sunlight, they convert these into glucose (sugar) and release oxygen as a by-product.\n\n**The equation:**\n6CO₂ + 6H₂O + Sunlight → C₆H₁₂O₆ + 6O₂\n\nThis happens inside the **chloroplasts** of plant cells, which contain a green pigment called **chlorophyll**.",
    timestamp: "10:02 AM",
    citations: [
      { chapter: 1, name: "Crop Production and Management", page: 12 },
      { chapter: 8, name: "Cell — Structure and Functions", page: 87 },
    ],
  },
  {
    id: "m3",
    role: "user" as const,
    content: "What are the two types of synthetic fibres?",
    timestamp: "10:05 AM",
  },
  {
    id: "m4",
    role: "assistant" as const,
    content:
      "Synthetic fibres are made from chemicals derived from petroleum. The two main types covered in your syllabus are:\n\n1. **Rayon** — Also called artificial silk. Made from cellulose (natural source) but processed chemically. Soft and lustrous.\n\n2. **Nylon** — The first fully synthetic fibre. Very strong, elastic, and resistant to heat. Used in ropes, parachutes, and clothing.\n\nOther examples include **Polyester** (wrinkle-free, durable) and **Acrylic** (resembles wool).",
    timestamp: "10:05 AM",
    citations: [
      { chapter: 3, name: "Synthetic Fibres and Plastics", page: 28 },
    ],
  },
];

// ===================== Quiz Questions =====================
export const quizQuestions = [
  {
    id: "q1",
    chapter: 1,
    difficulty: "easy" as const,
    question: "Which of the following is a Kharif crop?",
    options: ["Wheat", "Rice", "Mustard", "Gram"],
    correct: 1,
    explanation:
      "Rice is a Kharif crop, sown in the rainy season (June–September). Wheat, Mustard, and Gram are Rabi crops sown in winter.",
  },
  {
    id: "q2",
    chapter: 3,
    difficulty: "medium" as const,
    question: "Which synthetic fibre is also known as artificial silk?",
    options: ["Nylon", "Polyester", "Rayon", "Acrylic"],
    correct: 2,
    explanation:
      "Rayon is known as artificial silk. It is made from wood pulp (cellulose) and has a silky texture.",
  },
  {
    id: "q3",
    chapter: 7,
    difficulty: "hard" as const,
    question:
      "Which of the following is NOT a method of conservation of plants and animals?",
    options: [
      "National Parks",
      "Biosphere Reserves",
      "Afforestation",
      "Deforestation",
    ],
    correct: 3,
    explanation:
      "Deforestation (clearing forests) destroys habitats and is harmful. National Parks, Biosphere Reserves, and Afforestation (planting trees) are all conservation methods.",
  },
  {
    id: "q4",
    chapter: 8,
    difficulty: "easy" as const,
    question: "What is the powerhouse of the cell?",
    options: ["Nucleus", "Ribosome", "Mitochondria", "Chloroplast"],
    correct: 2,
    explanation:
      "Mitochondria are called the powerhouse of the cell because they produce energy (ATP) through cellular respiration.",
  },
  {
    id: "q5",
    chapter: 2,
    difficulty: "medium" as const,
    question: "Which microorganism causes malaria?",
    options: ["Bacteria", "Virus", "Fungi", "Protozoa"],
    correct: 3,
    explanation:
      "Malaria is caused by Plasmodium, a type of protozoa. It is transmitted by the female Anopheles mosquito.",
  },
];

// ===================== Student Progress Data =====================
export const progressData = [
  { week: "Week 1", quizScore: 62, chaptersRead: 2 },
  { week: "Week 2", quizScore: 68, chaptersRead: 3 },
  { week: "Week 3", quizScore: 71, chaptersRead: 2 },
  { week: "Week 4", quizScore: 78, chaptersRead: 4 },
  { week: "Week 5", quizScore: 84, chaptersRead: 3 },
  { week: "Week 6", quizScore: 88, chaptersRead: 2 },
];

export const chapterProgress = [
  { chapter: "Ch 1 – Crop Production", progress: 100, quizScore: 92 },
  { chapter: "Ch 2 – Microorganisms", progress: 100, quizScore: 78 },
  { chapter: "Ch 3 – Synthetic Fibres", progress: 75, quizScore: 64 },
  { chapter: "Ch 4 – Metals & Non-Metals", progress: 60, quizScore: 71 },
  { chapter: "Ch 5 – Coal & Petroleum", progress: 40, quizScore: 55 },
  { chapter: "Ch 6 – Combustion & Flame", progress: 20, quizScore: 0 },
  { chapter: "Ch 7 – Conservation", progress: 10, quizScore: 0 },
  { chapter: "Ch 8 – Cell Structure", progress: 0, quizScore: 0 },
];

// ===================== Admin Stats =====================
export const adminStats = {
  school: "Delhi Public School, Rohini",
  plan: "School SaaS — Pro",
  licenseCount: 300,
  usedLicenses: 247,
  activeStudents: 234,
  activeTeachers: 18,
  totalQueries: 12480,
  queriesThisMonth: 3720,
  renewalDate: "March 31, 2026",
  monthlyCost: "₹1,20,000",
};

export const adminClasses = [
  {
    id: "c1",
    name: "8A",
    students: 42,
    teacher: "Ms. Sunita Verma",
    subject: "Science",
    avgScore: 74,
  },
  {
    id: "c2",
    name: "8B",
    students: 39,
    teacher: "Mr. Rakesh Gupta",
    subject: "Science",
    avgScore: 68,
  },
  {
    id: "c3",
    name: "8C",
    students: 44,
    teacher: "Ms. Anjali Mishra",
    subject: "Science",
    avgScore: 81,
  },
  {
    id: "c4",
    name: "9A",
    students: 41,
    teacher: "Mr. Vijay Kumar",
    subject: "Science",
    avgScore: 72,
  },
  {
    id: "c5",
    name: "9B",
    students: 38,
    teacher: "Ms. Pooja Sharma",
    subject: "Science",
    avgScore: 69,
  },
  {
    id: "c6",
    name: "9C",
    students: 43,
    teacher: "Ms. Sunita Verma",
    subject: "Math",
    avgScore: 77,
  },
];

// ===================== Pricing =====================
export const pricingPlans = [
  {
    name: "Student",
    tagline: "For individual learners",
    price: "₹299",
    period: "/month",
    color: "accent",
    features: [
      "AI Tutor — unlimited queries",
      "NCERT-aligned answers with citations",
      "Adaptive quizzes — all chapters",
      "Personal progress dashboard",
      "Voice input (coming soon)",
      "Hindi + English support",
    ],
    cta: "Start Free Trial",
    popular: false,
  },
  {
    name: "School SaaS",
    tagline: "For schools & coaching institutes",
    price: "₹20,000",
    period: "/month",
    color: "primary",
    features: [
      "Everything in Student plan",
      "Up to 500 student licences",
      "Teacher dashboard + heatmap",
      "Class confusion analytics",
      "Admin panel + license management",
      "NCERT + custom content upload",
      "Dedicated onboarding support",
      "Fortnightly usage reports",
    ],
    cta: "Request Demo",
    popular: true,
  },
  {
    name: "Publisher API",
    tagline: "For EdTech publishers & platforms",
    price: "Custom",
    period: "",
    color: "secondary",
    features: [
      "White-labelled AI tutor API",
      "Custom curriculum upload",
      "Bulk student analytics",
      "Fine-tuned subject models",
      "SLA + dedicated support",
      "Revenue sharing available",
    ],
    cta: "Contact Sales",
    popular: false,
  },
];

// ===================== Auth (mock role state) =====================
export type UserRole = "student" | "teacher" | "admin";
export interface MockUser {
  name: string;
  role: UserRole;
  school: string;
  grade?: string;
  avatar: string;
}

export const mockUsers: Record<UserRole, MockUser> = {
  student: {
    name: "Priya Sharma",
    role: "student",
    school: "DPS Rohini",
    grade: "8A",
    avatar: "PS",
  },
  teacher: {
    name: "Ms. Sunita Verma",
    role: "teacher",
    school: "DPS Rohini",
    avatar: "SV",
  },
  admin: {
    name: "Rajesh Khanna",
    role: "admin",
    school: "DPS Rohini",
    avatar: "RK",
  },
};
