import requests
import os
from dotenv import load_dotenv

load_dotenv()  # loads HACKATIME_API_KEY from .env

API_KEY = os.getenv("HACKATIME_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get("https://hackatime.hackclub.com/api/v1/stats", headers=headers)

if response.status_code == 200:
    stats = response.json()
    print("✅ Coding Stats from HackaTime:")
    print(stats)
else:
    print("❌ Failed to fetch stats:", response.status_code)
