# Testing the API with a sample image

# import requests
# import os

# current_dir = os.path.dirname(os.path.abspath(__file__))

# file_path = os.path.join(current_dir, "data", "testpic1.jpg")

# url = "http://127.0.0.1:8000/upload-image/"

# if not os.path.exists(file_path):
#     print(f"Error: File not found at {file_path}")
#     exit(1)

# with open(file_path, "rb") as img:
#     files = {'file': ('testpic1.jpg', img, 'image/jpeg')}
#     response = requests.post(url, files=files)

# print("Status Code:", response.status_code)
# print("Response:", response.json())
