CREATE TABLE watchlist (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    influencer_id INTEGER NOT NULL REFERENCES influencer(id),
    user_id INTEGER NOT NULL REFERENCES user_table(id),
    CONSTRAINT fk_influencer FOREIGN KEY (influencer_id) REFERENCES influencer(id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user_table(id)
);

-- Indexes for performance
CREATE INDEX idx_watchlist_influencer_id ON watchlist (influencer_id);
CREATE INDEX idx_watchlist_user_id ON watchlist (user_id);