# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import relationship
from extensions import db
Base = db.Model



class GpuModel(Base):
    __tablename__ = 'gpu_model'

    ModelID = Column(INTEGER(11), primary_key=True)
    ModelName = Column(String(255))
    Manufacturer = Column(String(255))
    InventoryCount = Column(INTEGER(11))

    def to_dict(self):
        return {
            'ModelID': self.ModelID,
            'ModelName': self.ModelName,
            'Manufacturer': self.Manufacturer,
            'InventoryCount': self.InventoryCount
        }



class Gpu(Base):
    __tablename__ = 'gpu'

    SerialNumber = Column(String(16), primary_key=True)
    ModelID = Column(Integer, ForeignKey('gpu_model.ModelID', ondelete='SET NULL', onupdate='CASCADE'), index=True)

    def to_dict(self):
        return {
            'SerialNumber': self.SerialNumber,
            'ModelID': self.ModelID
        }



class Inventory(Base):
    __tablename__ = 'inventory'

    InventoryID = Column(INTEGER(11), primary_key=True)
    ClaimID = Column(INTEGER(11), nullable=False)
    SerialNumber = Column(String(255), nullable=False)
    Model = Column(String(255), nullable=False)
    Condition = Column(Enum('New', 'Used', 'Repaired'), nullable=False)
    Status = Column(Enum('InStock', 'ShippedToUser', 'ReceivedFromUser', 'AwaitingInspection', 'UnderRepair', 'ShippedToService', 'Disposed'), nullable=False)
    ReturnAddress = Column(Text)
    ShipDate = Column(Date)
    ReceiveDate = Column(Date)
    Notes = Column(Text)

    def to_dict(self):
        return {
            'InventoryID': self.InventoryID,
            'ClaimID': self.ClaimID,
            'SerialNumber': self.SerialNumber,
            'Model': self.Model,
            'Condition': self.Condition,
            'Status': self.Status,
            'ReturnAddress': self.ReturnAddress,
            'ShipDate': self.ShipDate.isoformat() if self.ShipDate else None,
            'ReceiveDate': self.ReceiveDate.isoformat() if self.ReceiveDate else None,
            'Notes': self.Notes
        }