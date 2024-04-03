CREATE DATABASE IF NOT EXISTS requests;
USE requests;

DROP TABLE IF EXISTS requests;

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
INSERT INTO requests (unit_Id, model_Id, model_Type, claimee, email, description, status)
VALUES
('SN130000000001', 'Nvidia RTX 3050', '3050', 'Charlie Brown', 'charliebrown@example.com', 'Display issue.', 'Pending'),
('SN130000000002', 'Nvidia RTX 3060', '3060', 'Lucy Van Pelt', 'lucyvanpelt@example.com', 'Overheating.', 'Pending'),
('SN130000000003', 'Nvidia RTX 3070', '3070', 'Linus Van Pelt', 'linusvanpelt@example.com', 'Fan noise.', 'Pending'),
('SN130000000004', 'Nvidia RTX 3080 Ti', '3080', 'Peppermint Patty', 'peppermintpatty@example.com', 'Not detected by PC.', 'Pending'),
('SN130000000005', 'Nvidia RTX 3090', '3090', 'Marcie', 'marcie@example.com', 'BSOD on boot.', 'Pending'),
('SN130000000006', 'Nvidia RTX 3070 Ti', '3070', 'Sally Brown', 'sallybrown@example.com', 'Artifacting.', 'Pending'),
('SN130000000007', 'Nvidia RTX 3060 Ti', '3060', 'Schroeder', 'schroeder@example.com', 'No HDMI output.', 'Pending'),
('SN130000000008', 'Nvidia RTX 3080', '3080', 'Frieda', 'frieda@example.com', 'Random restarts.', 'Pending'),
('SN130000000009', 'Nvidia RTX 3050 Ti', '3050', 'Pig Pen', 'pigpen@example.com', 'Low FPS.', 'Pending'),
('SN130000000010', 'Nvidia RTX 3090 Ti', '3090', 'Franklin', 'franklin@example.com', 'Driver crash.', 'Pending');