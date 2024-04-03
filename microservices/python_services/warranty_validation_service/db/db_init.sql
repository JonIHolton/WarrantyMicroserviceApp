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
('SN00000000000001', '2023-01-01', '2024-01-01'),
('SN00000000000002', '2023-02-15', '2024-02-15'),
('SN00000000000003', '2023-03-20', '2024-05-20'),
('SN00000000000004', '2023-01-01', '2024-01-01'),
('SN00000000000005', '2023-02-15', '2024-02-15'),
('SN00000000000006', '2023-03-20', '2024-05-20'),
('SN00000000000007', '2023-01-01', '2024-01-01'),
('SN00000000000008', '2023-02-15', '2024-02-15'),
('SN00000000000009', '2023-03-20', '2024-05-20'),
('SN000000000000010', '2023-01-01', '2024-01-01');
