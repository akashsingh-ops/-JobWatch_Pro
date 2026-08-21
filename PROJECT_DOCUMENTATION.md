# JobWatch Pro — End-to-End System & Architecture Documentation

**Document Version:** 1.0.0  
**Project Name:** JobWatch Pro  
**Repository Type:** React 18 + TypeScript + Vite + Tailwind CSS + TanStack Query  
**Primary Functionality:** Real-time Job Telemetry, Career Opportunity Monitoring, Candidate Profile Filtering & Alert Management System.

---

## 1. Executive Summary

**JobWatch Pro** is a modern, responsive web application engineered to monitor, filter, aggregate, and alert candidates on tech job openings across multiple engineering domains (Full Stack, AI/ML, DevOps, Security, Product, Design). It provides a full-featured UI with dark/light theming, stateful caching, multi-criteria filtering, local & remote data abstraction, and administrative posting capabilities.

---

## 2. Technical Stack & Dependencies

### Frontend Core
- **Framework:** React 18 (TypeScript)
- **Bundler & Dev Server:** Vite 5.x (Port 3000, 0.0.0.0 host)
- **Styling:** Tailwind CSS 3.x, PostCSS, Custom CSS Variables for Theming (`index.css`)
- **Icons:** `lucide-react`
- **Routing:** `react-router-dom` v6
- **State Management & Caching:** `@tanstack/react-query` v5
- **Animations:** `framer-motion`
- **Component Primitives:** Radix UI (`@radix-ui/react-*` for Dialog, Dropdown, Select, Tabs, Switch, Label, Avatar, Toast)
- **Theme Provider:** `next-themes` (Light, Dark, System)
- **Form Validation:** `zod`, `react-hook-form`, `@hookform/resolvers`
- **HTTP Client:** `axios` with automated interceptors

---

## 3. Directory & File Architecture

```
├── .env.example                # Sample environment configurations
├── components.json             # UI configuration definitions
├── index.html                  # HTML entry point
├── metadata.json               # Platform capabilities & permissions metadata
├── package.json                # Dependencies, build & lint scripts
├── tailwind.config.ts          # Tailwind design tokens & themes
├── tsconfig.json               # TypeScript project configurations
├── vite.config.ts              # Vite configuration & path aliases (@/ -> /src)
└── src/
    ├── api/
    │   ├── client.ts           # Centralized Axios client with JWT request/response interceptors
    │   └── records.ts          # Telemetry & system record data service with pagination
    ├── components/
    │   ├── jobs/
    │   │   ├── JobCard.tsx     # Card component rendering job details, salary & bookmark actions
    │   │   ├── JobFilters.tsx  # Dynamic multi-parameter filter bar (Search, Category, Type, Level)
    │   │   └── JobSkeleton.tsx # Loading skeleton placeholders
    │   ├── layout/
    │   │   ├── Footer.tsx      # App footer with copyright and navigation links
    │   │   ├── Layout.tsx      # Main layout shell containing Navbar, Outlet, and Footer
    │   │   └── Navbar.tsx      # Responsive header with brand, navigation links, and theme toggle
    │   ├── theme/
    │   │   ├── ThemeProvider.tsx # Wrapper around next-themes provider
    │   │   └── ThemeToggle.tsx   # Light/Dark/System theme switcher dropdown
    │   └── ui/                 # Reusable UI component library (Button, Card, Input, etc.)
    ├── context/
    │   └── AuthContext.tsx     # React Context for authentication state, login, register & mock fallback
    ├── hooks/
    │   ├── use-toast.ts        # Toast notification state hook
    │   └── useJobs.ts          # TanStack Query hooks for querying, mutating, filtering, and saving jobs
    ├── pages/
    │   ├── Activity.tsx        # Candidate telemetry dashboard with analytics metrics & logs
    │   ├── AdminDashboard.tsx  # Admin & employer console to create and delete listings
    │   ├── Dashboard.tsx       # Main exploratory jobs board with filtering and hero banner
    │   ├── Help.tsx            # Documentation and support FAQ page
    │   ├── JobDetail.tsx       # Deep-dive view of an individual job role and direct apply links
    │   ├── Login.tsx           # Authentication sign-in form with Zod schema validation
    │   ├── NotFound.tsx        # 404 error fallback screen
    │   ├── Notifications.tsx   # Real-time alert feed & notification trigger toggles
    │   ├── Profile.tsx         # User resume and monitored target skills tag manager
    │   ├── Register.tsx        # Account registration with validation
    │   └── SavedJobs.tsx       # Dedicated saved/bookmarked jobs view
    ├── types/
    │   ├── auth.ts             # TypeScript interfaces for User, AuthContextType
    │   ├── jobs.ts             # TypeScript interfaces for Job, JobFilters, JobsResponse
    │   ├── records.ts          # TypeScript interfaces for Record, RecordFilters, RecordsResponse
    │   └── index.ts            # Centralized type exports
    ├── App.tsx                 # Root Router, QueryClientProvider, ThemeProvider, and Route definitions
    ├── index.css               # Base Tailwind CSS rules, CSS variables, and utility classes
    └── main.tsx                # React DOM root mounting entry point
```

---

## 4. End-to-End Application Workflows

### 4.1. Navigation & Routing Structure
The application employs `react-router-dom` with a layout wrapper:
- `/dashboard` — Main job search and telemetry board
- `/jobs/:id` — Detailed job description and apply actions
- `/saved` — User bookmarked positions
- `/notifications` — Alert feed and preference configuration
- `/activity` — Telemetry activity metrics, application tracking, and logs
- `/profile` — User profile headline and monitored skills
- `/settings` — Notification preferences and cache controls
- `/help` — Documentation and FAQs
- `/admin` — Employer/Admin job creation and deletion portal
- `/login` & `/register` — Authentication views

### 4.2. State Management & Data Flow
1. **Query Layer (`@tanstack/react-query`)**:
   - `useJobs(filters)`: Executes dynamic filtering across categories, job types, experience levels, and full-text keyword searches with pagination.
   - `useJob(jobId)`: Retrieves single job metadata.
   - `useSavedJobs()`: Queries only bookmarked items.
   - Mutations (`useCreateJob`, `useDeleteJob`, `useSaveJob`, `useUnsaveJob`): Automatically invalidate corresponding query keys (`['jobs']`, `['savedJobs']`, `['job']`) to trigger immediate UI re-renders without full page reloads.

2. **Persistence Strategy**:
   - Stores job state in browser `localStorage` under `jobwatch_jobs`.
   - Seeded with comprehensive industry-standard mock roles.
   - Any updates (adding a new role in Admin, toggling bookmarks, deleting roles) persist between browser sessions.

3. **HTTP Client & API Layer (`/src/api/client.ts`)**:
   - Base URL configurable via `VITE_API_URL` (defaults to `/api`).
   - Request Interceptor: Automatically attaches Bearer tokens from `localStorage.getItem('token')`.
   - Response Interceptor: Catches `401 Unauthorized` errors and clears stale session keys.

---

## 5. Security & Architectural Best Practices

- **Separation of Concerns:** Split cleanly between presentation components (`/components`), domain hooks (`/hooks`), API clients (`/api`), and global contexts (`/context`).
- **Accessibility & Contrast:** Fully compatible with WCAG standards across both light and dark themes using semantic HTML and Radix UI headless components.
- **Graceful Error Handling:** Comprehensive loading skeleton fallbacks and empty-state handling across all pages.
- **Zero Hardcoded Secrets:** Environment variable access conforms to client-side standards (`import.meta.env`).

---

## 6. How to Run, Test & Build

```bash
# 1. Install dependencies
npm install

# 2. Run local development server
npm run dev

# 3. Lint codebase
npm run lint

# 4. Production build
npm run build
```

---
*End of Documentation.*
