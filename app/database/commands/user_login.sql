CREATE TABLE user_login (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    otp VARCHAR(5) NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
    CONSTRAINT check_otp_length CHECK (LENGTH(otp) = 5),
    CONSTRAINT check_phone_number_length CHECK (LENGTH(phone_number) = 10)
);

-- Indexes for performance
CREATE INDEX idx_user_login_phone_number ON user_login (phone_number);
