from datetime import date

class WarrantyClaim:
    def __init__(self, serial_number : str, claim_date : date,
                 email : str, reason_for_claim: str,
                 proof_of_claim : any=None):
        self.serial_number : str = serial_number
        self.claim_date : date = claim_date
        self.email : str = email
        self.reason_for_claim : str = reason_for_claim
        self.proof_of_claim : any = proof_of_claim
    
    def getSerialNumber(self):
        return self.serial_number
    
    def getClaimDate(self):
        return self.claim_date
    
    def getEmail(self):
        return self.email
    
    def getReasonForClaim(self):
        return self.reason_for_claim
    
    def getPictureOfReceipt(self):
        return self.proof_of_claim
    
    def __str__(self):
        return f"Serial Number: {self.serial_number}, Claim Date: {self.claim_date}, Email: {self.email}, Reason for Claim: {self.reason_for_claim}"