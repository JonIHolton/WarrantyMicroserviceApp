-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
--
CREATE DATABASE IF NOT EXISTS `refund_records` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `refund_records`;

-- --------------------------------------------------------

DROP TABLE IF EXISTS `refund_records`;
CREATE TABLE IF NOT EXISTS `refund_records` (
  `RequestID` int(16) NOT NULL,
  `RefundAmt` decimal(10,2) NOT NULL,
  `RefundDateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`RequestID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--

INSERT INTO `refund_records` (`RequestID`, `RefundAmt`, `RefundDateTime`) VALUES
('1', '894.62', '2023-12-11 07:12:31'),
('2', '619.38', '2023-12-11 07:12:31'),
('3', '1024.52', '2023-12-11 07:12:31');
COMMIT;

