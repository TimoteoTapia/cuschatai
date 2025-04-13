CREATE TABLE IF NOT EXISTS company_settings (
    company_name VARCHAR(255) NOT NULL,
    initial_context TEXT NOT NULL
);

INSERT INTO company_settings (company_name, initial_context) 
VALUES ('Dunder Mifflin', 'You are a customer service representative for Dunder Mifflin Paper Company...');
