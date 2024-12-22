CREATE TABLE campaign (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    last_updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    created_by VARCHAR(255) NOT NULL,
    last_updated_by VARCHAR(255) NOT NULL,
    campaign_managed_by VARCHAR(255) NOT NULL,
    influencer_id INTEGER NOT NULL REFERENCES influencer(id),
    user_id INTEGER NOT NULL REFERENCES user_table(id),
    stage VARCHAR(100) NOT NULL,
    content_charge INTEGER CHECK (content_charge >= 0),
    views_charge INTEGER CHECK (views_charge >= 0),
    type_of_content VARCHAR(100),
    campaign_notes VARCHAR(1000),
    rating INTEGER CHECK (rating >= 0 AND rating <= 5),
    review VARCHAR(1000),
    influencer_finalization_date DATE,
    content_shoot_date DATE,
    content_post_date DATE,
    content_billing_amount INTEGER CHECK (content_billing_amount >= 0),
    content_billing_payment_at TIMESTAMP,
    content_billing_payment_status VARCHAR(100),
    insta_post_link VARCHAR(255),
    youtube_post_link VARCHAR(255),
    fb_post_link VARCHAR(255),
    first_billing_date DATE,
    first_billing_views INTEGER CHECK (first_billing_views >= 0),
    first_billing_likes INTEGER CHECK (first_billing_likes >= 0),
    first_billing_comments INTEGER CHECK (first_billing_comments >= 0),
    first_billing_shares INTEGER CHECK (first_billing_shares >= 0),
    first_billing_amount INTEGER CHECK (first_billing_amount >= 0),
    first_billing_payment_at TIMESTAMP,
    first_billing_payment_status VARCHAR(100),
    second_billing_date DATE,
    second_billing_views INTEGER CHECK (second_billing_views >= 0),
    second_billing_likes INTEGER CHECK (second_billing_likes >= 0),
    second_billing_comments INTEGER CHECK (second_billing_comments >= 0),
    second_billing_shares INTEGER CHECK (second_billing_shares >= 0),
    second_billing_amount INTEGER CHECK (second_billing_amount >= 0),
    second_billing_payment_at TIMESTAMP,
    second_billing_payment_status VARCHAR(100),
    post_insights VARCHAR[],
    pending_deliverables VARCHAR[]
);

-- Indexes
CREATE INDEX idx_campaign_user_id ON campaign (user_id);
CREATE INDEX idx_campaign_influencer_id ON campaign (influencer_id);
CREATE INDEX idx_campaign_stage ON campaign (stage);

-- Create the trigger function
CREATE OR REPLACE FUNCTION update_last_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER update_campaign_last_updated_at
BEFORE UPDATE ON campaign
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_at();
