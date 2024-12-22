CREATE TABLE user_table (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    last_updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    created_by VARCHAR(255) NOT NULL,
    last_updated_by VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    phone_number VARCHAR(10) NOT NULL,
    business_name VARCHAR(255),
    email VARCHAR(255),
    city VARCHAR(255),
    niche VARCHAR(255),
    category VARCHAR(255),
    total_profile_visited INTEGER NOT NULL DEFAULT 0 CHECK (total_profile_visited >= 0),
    balance_profile_visits INTEGER NOT NULL DEFAULT 20 CHECK (balance_profile_visits >= 0),
    insta_username VARCHAR(255),
    insta_profile_link VARCHAR(255),
    insta_followers INTEGER DEFAULT 0 CHECK (insta_followers >= 0),
    yt_username VARCHAR(255),
    yt_profile_link VARCHAR(255),
    yt_followers INTEGER DEFAULT 0 CHECK (yt_followers >= 0),
    fb_username VARCHAR(255),
    fb_profile_link VARCHAR(255),
    fb_followers INTEGER DEFAULT 0 CHECK (fb_followers >= 0)
);

-- Indexes for performance
CREATE INDEX idx_user_phone_number ON user_table (phone_number);

-- Create the trigger function
CREATE OR REPLACE FUNCTION update_last_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER update_user_table_last_updated_at
BEFORE UPDATE ON user_table
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_at();