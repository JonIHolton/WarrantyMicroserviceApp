class WarrantyClaim:
    def __init__(self, serial_number, claim_date, email, picture_of_receipt=None):
        self.serial_number = serial_number
        self.claim_date = claim_date
        self.email = email
        self.picture_of_receipt = picture_of_receipt
    
    def getSerialNumber(self):
        return self.serial_number
    
    def getClaimDate(self):
        return self.claim_date
    
    def getEmail(self):
        return self.email
    
    def getPictureOfReceipt(self):
        return self.picture_of_receipt