CREATE TABLE warranty (
    serial_number VARCHAR(255) PRIMARY KEY,
    start_date DATE,
    expiry_date DATE
);

-- Insert dummy values into the warranty table
INSERT INTO warranty (serial_number, start_date, expiry_date) VALUES 
('SN123456', '2023-01-01', '2024-01-01'),
('SN234567', '2023-02-15', '2024-02-15'),
('SN345678', '2023-03-20', '2024-03-20');
