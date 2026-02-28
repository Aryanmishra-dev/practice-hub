# 🎯 MCQ Practice Platform - Master Development Prompt

## 📋 Project Overview

**Project Type:** Curated MCQ Practice Platform with Analytics  
**Target:** Exam preparation and skill mastery  
**Approach:** Admin-curated questions (NO PDF processing)  
**Architecture Grade:** Production-ready, scalable, secure

---

## 🏗️ Core Technology Stack

### Frontend
- **Framework:** Next.js 14+ (App Router)
- **UI Library:** React 18+
- **Styling:** Tailwind CSS
- **Component Library:** Radix UI / Headless UI
- **State Management:** React Query (TanStack Query)
- **Form Handling:** React Hook Form + Zod validation

### Backend
- **API Framework:** FastAPI (Python 3.11+)
- **Authentication:** Supabase Auth (OAuth + Email)
- **Database:** PostgreSQL (via Supabase)
- **Validation:** Pydantic models
- **API Documentation:** Auto-generated OpenAPI/Swagger

### Infrastructure
- **Hosting:** Vercel (Frontend) + Railway/Render (Backend)
- **Database:** Supabase (managed PostgreSQL)
- **CDN:** Built-in with Vercel
- **Monitoring:** Sentry (error tracking)

---

## 🎯 MCP (Model Context Protocol) Rules

### Rule 1: Single Responsibility Components
- Each component/module handles ONE specific concern
- No mixed business logic with presentation
- Clear separation: UI → Logic → Data

### Rule 2: Data Flow Integrity
```
User Action → API Call → Backend Validation → Database → Response → UI Update
```
- No direct database access from frontend
- All mutations through authenticated API endpoints
- Optimistic UI updates with rollback capability

### Rule 3: State Management Hierarchy
1. **Server State** (React Query): API data, questions, user stats
2. **URL State** (Next.js Router): Current quiz, filters, pagination
3. **Local State** (useState): Quiz session, current answer, timer
4. **Form State** (React Hook Form): Admin uploads, user settings

### Rule 4: Security-First Design
- Row Level Security (RLS) on all database tables
- JWT-based authentication on every protected endpoint
- Role-based access control (user vs admin)
- Input sanitization on both client and server
- Rate limiting on all public endpoints

### Rule 5: Error Handling Protocol
```
Try → Catch → Log → User Feedback → Graceful Degradation
```
- Never expose internal errors to users
- Always provide actionable error messages
- Log all errors with context (user_id, endpoint, timestamp)
- Implement retry logic for transient failures

### Rule 6: Performance Standards
- **First Contentful Paint:** < 1.5s
- **Time to Interactive:** < 3s
- **API Response Time:** < 200ms (p95)
- **Database Queries:** Indexed, < 50ms
- **Image Optimization:** Next.js Image, lazy loading

### Rule 7: Code Quality Gates
- TypeScript strict mode enabled
- ESLint + Prettier configured
- 80%+ test coverage on critical paths
- No unused dependencies
- Lighthouse score > 90

---

## 📐 Database Schema (PostgreSQL)

### Core Tables

```sql
-- Categories Table
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50),
    display_order INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Questions Table
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    difficulty VARCHAR(20) NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard', 'expert')),
    question_text TEXT NOT NULL,
    options JSONB NOT NULL, -- Array of {id, text}
    correct_option VARCHAR(10) NOT NULL,
    explanation TEXT,
    tags TEXT[], -- For additional filtering
    is_active BOOLEAN DEFAULT true,
    version INTEGER DEFAULT 1,
    created_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_options CHECK (jsonb_array_length(options) >= 2),
    CONSTRAINT valid_difficulty CHECK (difficulty IN ('easy', 'medium', 'hard', 'expert'))
);

-- User Answers Table
CREATE TABLE user_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    selected_option VARCHAR(10) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INTEGER, -- Time to answer
    answered_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Prevent duplicate answers in same session
    UNIQUE(user_id, question_id, answered_at)
);

-- User Statistics (Aggregated)
CREATE TABLE user_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    difficulty VARCHAR(20),
    total_attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,
    accuracy DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE 
            WHEN total_attempts > 0 THEN (correct_attempts::DECIMAL / total_attempts * 100)
            ELSE 0 
        END
    ) STORED,
    avg_time_seconds DECIMAL(8,2),
    last_practiced_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Unique constraint per user/category/difficulty
    UNIQUE(user_id, category_id, difficulty)
);

-- Indexes for Performance
CREATE INDEX idx_questions_category ON questions(category_id) WHERE is_active = true;
CREATE INDEX idx_questions_difficulty ON questions(difficulty) WHERE is_active = true;
CREATE INDEX idx_user_answers_user ON user_answers(user_id);
CREATE INDEX idx_user_answers_question ON user_answers(question_id);
CREATE INDEX idx_user_stats_user ON user_stats(user_id);
CREATE INDEX idx_user_stats_category ON user_stats(category_id);
```

---

## 🔐 Row Level Security (RLS) Policies

```sql
-- Enable RLS
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;

-- Categories: Public read, admin write
CREATE POLICY "Anyone can view active categories" 
    ON categories FOR SELECT 
    USING (is_active = true);

CREATE POLICY "Admins can manage categories" 
    ON categories FOR ALL 
    USING (auth.jwt() ->> 'role' = 'admin');

-- Questions: Public read (active only), admin write
CREATE POLICY "Anyone can view active questions" 
    ON questions FOR SELECT 
    USING (is_active = true);

CREATE POLICY "Admins can manage questions" 
    ON questions FOR ALL 
    USING (auth.jwt() ->> 'role' = 'admin');

-- User Answers: Users can only access their own
CREATE POLICY "Users can view own answers" 
    ON user_answers FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own answers" 
    ON user_answers FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- User Stats: Users can view own stats
CREATE POLICY "Users can view own stats" 
    ON user_stats FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "System can update stats" 
    ON user_stats FOR ALL 
    USING (auth.jwt() ->> 'role' IN ('admin', 'service'));
```

---

## 🚀 Phase-Wise Development Roadmap

## **PHASE 1: Foundation & Authentication** (Week 1)

### Objectives
- Set up development environment
- Implement authentication flow
- Create base project structure

### Tasks

#### 1.1 Project Initialization
```bash
# Frontend setup
- Initialize Next.js project with TypeScript
- Configure Tailwind CSS + Radix UI
- Set up ESLint + Prettier
- Configure absolute imports (@/components, @/lib)

# Backend setup
- Initialize FastAPI project
- Set up virtual environment
- Configure Pydantic settings
- Set up CORS middleware
```

#### 1.2 Supabase Configuration
```bash
- Create Supabase project
- Configure OAuth providers (Google, GitHub)
- Set up email authentication
- Create auth.users metadata schema
- Configure JWT secret in environment
```

#### 1.3 Authentication Implementation
**Frontend:**
- Create auth context provider
- Build login/signup pages
- Implement OAuth buttons
- Add protected route middleware
- Create session persistence logic

**Backend:**
- Implement JWT verification middleware
- Create user role checker decorator
- Build auth utilities (get_current_user)
- Set up refresh token rotation

#### 1.4 Base UI Components
```
- Layout component (Navbar, Sidebar, Footer)
- Button variants (primary, secondary, ghost)
- Input components with validation states
- Loading states and skeletons
- Toast notification system
- Modal/Dialog components
```

### Deliverables
- ✅ Working authentication (Email + OAuth)
- ✅ Protected routes on frontend
- ✅ JWT validation on backend
- ✅ Base component library
- ✅ Development environment configured

---

## **PHASE 2: Core Database & Admin Upload** (Week 2)

### Objectives
- Implement database schema
- Build admin question upload system
- Create data validation pipeline

### Tasks

#### 2.1 Database Setup
```sql
- Create all tables (categories, questions, user_answers, user_stats)
- Implement RLS policies
- Add indexes for performance
- Set up database triggers for updated_at
- Create database functions for stats calculation
```

#### 2.2 Admin Upload API
**Backend Endpoints:**
```python
POST /admin/categories/bulk          # Upload categories
POST /admin/questions/bulk           # Upload questions
GET  /admin/questions                # List all questions
PUT  /admin/questions/{id}           # Update single question
DELETE /admin/questions/{id}         # Soft delete question
GET  /admin/stats                    # System statistics
```

**Validation Logic:**
```python
- Validate JSON schema (Pydantic models)
- Check required fields (question_text, options, correct_option)
- Validate option format and correct_option reference
- Ensure difficulty is valid enum value
- Check for duplicate questions (similarity check)
- Validate category existence
```

#### 2.3 JSON Schema Definition
```json
{
  "categories": [
    {
      "name": "European Parliament Official",
      "description": "Questions about EPO exam",
      "icon": "file-text",
      "display_order": 1
    }
  ],
  "questions": [
    {
      "category_name": "European Parliament Official",
      "difficulty": "easy",
      "question_text": "What is the primary function of the European Parliament?",
      "options": [
        {"id": "A", "text": "Legislative body"},
        {"id": "B", "text": "Executive body"},
        {"id": "C", "text": "Judicial body"},
        {"id": "D", "text": "Advisory body"}
      ],
      "correct_option": "A",
      "explanation": "The European Parliament is primarily a legislative institution...",
      "tags": ["parliament", "basics"]
    }
  ]
}
```

#### 2.4 Admin Dashboard UI
```
- Admin login page (role-based access)
- File upload interface with drag & drop
- JSON preview and validation feedback
- Bulk operation progress indicator
- Question management table (list, edit, delete)
- Category management interface
```

### Deliverables
- ✅ Complete database schema deployed
- ✅ Admin bulk upload working
- ✅ JSON validation pipeline
- ✅ Admin dashboard UI
- ✅ Sample data loaded (100+ questions)

---

## **PHASE 3: Question Delivery & Quiz Engine** (Week 3)

### Objectives
- Build question retrieval system
- Implement quiz session logic
- Create user answer submission flow

### Tasks

#### 3.1 Question API Endpoints
```python
GET /api/categories
# Returns: List of active categories with question counts

GET /api/categories/{id}/questions?difficulty=easy&limit=10&exclude_answered=true
# Returns: Random questions matching criteria
# Params:
#   - difficulty: easy|medium|hard|expert (optional)
#   - limit: number of questions (default: 10)
#   - exclude_answered: bool (default: false)

GET /api/questions/{id}
# Returns: Single question details (for review mode)
```

#### 3.2 Quiz Session Management
**Frontend State Machine:**
```
States: IDLE → LOADING → ACTIVE → REVIEWING → COMPLETED

Actions:
- START_QUIZ (category, difficulty, count)
- SUBMIT_ANSWER (question_id, selected_option)
- NEXT_QUESTION
- REVIEW_QUIZ
- END_QUIZ
```

**Session Storage:**
```typescript
interface QuizSession {
  id: string;
  category_id: string;
  difficulty: string;
  questions: Question[];
  currentIndex: number;
  answers: Map<string, UserAnswer>;
  startedAt: Date;
  timeElapsed: number;
}
```

#### 3.3 Answer Submission API
```python
POST /api/quiz/submit
Request Body:
{
  "question_id": "uuid",
  "selected_option": "A",
  "time_taken_seconds": 45
}

Response:
{
  "is_correct": true,
  "correct_option": "A",
  "explanation": "...",
  "user_stats_updated": true
}
```

#### 3.4 Quiz UI Components
```
Components to build:
- CategorySelector (grid/list view)
- DifficultySelector (tabs with descriptions)
- QuestionCard (question text, options, timer)
- OptionButton (A/B/C/D with selection states)
- QuizProgress (X/Y questions, progress bar)
- AnswerFeedback (correct/incorrect with explanation)
- QuizSummary (score, time, weak areas)
- ReviewMode (all questions with answers)
```

#### 3.5 Timer & Session Tracking
```typescript
Features:
- Per-question timer (optional setting)
- Total quiz duration tracking
- Auto-submit on timer expiry (optional)
- Pause/resume capability
- Session recovery on page reload
```

### Deliverables
- ✅ Question fetching with filters working
- ✅ Complete quiz flow (start → answer → review → complete)
- ✅ Answer validation and immediate feedback
- ✅ Session state persistence
- ✅ Timer functionality

---

## **PHASE 4: Analytics & Progress Tracking** (Week 4)

### Objectives
- Implement comprehensive analytics
- Build user progress dashboard
- Create performance insights

### Tasks

#### 4.1 Analytics API Endpoints
```python
GET /api/user/progress
# Returns: Overall user statistics across all categories

GET /api/user/analytics/{category_id}
# Returns: Detailed performance for specific category

GET /api/user/history?limit=20&offset=0
# Returns: Recent quiz attempts with scores

GET /api/user/insights
# Returns: AI-generated insights (weak areas, recommendations)
```

#### 4.2 Statistics Calculation
**Metrics to Track:**
```python
Per Category:
- Total attempts
- Correct attempts
- Accuracy percentage
- Average time per question
- Difficulty distribution (easy/medium/hard breakdown)
- Last practiced date

Overall:
- Total questions answered
- Overall accuracy
- Favorite categories (most practiced)
- Improvement trend (last 7/30 days)
- Current streak
```

#### 4.3 Database Functions
```sql
-- Function to update user stats (called via trigger)
CREATE OR REPLACE FUNCTION update_user_stats()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_stats (
        user_id, category_id, difficulty,
        total_attempts, correct_attempts
    )
    VALUES (
        NEW.user_id,
        (SELECT category_id FROM questions WHERE id = NEW.question_id),
        (SELECT difficulty FROM questions WHERE id = NEW.question_id),
        1,
        CASE WHEN NEW.is_correct THEN 1 ELSE 0 END
    )
    ON CONFLICT (user_id, category_id, difficulty)
    DO UPDATE SET
        total_attempts = user_stats.total_attempts + 1,
        correct_attempts = user_stats.correct_attempts + CASE WHEN NEW.is_correct THEN 1 ELSE 0 END,
        last_practiced_at = NOW(),
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_user_stats
AFTER INSERT ON user_answers
FOR EACH ROW
EXECUTE FUNCTION update_user_stats();
```

#### 4.4 Progress Dashboard UI
```
Visualizations:
- Accuracy chart (line graph over time)
- Category performance radar chart
- Difficulty distribution pie chart
- Recent activity timeline
- Achievements/badges section
- Recommended next practice areas

Components:
- StatCard (accuracy, questions answered, streak)
- PerformanceChart (Chart.js or Recharts)
- CategoryBreakdown (table with drill-down)
- WeakAreasList (actionable recommendations)
- StreakTracker (calendar heatmap)
```

#### 4.5 Recommendation Engine
```python
Algorithm:
1. Identify categories with < 70% accuracy
2. Find difficulty levels with declining trends
3. Suggest practicing weak areas
4. Recommend mixed difficulty for balanced practice

Example Output:
{
  "recommended_category": "European Parliament Official",
  "recommended_difficulty": "medium",
  "reason": "Your accuracy dropped 15% in medium-level EPO questions",
  "estimated_improvement": "Practice 20 questions to regain proficiency"
}
```

### Deliverables
- ✅ Complete analytics API
- ✅ Real-time stats updates via triggers
- ✅ Progress dashboard with charts
- ✅ Personalized recommendations
- ✅ Performance insights

---

## **PHASE 5: Polish, Optimization & Launch Prep** (Week 5)

### Objectives
- Performance optimization
- Security hardening
- User experience refinement
- Production deployment

### Tasks

#### 5.1 Performance Optimization
```
Frontend:
- Implement code splitting (dynamic imports)
- Add React Query caching strategy
- Optimize images (Next.js Image)
- Lazy load non-critical components
- Implement virtual scrolling for long lists
- Add service worker for offline support

Backend:
- Add Redis caching for frequently accessed data
- Optimize SQL queries (EXPLAIN ANALYZE)
- Implement database connection pooling
- Add response compression (gzip)
- Set up CDN for static assets
```

#### 5.2 Security Hardening
```
Checklist:
- [ ] Enable Supabase RLS on all tables
- [ ] Implement rate limiting (10 req/min per user)
- [ ] Add CSRF protection
- [ ] Sanitize all user inputs
- [ ] Set security headers (CSP, HSTS, X-Frame-Options)
- [ ] Enable HTTPS only
- [ ] Implement API key rotation
- [ ] Add honeypot fields in forms
- [ ] Set up DDoS protection (Cloudflare)
- [ ] Configure CORS properly
```

#### 5.3 Error Handling & Monitoring
```python
Backend:
- Integrate Sentry for error tracking
- Add structured logging (JSON format)
- Implement health check endpoint (/health)
- Create custom error pages (404, 500)
- Add request ID tracing

Frontend:
- Global error boundary component
- Network error retry logic
- Graceful degradation for offline mode
- User-friendly error messages
- Error reporting to Sentry
```

#### 5.4 Testing Strategy
```
Unit Tests (80% coverage):
- API endpoint tests (pytest)
- Database function tests
- Utility function tests
- React component tests (Jest + Testing Library)

Integration Tests:
- Full quiz flow test
- Authentication flow test
- Admin upload workflow test

E2E Tests (Playwright/Cypress):
- User registration → quiz → results flow
- Admin login → upload questions flow
- Mobile responsiveness tests
```

#### 5.5 Documentation
```
Create:
- README.md (setup instructions)
- API documentation (auto-generated from FastAPI)
- Admin guide (how to upload questions)
- User guide (how to use the platform)
- Database schema diagram
- Architecture decision records (ADR)
- Deployment guide
```

#### 5.6 Production Deployment
```
Steps:
1. Set up production Supabase instance
2. Configure environment variables
3. Deploy backend to Railway/Render
4. Deploy frontend to Vercel
5. Configure custom domain
6. Set up SSL certificates
7. Configure monitoring alerts
8. Create database backups schedule
9. Set up CI/CD pipeline (GitHub Actions)
10. Load initial question bank
```

### Deliverables
- ✅ Lighthouse score > 90
- ✅ 80%+ test coverage
- ✅ All security checks passed
- ✅ Complete documentation
- ✅ Production deployment live
- ✅ Monitoring & alerts configured

---

## 🎨 User Experience Guidelines

### Design Principles
1. **Clarity over Complexity:** Every UI element has a clear purpose
2. **Immediate Feedback:** Users always know the result of their actions
3. **Progressive Disclosure:** Show basics first, details on demand
4. **Consistent Patterns:** Same actions work the same way everywhere
5. **Accessible by Default:** WCAG 2.1 AA compliance

### Key UX Flows

#### Quiz Taking Flow
```
1. Select Category → 2. Choose Difficulty → 3. Set Preferences (count, timer)
     ↓
4. Answer Questions (with progress indicator)
     ↓
5. Immediate Feedback (correct/incorrect + explanation)
     ↓
6. Quiz Summary (score, time, weak areas)
     ↓
7. Review Mode (see all questions + answers)
     ↓
8. Recommendations (what to practice next)
```

#### First-Time User Onboarding
```
1. Welcome screen (platform overview)
2. Quick tutorial (how to take quiz)
3. Suggested starting category
4. First quiz with hints enabled
5. Achievements unlocked popup
```

### Responsive Design Breakpoints
```css
- Mobile: 320px - 640px (single column, full-width cards)
- Tablet: 641px - 1024px (two columns, side nav)
- Desktop: 1025px+ (three columns, persistent sidebar)
```

---

## 🔧 Environment Configuration

### Frontend (.env.local)
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=MCQ Practice Platform
NEXT_PUBLIC_ENVIRONMENT=development
```

### Backend (.env)
```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# API
API_HOST=0.0.0.0
API_PORT=8000
API_VERSION=v1
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Monitoring
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=INFO
```

---

## 📊 Success Metrics & KPIs

### Technical Metrics
- **Uptime:** 99.9%
- **API Response Time (p95):** < 200ms
- **Page Load Time:** < 2s
- **Error Rate:** < 0.1%
- **Database Query Time:** < 50ms

### Business Metrics
- **Daily Active Users (DAU)**
- **Questions Answered per User**
- **Average Session Duration**
- **Quiz Completion Rate**
- **User Retention (7-day, 30-day)**

### Quality Metrics
- **Question Accuracy Reporting:** % of questions flagged as incorrect
- **User Satisfaction Score:** NPS or CSAT
- **Category Coverage:** Questions per category
- **Difficulty Distribution:** Balance across easy/medium/hard/expert

---

## 🚨 Critical Rules & Constraints

### NEVER DO
❌ Allow users to modify questions  
❌ Expose admin endpoints without role verification  
❌ Store passwords in plain text  
❌ Process PDFs in production (questions are pre-curated)  
❌ Allow SQL injection (use parameterized queries)  
❌ Skip input validation on backend  
❌ Return detailed error messages to users  
❌ Deploy without environment variable validation  

### ALWAYS DO
✅ Validate on both client and server  
✅ Use prepared statements for SQL  
✅ Implement rate limiting  
✅ Log all admin actions  
✅ Use HTTPS in production  
✅ Enable RLS policies  
✅ Version your questions (for auditing)  
✅ Implement proper error boundaries  
✅ Test on multiple devices/browsers  

---

## 🔄 Post-Launch Iteration Plan

### Month 1: Stabilization
- Monitor error rates and fix critical bugs
- Gather user feedback on UX
- Optimize slow queries
- Adjust difficulty levels based on data

### Month 2: Feature Enhancements
- Add timed quiz mode
- Implement achievements/badges system
- Create leaderboard (optional)
- Add social sharing for results

### Month 3: Growth Features
- Multi-language support
- Mobile app (React Native/Flutter)
- Collaborative study mode
- Export performance reports (PDF)

### Month 4+: Advanced Features
- Spaced repetition algorithm
- Personalized question selection (AI)
- Adaptive difficulty (adjusts based on performance)
- Integration with external platforms

---

## 📚 Reference Resources

### Documentation
- Next.js Docs: https://nextjs.org/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Supabase Docs: https://supabase.com/docs
- React Query: https://tanstack.com/query/latest
- Tailwind CSS: https://tailwindcss.com/docs

### Code Quality Tools
- ESLint: https://eslint.org
- Prettier: https://prettier.io
- TypeScript: https://www.typescriptlang.org
- Pytest: https://docs.pytest.org

### Deployment
- Vercel: https://vercel.com/docs
- Railway: https://docs.railway.app
- Supabase: https://supabase.com/docs/guides/platform

---

## 🎯 Final Checklist Before Launch

### Pre-Launch Verification
- [ ] All environment variables configured
- [ ] Database backups automated
- [ ] RLS policies active and tested
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] Error monitoring active (Sentry)
- [ ] Performance benchmarks met
- [ ] Mobile responsiveness verified
- [ ] Cross-browser testing completed
- [ ] Admin upload tested with real data
- [ ] User authentication flows tested
- [ ] Analytics tracking verified
- [ ] Legal pages added (Privacy, Terms)
- [ ] Domain configured with SSL
- [ ] Production database seeded

### Go-Live
- [ ] Announce to beta users
- [ ] Monitor error dashboards
- [ ] Track performance metrics
- [ ] Gather initial feedback
- [ ] Prepare hotfix deployment process

---

## 💡 Key Differentiators

What makes your platform stand out:

1. **Curated Quality:** Professional, admin-verified questions (not AI-generated slop)
2. **Deep Analytics:** Granular performance tracking per category and difficulty
3. **Smart Recommendations:** Data-driven suggestions on what to practice next
4. **Clean UX:** No clutter, focused on learning outcomes
5. **Privacy-First:** No selling user data, minimal tracking
6. **Fast & Reliable:** Optimized for speed, works offline
7. **Accessible:** WCAG compliant, works on all devices

---

## 🏆 Success Definition

Your platform succeeds when:

✅ Users complete quizzes consistently (70%+ completion rate)  
✅ Accuracy improves over time (measurable learning)  
✅ Users return regularly (30%+ weekly retention)  
✅ Platform is fast and reliable (< 0.1% error rate)  
✅ Admin can easily add content (< 5 min to upload 100 questions)  
✅ Zero security incidents  
✅ Positive user feedback (NPS > 50)  

---

## 📞 Support & Maintenance

### Daily
- Monitor error logs (Sentry)
- Check uptime status
- Review user feedback

### Weekly
- Analyze performance metrics
- Review database query performance
- Check for security updates

### Monthly
- Add new questions
- Update dependencies
- Performance optimization review
- User analytics review

---

**End of Master Prompt**

*This document serves as the complete blueprint for building an industry-grade MCQ practice platform. Follow each phase sequentially, adhering to MCP rules and quality standards throughout.*

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Maintained By:** Development Team