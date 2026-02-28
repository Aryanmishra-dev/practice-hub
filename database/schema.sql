-- MCQ Practice Platform Database Schema
-- For Supabase PostgreSQL

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- CATEGORIES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50),
    display_order INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- QUESTIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS questions (
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

-- ============================================
-- USER ANSWERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS user_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    selected_option VARCHAR(10) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INTEGER, -- Time to answer
    answered_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Index for efficient querying
    UNIQUE(user_id, question_id, answered_at)
);

-- ============================================
-- USER STATISTICS TABLE (Aggregated)
-- ============================================
CREATE TABLE IF NOT EXISTS user_stats (
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

-- ============================================
-- QUIZ SESSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS quiz_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    difficulty VARCHAR(20),
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER DEFAULT 0,
    total_time_seconds INTEGER DEFAULT 0,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    
    -- Status can be: active, completed, abandoned
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'abandoned'))
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================
CREATE INDEX IF NOT EXISTS idx_questions_category ON questions(category_id) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_questions_category_difficulty ON questions(category_id, difficulty) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_user_answers_user ON user_answers(user_id);
CREATE INDEX IF NOT EXISTS idx_user_answers_question ON user_answers(question_id);
CREATE INDEX IF NOT EXISTS idx_user_answers_user_date ON user_answers(user_id, answered_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_stats_user ON user_stats(user_id);
CREATE INDEX IF NOT EXISTS idx_user_stats_category ON user_stats(category_id);
CREATE INDEX IF NOT EXISTS idx_quiz_sessions_user ON quiz_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_quiz_sessions_status ON quiz_sessions(status);

-- ============================================
-- TRIGGERS FOR AUTOMATIC TIMESTAMPS
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for categories
CREATE TRIGGER trigger_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for questions
CREATE TRIGGER trigger_questions_updated_at
    BEFORE UPDATE ON questions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for user_stats
CREATE TRIGGER trigger_user_stats_updated_at
    BEFORE UPDATE ON user_stats
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- FUNCTION TO UPDATE USER STATS
-- ============================================
CREATE OR REPLACE FUNCTION update_user_stats()
RETURNS TRIGGER AS $$
DECLARE
    v_category_id UUID;
    v_difficulty VARCHAR(20);
BEGIN
    -- Get question details
    SELECT category_id, difficulty INTO v_category_id, v_difficulty
    FROM questions WHERE id = NEW.question_id;
    
    -- Upsert into user_stats
    INSERT INTO user_stats (
        user_id, 
        category_id, 
        difficulty,
        total_attempts, 
        correct_attempts,
        last_practiced_at
    )
    VALUES (
        NEW.user_id,
        v_category_id,
        v_difficulty,
        1,
        CASE WHEN NEW.is_correct THEN 1 ELSE 0 END,
        NOW()
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

-- Trigger to update user stats on new answer
CREATE TRIGGER trigger_update_user_stats
    AFTER INSERT ON user_answers
    FOR EACH ROW
    EXECUTE FUNCTION update_user_stats();

-- ============================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================

-- Enable RLS
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_sessions ENABLE ROW LEVEL SECURITY;

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

-- Quiz Sessions: Users can only access their own
CREATE POLICY "Users can view own quiz sessions" 
    ON quiz_sessions FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own quiz sessions" 
    ON quiz_sessions FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own quiz sessions" 
    ON quiz_sessions FOR UPDATE 
    USING (auth.uid() = user_id);

-- ============================================
-- HELPER VIEWS
-- ============================================

-- View for category stats
CREATE OR REPLACE VIEW category_stats AS
SELECT 
    c.id,
    c.name,
    c.description,
    c.icon,
    c.display_order,
    c.is_active,
    COUNT(q.id) as question_count,
    COUNT(q.id) FILTER (WHERE q.difficulty = 'easy') as easy_count,
    COUNT(q.id) FILTER (WHERE q.difficulty = 'medium') as medium_count,
    COUNT(q.id) FILTER (WHERE q.difficulty = 'hard') as hard_count,
    COUNT(q.id) FILTER (WHERE q.difficulty = 'expert') as expert_count
FROM categories c
LEFT JOIN questions q ON c.id = q.category_id AND q.is_active = true
WHERE c.is_active = true
GROUP BY c.id, c.name, c.description, c.icon, c.display_order, c.is_active;

-- View for user progress
CREATE OR REPLACE VIEW user_progress AS
SELECT 
    us.user_id,
    COUNT(DISTINCT us.category_id) as categories_practiced,
    SUM(us.total_attempts) as total_questions_answered,
    ROUND(AVG(us.accuracy), 2) as overall_accuracy,
    MAX(us.last_practiced_at) as last_active
FROM user_stats us
GROUP BY us.user_id;
