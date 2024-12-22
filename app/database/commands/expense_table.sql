CREATE TABLE expense (
    id SERIAL PRIMARY KEY,
    created_by VARCHAR(255) NOT NULL,
    last_updated_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    last_updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Kolkata',
    type VARCHAR(255) NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    amount INTEGER NOT NULL CHECK (amount >= 1),
    description VARCHAR(255) NOT NULL,
    mode_of_payment VARCHAR(255) NOT NULL,
    account_id VARCHAR(255) NOT NULL
);

-- Create the trigger function
CREATE OR REPLACE FUNCTION update_last_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER update_expense_last_updated_at
BEFORE UPDATE ON expense
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_at();