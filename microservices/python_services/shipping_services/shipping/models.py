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
    Remarks = Column(String(254), nullable=False)

    def to_dict(self):
        return {
            'CaseID': self.CaseID,
            'ShippingInID': self.ShippingInID,
            'ReceivedDateTime': self.ReceivedDateTime.isoformat(),
            'ShippingOutID': self.ShippingOutID,
            'ShippingOutDateTime': self.ShippingOutDateTime.isoformat(),
            'Remarks': self.Remarks
        }
    