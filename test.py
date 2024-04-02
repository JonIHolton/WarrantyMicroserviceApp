import requests

api_url = f"http://localhost:5000/requests/1/status"

update_data = {
    "status": "completed"
}

response = requests.patch(api_url, json=update_data, headers={"claimee":"", "email": ""})

print(response.text)