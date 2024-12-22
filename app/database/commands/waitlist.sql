CREATE TABLE waitlist (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    entity_type VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
    email VARCHAR(255),
    social_media_handle VARCHAR(255),
    onboarding_status VARCHAR(255) NOT NULL DEFAULT 'PROCESSING',
    message VARCHAR(1000)
);

