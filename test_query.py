# test_query.py
import requests

url = "http://localhost:8000/api/v1/hackrx/run"
headers = {
    "Authorization": "Bearer 754cd51c1f0eedef7f6b16e092d6ed8ad94579e08a543b6dec0b2a8cd795db62",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

data = {
    "documents": "https://hackrx.blob.core.windows.net/assets/Arogya%20Sanjeevani%20Policy%20-%20CIN%20-%20U10200WB1906GOI001713%201.pdf?sv=2023-01-03&st=2025-07-21T08%3A29%3A02Z&se=2025-09-22T08%3A29%3A00Z&sr=b&sp=r&sig=nzrz1K9Iurt%2BBXom%2FB%2BMPTFMFP3PRnIvEsipAX10Ig4%3D",
    "questions": [
        "Does this policy cover knee surgery, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are organ donor medical expenses covered under this policy?"
    ]
}

response = requests.post(url, json=data, headers=headers)
print("HTTP Status:", response.status_code)
print("Response JSON:", response.json())
