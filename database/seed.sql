-- Seed data for MCQ Practice Platform
-- Run this after the schema has been created

-- ============================================
-- INSERT CATEGORIES
-- ============================================
INSERT INTO categories (id, name, description, icon, display_order) VALUES
    ('c1000000-0000-0000-0000-000000000001', 'ePO Server Administration', 
     'Questions about Trellix ePO server installation, configuration, sizing, and management. Covers topics from basic concepts to advanced cloud deployments.',
     'file-text', 1)
ON CONFLICT (name) DO NOTHING;

-- Note: The actual questions should be imported from the JSON files
-- using the admin API or a migration script.
-- The following is an example of how questions would be structured:

/*
INSERT INTO questions (
    category_id, 
    difficulty, 
    question_text, 
    options, 
    correct_option, 
    explanation,
    tags
) VALUES (
    'c1000000-0000-0000-0000-000000000001',
    'easy',
    'What is the minimum recommended CPU speed for a server-class ePO - On-prem server?',
    '[{"id": "A", "text": "1.5 GHz"}, {"id": "B", "text": "2.0 GHz"}, {"id": "C", "text": "2.2 GHz"}, {"id": "D", "text": "3.0 GHz"}]'::jsonb,
    'C',
    'According to Important sizing considerations, the minimum CPU core speed is 2.2 GHz.',
    ARRAY['sizing', 'hardware']
);
*/
