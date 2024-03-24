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
-- Table structure for shippingrecord
-- ----------------------------
DROP TABLE IF EXISTS `shippingrecord`;
CREATE TABLE `shippingrecord` (
  `CaseID` varchar(16) NOT NULL,
  `ShippingInID` varchar(16) NOT NULL,
  `ReceivedDateTime` datetime NOT NULL,
  `ShippingOutID` varchar(16) NOT NULL,
  `ShippingOutDateTime` datetime NOT NULL,
  `Remarks` varchar(254) NOT NULL,
  PRIMARY KEY (`CaseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of shippingrecord
-- ----------------------------