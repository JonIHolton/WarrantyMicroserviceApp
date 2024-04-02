CREATE DATABASE IF NOT EXISTS warranty_validation_db;
USE warranty_validation_db;

DROP TABLE IF EXISTS warranty;

CREATE TABLE warranty (
    serial_number VARCHAR(255) PRIMARY KEY,
    start_date DATE,
    expiry_date DATE
);

-- Insert dummy values into the warranty table
INSERT INTO warranty (serial_number, start_date, expiry_date) VALUES 
('SN1234-5678-9012-3456', '2023-01-01', '2024-01-01'),
('SN1234-5678-9012-3457', '2023-02-15', '2024-02-15'),
('SN1234-5678-9012-3458', '2023-03-20', '2024-05-20'),
('U12345', '2023-01-01', '2024-01-01'),
('U12346', '2023-02-15', '2024-02-15'),
('U12347', '2023-03-20', '2024-05-20');
