CREATE TABLE influencer (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    last_updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    created_by VARCHAR(255) NOT NULL,
    last_updated_by VARCHAR(255) NOT NULL,
    primary_platform VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(255),
    phone_number VARCHAR(10) NOT NULL,
    email VARCHAR(255),
    address VARCHAR(255),
    profile_picture VARCHAR(255) NOT NULL,
    languages TYPE language_enum[] DEFAULT NULL,
    next_reach_score INT DEFAULT 0 CHECK (next_reach_score >= 0),
    age INT DEFAULT 0 CHECK (age >= 0),
    insta_username VARCHAR(255),
    insta_profile_link VARCHAR(1000),
    youtube_username VARCHAR(255),
    youtube_profile_link VARCHAR(1000),
    fb_username VARCHAR(255),
    fb_profile_link VARCHAR(1000),
    niche VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    collab_type VARCHAR(255) NOT NULL,
    deliverables VARCHAR[],  -- Array of strings
    content_charge INT DEFAULT 0 CHECK (content_charge >= 0),
    views_charge INT DEFAULT 0 CHECK (views_charge >= 0)
);

-- Indexes for performance optimization
CREATE INDEX ix_influencer_phone_number ON influencer (phone_number);

-- Create the trigger function
CREATE OR REPLACE FUNCTION update_last_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER update_influencer_last_updated_at
BEFORE UPDATE ON influencer
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_at();

CREATE TYPE language_enum as ENUM ('HINDI', 'ENGLISH', 'BENGALI', 'TAMIL', 'TELUGU', 'MARATHI', 'GUJARATI'
,'MALAYALAM', 'KANNADA','ODIA', 'PUNJABI', 'ASSAMESE', 'URDU', 'SINDHI', 'SANSKRIT', 'KASHMIRI', 'MAITHILI'
)