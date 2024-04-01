-- financialrecords.sql
CREATE DATABASE IF NOT EXISTS FinancialRecordsDB;

USE FinancialRecordsDB;

CREATE TABLE IF NOT EXISTS RefundRecords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status ENUM('initiated', 'processed', 'completed') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
