import requests
import time

BASE_URL = "http://localhost:8000"

def test_qr_endpoint():
    print("Testing QR Endpoint...")
    # Using a dummy slug, expecting 404 but checking for rate limit headers or just connectivity
    # Ideally we need a real slug, but 404 is enough to prove the endpoint is reachable and not 500
    try:
        response = requests.get(f"{BASE_URL}/public/cards/test-slug-123/qrcode")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 404:
            print("Success: Endpoint reachable (returned 404 as expected for dummy slug)")
        elif response.status_code == 200:
            print("Success: Endpoint reachable and returned QR")
        else:
            print(f"Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def test_rate_limit():
    print("\nTesting Rate Limit (25 requests)...")
    limit_hit = False
    for i in range(25):
        response = requests.get(f"{BASE_URL}/public/cards/test-slug-123/qrcode")
        if response.status_code == 429:
            print(f"Request {i+1}: 429 Too Many Requests (Rate Limit Hit!)")
            limit_hit = True
            break
        else:
            print(f"Request {i+1}: {response.status_code}")
    
    if limit_hit:
        print("Success: Rate limiting is working.")
    else:
        print("Failure: Rate limit was not hit.")

if __name__ == "__main__":
    test_qr_endpoint()
    test_rate_limit()
