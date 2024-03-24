/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50505
Source Host           : localhost:36693
Source Database       : shippingrecord

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2024-03-20 20:35:12
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for inventory
-- ----------------------------
DROP TABLE IF EXISTS `inventory`;
CREATE TABLE `inventory` (
  `InventoryID` int(11) NOT NULL AUTO_INCREMENT,
  `ClaimID` int(11) NOT NULL,
  `SerialNumber` varchar(255) NOT NULL,
  `Model` varchar(255) NOT NULL,
  `Condition` enum('New','Used','Repaired') NOT NULL,
  `Status` enum('InStock','ShippedToUser','ReceivedFromUser','AwaitingInspection','UnderRepair','ShippedToService','Disposed') NOT NULL,
  `ReturnAddress` text DEFAULT NULL,
  `ShipDate` date DEFAULT NULL,
  `ReceiveDate` date DEFAULT NULL,
  `Notes` text DEFAULT NULL,
  PRIMARY KEY (`InventoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of inventory
-- ----------------------------