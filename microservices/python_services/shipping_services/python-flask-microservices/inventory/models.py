# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Enum, String, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from extensions import db
Base = db.Model



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