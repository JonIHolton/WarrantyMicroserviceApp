CREATE DATABASE IF NOT EXISTS warranty_validation_db;
USE warranty_validation_db;

CREATE TABLE warranty (
    serial_number VARCHAR(255) PRIMARY KEY,
    start_date DATE,
    expiry_date DATE
);

-- Insert dummy values into the warranty table
INSERT INTO warranty (serial_number, start_date, expiry_date) VALUES 
('GV-N4090GAMING OC-24GD', '2023-01-01', '2024-01-01'),
('GeForce RTX 4090 GAMING X TRIO 24G', '2023-02-15', '2024-02-15'),
('GV-N4090GAMING', '2023-03-20', '2024-05-20');
