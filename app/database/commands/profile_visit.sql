CREATE TABLE profile_visit (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    last_visited_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    influencer_id INTEGER NOT NULL REFERENCES influencer(id),
    user_id INTEGER NOT NULL REFERENCES user_table(id),
    CONSTRAINT unique_profile_visit UNIQUE (influencer_id, user_id, created_at)
);

-- Indexes for performance
CREATE INDEX idx_profile_visit_influencer_id ON profile_visit (influencer_id);
CREATE INDEX idx_profile_visit_user_id ON profile_visit (user_id);