from datetime import date

class WarrantyClaim:
    def __init__(self, 
                 unit_id : str, 
                 model_id : str, 
                 model_type : str,
                 claimee : str,
                 email : str,
                 description : str):
        
        self.unit_id : str = unit_id
        self.model_id : str = model_id
        self.model_type : str = model_type
        self.claimee : str = claimee
        self.email : str = email
        self.description : str = description
        
    def getUnitId(self):
        return self.unit_id
    
    def getModelId(self):
        return self.model_id
    
    def getModelType(self):
        return self.model_type
    
    def getClaimee(self):
        return self.claimee
    
    def getEmail(self):
        return self.email
    
    def getDescription(self):
        return self.description
        
    def __str__(self):
        return f"Unit ID: {self.unit_id}, Model ID: {self.model_id}, Model Type: {self.model_type}, Claimee: {self.claimee}, Email: {self.email}, Description: {self.description}"