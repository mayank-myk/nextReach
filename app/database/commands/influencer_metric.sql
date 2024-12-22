CREATE TABLE influencer_metric (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    last_updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    created_by VARCHAR(255) NOT NULL,
    last_updated_by VARCHAR(255) NOT NULL,
    influencer_id INTEGER NOT NULL REFERENCES influencer(id),

    -- Instagram metrics
    insta_followers INTEGER CHECK (insta_followers >= 0) DEFAULT 0,
    insta_city_1 VARCHAR(255),
    insta_city_pc_1 INTEGER CHECK (insta_city_pc_1 >= 0) DEFAULT 0,
    insta_city_2 VARCHAR(255),
    insta_city_pc_2 INTEGER CHECK (insta_city_pc_2 >= 0) DEFAULT 0,
    insta_city_3 VARCHAR(255),
    insta_city_pc_3 INTEGER CHECK (insta_city_pc_3 >= 0) DEFAULT 0,
    insta_age_13_to_17 INTEGER CHECK (insta_age_13_to_17 >= 0) DEFAULT 0,
    insta_age_18_to_24 INTEGER CHECK (insta_age_18_to_24 >= 0) DEFAULT 0,
    insta_age_25_to_34 INTEGER CHECK (insta_age_25_to_34 >= 0) DEFAULT 0,
    insta_age_35_to_44 INTEGER CHECK (insta_age_35_to_44 >= 0) DEFAULT 0,
    insta_age_45_to_54 INTEGER CHECK (insta_age_45_to_54 >= 0) DEFAULT 0,
    insta_age_55 INTEGER CHECK (insta_age_55 >= 0) DEFAULT 0,
    insta_men_follower_pc INTEGER CHECK (insta_men_follower_pc >= 0) DEFAULT 0,
    insta_women_follower_pc INTEGER CHECK (insta_women_follower_pc >= 0) DEFAULT 0,
    insta_avg_views INTEGER CHECK (insta_avg_views >= 0) DEFAULT 0,
    insta_max_views INTEGER CHECK (insta_max_views >= 0) DEFAULT 0,
    insta_min_views INTEGER CHECK (insta_min_views >= 0) DEFAULT 0,
    insta_consistency_score INTEGER CHECK (insta_consistency_score >= 0) DEFAULT 0,
    insta_avg_likes INTEGER CHECK (insta_avg_likes >= 0) DEFAULT 0,
    insta_avg_comments INTEGER CHECK (insta_avg_comments >= 0) DEFAULT 0,
    insta_avg_shares INTEGER CHECK (insta_avg_shares >= 0) DEFAULT 0,
    insta_engagement_rate INTEGER CHECK (insta_engagement_rate >= 0) DEFAULT 0,

    -- YouTube metrics
    yt_followers INTEGER CHECK (yt_followers >= 0) DEFAULT 0,
    yt_city_1 VARCHAR(255),
    yt_city_pc_1 INTEGER CHECK (yt_city_pc_1 >= 0) DEFAULT 0,
    yt_city_2 VARCHAR(255),
    yt_city_pc_2 INTEGER CHECK (yt_city_pc_2 >= 0) DEFAULT 0,
    yt_city_3 VARCHAR(255),
    yt_city_pc_3 INTEGER CHECK (yt_city_pc_3 >= 0) DEFAULT 0,
    yt_avg_views INTEGER CHECK (yt_avg_views >= 0) DEFAULT 0,
    yt_max_views INTEGER CHECK (yt_max_views >= 0) DEFAULT 0,
    yt_min_views INTEGER CHECK (yt_min_views >= 0) DEFAULT 0,
    yt_consistency_score INTEGER CHECK (yt_consistency_score >= 0) DEFAULT 0,
    yt_avg_likes INTEGER CHECK (yt_avg_likes >= 0) DEFAULT 0,
    yt_avg_comments INTEGER CHECK (yt_avg_comments >= 0) DEFAULT 0,
    yt_avg_shares INTEGER CHECK (yt_avg_shares >= 0) DEFAULT 0,
    yt_engagement_rate INTEGER CHECK (yt_engagement_rate >= 0) DEFAULT 0,

    -- Facebook metrics
    fb_followers INTEGER CHECK (fb_followers >= 0) DEFAULT 0,
    fb_city_1 VARCHAR(255),
    fb_city_pc_1 INTEGER CHECK (fb_city_pc_1 >= 0) DEFAULT 0,
    fb_city_2 VARCHAR(255),
    fb_city_pc_2 INTEGER CHECK (fb_city_pc_2 >= 0) DEFAULT 0,
    fb_city_3 VARCHAR(255),
    fb_city_pc_3 INTEGER CHECK (fb_city_pc_3 >= 0) DEFAULT 0,
    fb_avg_views INTEGER CHECK (fb_avg_views >= 0) DEFAULT 0,
    fb_max_views INTEGER CHECK (fb_max_views >= 0) DEFAULT 0,
    fb_min_views INTEGER CHECK (fb_min_views >= 0) DEFAULT 0,
    fb_consistency_score INTEGER CHECK (fb_consistency_score >= 0) DEFAULT 0,
    fb_avg_likes INTEGER CHECK (fb_avg_likes >= 0) DEFAULT 0,
    fb_avg_comments INTEGER CHECK (fb_avg_comments >= 0) DEFAULT 0,
    fb_avg_shares INTEGER CHECK (fb_avg_shares >= 0) DEFAULT 0,
    fb_engagement_rate INTEGER CHECK (fb_engagement_rate >= 0) DEFAULT 0
);

-- Index for faster foreign key lookups
CREATE INDEX idx_influencer_metric_influencer_id ON influencer_metric (influencer_id);

-- Create the trigger function
CREATE OR REPLACE FUNCTION update_last_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER update_influencer_metric_last_updated_at
BEFORE UPDATE ON influencer_metric
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_at();