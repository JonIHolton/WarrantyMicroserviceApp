SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `shippingrecord` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `shippingrecord`;

DROP TABLE IF EXISTS `shippingrecord`;
CREATE TABLE IF NOT EXISTS `shippingrecord` (
  `CaseID` varchar(16) NOT NULL,
  `ShippingInID` varchar(16) NOT NULL,
  `ReceivedDateTime` datetime NOT NULL,
  `ShippingOutID` varchar(16) NOT NULL,
  `ShippingOutDateTime` datetime NOT NULL,
  `Remarks` varchar(254) NOT NULL,
  
  PRIMARY KEY (`CaseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `shippingrecord` (`CaseID`, `ShippingInID`, `ReceivedDateTime`, `ShippingOutID`, `ShippingOutDateTime`, `Remarks`) VALUES
('1', '123', '2023-12-11 07:12:31', '111', '2023-12-20 07:12:31', 'shipped'),
('2', '456', '2023-12-11 07:12:32', '222', '2023-12-21 07:12:31', 'shipped'),
('3', '789', '2023-12-11 07:12:33', '333', '2023-12-22 07:12:31', 'shipped');
COMMIT;

