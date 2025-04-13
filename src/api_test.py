import requests

url = "http://127.0.0.1:8000/upload-image/"
file_path = "C:\\Users\\Administrator\\Desktop\\divergence-vs-convergence-tests.png"  # <-- Replace with a real file path

with open(file_path, "rb") as img:
    files = {'file': (file_path, img, 'image/jpeg')}
    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response:", response.json())
