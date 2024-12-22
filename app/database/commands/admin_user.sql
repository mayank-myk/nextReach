CREATE TABLE admin_user (
    id SERIAL PRIMARY KEY,
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    last_updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    admin_id VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    admin_type VARCHAR(50) NOT NULL DEFAULT 'SUPER_ADMIN'
);

CREATE INDEX idx_admin_user_admin_id ON admin_user (admin_id);

-- Create the trigger function
CREATE OR REPLACE FUNCTION update_last_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER update_admin_user_last_updated_at
BEFORE UPDATE ON admin_user
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_at();