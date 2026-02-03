import requests

BASE_URL = "https://ai-agentic-honeypot.vercel.app"

print("=" * 80)
print("API ENDPOINT TESTER SIMULATION")
print("=" * 80)
print("\nSimulating the exact scenario that was causing INVALID_REQUEST_BODY error:")
print("  • Method: POST")
print("  • Path: /")
print("  • Body: None (empty)")
print("  • Content-Type: Not set\n")

try:
    # Exact scenario from the tester
    r = requests.post(BASE_URL + "/", data="")
    
    print(f"Status Code: {r.status_code}")
    print(f"Response Headers: {dict(r.headers)}")
    print(f"Response Body: {r.text}")
    
    # Try to parse as JSON
    try:
        data = r.json()
        print(f"\n✅ Response is valid JSON: {data}")
    except:
        print(f"\n❌ Response is NOT valid JSON")
        
    # Check if it's an error response
    if "INVALID_REQUEST_BODY" in r.text.upper():
        print("\n❌ ERROR: Still getting INVALID_REQUEST_BODY!")
    elif r.status_code == 405:
        print("\n❌ ERROR: Getting 405 Method Not Allowed!")
    elif r.status_code == 200:
        print("\n✅ SUCCESS: Root endpoint returns 200 OK as expected!")
    else:
        print(f"\n⚠️  Unexpected status code: {r.status_code}")
        
except Exception as e:
    print(f"❌ Request failed with error: {e}")

print("\n" + "=" * 80)
