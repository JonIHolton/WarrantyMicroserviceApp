import mysql.connector
from modules.Warranty import Warranty
from datetime import datetime
from dotenv import load_dotenv
import os

class WarrantyDAO:
    def __init__(self):
        load_dotenv()
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def get_warranty(self, serial_number):
        # This is safe from SQL injection
        self.cursor.execute('SELECT * FROM warranty WHERE serial_number = %s', (serial_number,))
        result = self.cursor.fetchone()
        if result:
            return Warranty(result['serial_number'], result['start_date'], result['expiry_date'])
        return None
    
    def get_all_warranties(self):
        self.cursor.execute('SELECT * FROM warranty')
        result = self.cursor.fetchall()
        warranties = []
        for row in result:
            warranties.append(Warranty(row['serial_number'], row['start_date'], row['expiry_date']))
        return warranties
    
    def add_warranty(self, warranty):
        (self.cursor.execute('INSERT INTO warranty (serial_number, start_date, expiry_date) VALUES (%s, %s, %s)', 
                             (warranty.getSerialNumber(), warranty.getStartDate(), warranty.getExpiryDate())))
        self.connection.commit()