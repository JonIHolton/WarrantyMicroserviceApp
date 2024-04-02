# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Enum, String, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from extensions import db
Base = db.Model


class ShippingRecord(Base):
    __tablename__ = 'shippingrecord'

    CaseID = Column(String(16), primary_key=True)
    ShippingInID = Column(String(16), nullable=False)
    ReceivedDateTime = Column(DateTime, nullable=False)
    ShippingOutID = Column(String(16), nullable=False)
    ShippingOutDateTime = Column(DateTime, nullable=False)
    ReturnAddress = Column(String(500), nullable=False)
    InSerialNumber = Column(String(16), nullable=False)
    InBrand = Column(String(255), nullable=False)
    InModel = Column(String(255), nullable=False)
    Email = Column(String(50), nullable=False)
    Remarks = Column(String(254), nullable=False)

    def to_dict(self):
        return {
            'CaseID': self.CaseID,
            'ShippingInID': self.ShippingInID,
            'ReceivedDateTime': self.ReceivedDateTime.isoformat() if self.ReceivedDateTime else None,
            'ShippingOutID': self.ShippingOutID,
            'ShippingOutDateTime': self.ShippingOutDateTime.isoformat() if self.ShippingOutDateTime else None,
            'ReturnAddress': self.ReturnAddress,
            'InSerialNumber': self.InSerialNumber,
            'InBrand': self.InBrand,
            'InModel': self.InModel,
            'Email': self.Email,
            'Remarks': self.Remarks
        }
    