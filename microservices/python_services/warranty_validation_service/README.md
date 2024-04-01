## API endpoint documentation:
URL: `/validate/<serial_number>`
Method: `GET`
Request Parameters (required):
```
claim_date (required): A datetime.date object indicating the date that the claim is submitted,
                        has the format of %Y-%m-%d, e.g. 2023-01-01
```

Response Structure:
200 ok
- message (str): A message describing the status of the warranty.
- status (str): A status indicating the status of the warranty.
Example: 
`Request: GET /validate/<serial_number>?claim_date=2023-03-21`
```
{
    "message": "Valid warranty",
    "status": "valid"
}
```

400 bad request
- message (str): A message describing the status of the warranty.
- status (str): A status indicating the status of the warranty. 
                Values: expired / valid
Example: 
`Request: GET /validate/<serial_number>?claim_date=2028-03-21`
```
{
    "message": "Expired warranty",
    "status": "expired"
}

{
    "message": "Invalid serial number",
    "status": "invalid"
}
```