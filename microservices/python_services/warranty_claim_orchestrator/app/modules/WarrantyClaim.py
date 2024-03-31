from datetime import date

class WarrantyClaim:
    def __init__(self, serial_number : str, claim_date : date,
                 email : str, picture_of_receipt : any=None):
        self.serial_number : str = serial_number
        self.claim_date : date = claim_date
        self.email : str = email
        self.picture_of_receipt : any = picture_of_receipt
    
    def getSerialNumber(self):
        return self.serial_number
    
    def getClaimDate(self):
        return self.claim_date
    
    def getEmail(self):
        return self.email
    
    def getPictureOfReceipt(self):
        return self.picture_of_receipt