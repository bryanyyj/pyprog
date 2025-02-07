import requests

BOT_TOKEN = "7823253969:AAEYvW89aQ3a5ozS2rhJmpEAy-hv7q-a-sM"
CHAT_ID = "1874241047"
MESSAGE = "Hello from my bot!"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": MESSAGE}

response = requests.post(url, data=data)
print(response.json())  # Check the response
