import requests
import os

BASE_URL = "http://localhost:8000"
EMAIL = "test_avatar@example.com"
PASSWORD = "password123"

def get_token():
    # Register or Login
    try:
        requests.post(f"{BASE_URL}/auth/register", json={"email": EMAIL, "password": PASSWORD})
    except:
        pass
    
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    if res.status_code != 200:
        print(f"Login failed: {res.text}")
        return None
    return res.json()["access_token"]

def verify_avatar():
    token = get_token()
    if not token: return

    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Card (Check Fallback)
    print("\n1. Creating Card...")
    card_data = {"title": "Avatar Test", "slug": "avatar-test"}
    res = requests.post(f"{BASE_URL}/cards", json=card_data, headers=headers)
    if res.status_code != 200:
        print(f"Create failed: {res.text}")
        return
    
    card = res.json()
    card_id = card["id"]
    print(f"Card created: {card_id}")
    
    if "dicebear.com" in card.get("avatar_url", ""):
        print("SUCCESS: Fallback avatar is present.")
    else:
        print(f"FAILURE: Fallback avatar missing or incorrect: {card.get('avatar_url')}")

    # 2. Upload Avatar
    print("\n2. Uploading Avatar...")
    # Create dummy image
    with open("test_avatar.png", "wb") as f:
        f.write(os.urandom(1024))
    
    with open("test_avatar.png", "rb") as f:
        files = {"file": ("test_avatar.png", f, "image/png")}
        res = requests.post(f"{BASE_URL}/cards/{card_id}/avatar", files=files, headers=headers)
    
    if res.status_code == 200:
        updated_card = res.json()
        new_url = updated_card.get("avatar_url")
        print(f"Upload success. New URL: {new_url}")
        if "/static/uploads/" in new_url:
            print("SUCCESS: Avatar URL points to static uploads.")
        else:
            print("FAILURE: Avatar URL format incorrect.")
    else:
        print(f"FAILURE: Upload failed: {res.text}")

    # Cleanup
    try:
        os.remove("test_avatar.png")
    except:
        pass

if __name__ == "__main__":
    verify_avatar()
