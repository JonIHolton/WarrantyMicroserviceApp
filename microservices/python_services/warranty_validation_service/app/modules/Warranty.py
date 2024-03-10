from datetime import datetime

class Warranty:
    def __init__(self, serial_number, start_date, expiry_date):
        self.serial_number = serial_number
        self.start_date = start_date
        self.expiry_date = expiry_date
        
    def getSerialNumber(self):
        return self.serial_number
    
    def getStartDate(self):
        return self.start_date
    
    def getExpiryDate(self):
        return self.expiry_date

    def isValid(self):
        return datetime.now().date() <= self.expiry_date
    
    def __str__(self):
        return f"Serial Number: {self.serial_number}, Start Date: {self.start_date}, Expiry Date: {self.expiry_date}"
    