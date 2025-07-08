import os
import requests
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-resume-summary"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_huggingface(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)

    if response.status_code == 200:
        output = response.json()
        return output[0]["generated_text"] if isinstance(output, list) else output
    else:
        raise Exception(f"HF API Error: {response.status_code} - {response.text}")

# Prompt test
print(query_huggingface("Summarize the following resume: Bhavishya is a computer science student with experience in Java and web development..."))
