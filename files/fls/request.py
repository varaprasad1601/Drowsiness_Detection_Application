import requests
url = 'https://irctctrainticketextracter.pythonanywhere.com/app_api'
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    for i in data:
        print(i['id'])
    # Process the retrieved data as needed
else:
    print('Error: Failed to retrieve data. Status code:', response.status_code)
