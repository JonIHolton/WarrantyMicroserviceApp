from datetime import date

class Warranty:
    def __init__(self, serial_number : str, start_date : date, expiry_date : date):
        self.serial_number : str = serial_number
        self.start_date : date = start_date
        self.expiry_date : date = expiry_date
        
    def getSerialNumber(self):
        return self.serial_number
    
    def getStartDate(self):
        return self.start_date
    
    def getExpiryDate(self):
        return self.expiry_date

    def isValid(self, claim_date : date):
        return claim_date <= self.expiry_date
    
    def __str__(self):
        return f"Serial Number: {self.serial_number}, Start Date: {self.start_date}, Expiry Date: {self.expiry_date}"
    