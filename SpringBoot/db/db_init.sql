CREATE DATABASE IF NOT EXISTS requests;
USE requests;

CREATE TABLE requests (
    request_Id INT AUTO_INCREMENT PRIMARY KEY,
    unit_Id VARCHAR(255),
    model_Id VARCHAR(255),
    model_Type VARCHAR(255),
    claimee VARCHAR(255),
    email VARCHAR(255),
    description TEXT,
    status VARCHAR(255),
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert dummy values into the requests table