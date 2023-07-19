import requests

# Define the base URL
base_url = "http://127.0.0.1:8000/user_register"

# Define the data to be sent
data = {
    'name': 'value1',
    'p_code': 'value2',
    'number': 'value3',
    'company': 'value4',
    'face_encodings': 'value5',
}

# Send the request with data
response = requests.get(base_url, params=data)

# Check the response
if response.status_code == 200:
    print("Request was successful.")
    print("Response:", response.text)
else:
    print("Request failed with status code:", response.status_code)
