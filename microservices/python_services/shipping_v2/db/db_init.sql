SET FOREIGN_KEY_CHECKS=0;


CREATE DATABASE IF NOT EXISTS shippingrecord;
USE shippingrecord;

DROP TABLE IF EXISTS `shippingrecord`;
CREATE TABLE `shippingrecord` (
  `CaseID` varchar(16) NOT NULL,
  `ShippingInID` varchar(16) DEFAULT NULL,
  `ReceivedDateTime` datetime DEFAULT NULL,
  `ShippingOutID` varchar(16) DEFAULT NULL,
  `ShippingOutDateTime` datetime DEFAULT NULL,
  `ReturnAddress` varchar(500) DEFAULT '',
  `InSerialNumber` varchar(16) DEFAULT '',
  `InBrand` varchar(255) DEFAULT '',
  `InModel` varchar(255) DEFAULT '',
  `Email` varchar(50) DEFAULT '',
  `Remarks` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`CaseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE DATABASE IF NOT EXISTS inventory;
USE inventory;


DROP TABLE IF EXISTS `gpu_model`;
CREATE TABLE `gpu_model` (
  `ModelID` int(11) NOT NULL AUTO_INCREMENT,
  `ModelName` varchar(255) DEFAULT NULL,
  `model_Type` varchar(255) DEFAULT NULL,
  `InventoryCount` int(11) DEFAULT NULL,
  PRIMARY KEY (`ModelID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;


INSERT INTO `gpu_model` VALUES ('1', 'Asus GeForce RTX 3080', '3080', '8');
INSERT INTO `gpu_model` VALUES ('2', 'Evga GeForce RTX 3080', '6800', '7');
INSERT INTO `gpu_model` VALUES ('3', 'Asus GeForce RTX 3070', '3070', '14');
INSERT INTO `gpu_model` VALUES ('4', 'Asus GeForce RTX 3060', '6900', '10');
INSERT INTO `gpu_model` VALUES ('5', 'Evga GeForce RTX 3060', '3060', '9');
INSERT INTO `gpu_model` VALUES ('6', 'Asus GeForce RTX 3090', '6700', '7');
INSERT INTO `gpu_model` VALUES ('7', 'Evga GeForce GTX 1660 Super', '3090', '4');
INSERT INTO `gpu_model` VALUES ('8', 'Evga GeForce GTX 4080', '4080', '0');
INSERT INTO `gpu_model` VALUES ('9', 'MSI GeForce GTX RTX 3080', '3080', '4');
INSERT INTO `gpu_model` VALUES ('10', 'Zotac GeForce GTX RTX 3080', '3080', '0');



DROP TABLE IF EXISTS `gpu`;
CREATE TABLE `gpu` (
  `SerialNumber` varchar(16) NOT NULL,
  `ModelID` int(11) DEFAULT NULL,
  PRIMARY KEY (`SerialNumber`),
  KEY `fk_gpu_model` (`ModelID`),
  CONSTRAINT `fk_gpu_model` FOREIGN KEY (`ModelID`) REFERENCES `gpu_model` (`ModelID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO `gpu` VALUES ('SN00000000000001', '1');
INSERT INTO `gpu` VALUES ('SN00000000000002', '2');
INSERT INTO `gpu` VALUES ('SN00000000000003', '3');
INSERT INTO `gpu` VALUES ('SN00000000000004', '4');
INSERT INTO `gpu` VALUES ('SN00000000000005', '5');
INSERT INTO `gpu` VALUES ('SN00000000000006', '6');
INSERT INTO `gpu` VALUES ('SN00000000000007', '7');
INSERT INTO `gpu` VALUES ('SN00000000000008', '8');
INSERT INTO `gpu` VALUES ('SN00000000000009', '9');
INSERT INTO `gpu` VALUES ('SN00000000000010', '10');


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

