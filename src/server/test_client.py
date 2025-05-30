import requests
import json


BASE_URL = "http://localhost:8000"

def test_home():
    """Test the home endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print("\n=== Testing Home Endpoint ===")
    print(f"Status code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_send_data():
    """Test sending JSON data"""
    test_data = {
        "test": "hello",
        "number": 42,
        "list": [1, 2, 3]
    }
    
    # Wrap the data in a "data" field as expected by the API
    data = {
        "data": test_data
    }
    
    print("\n=== Testing Data Submission ===")
    print("Sending data:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))
    
    response = requests.post(
        f"{BASE_URL}/api/data",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus code: {response.status_code}")
    print("Server response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_get_all_data():
    """Test retrieving all stored data"""
    print("\n=== Testing Data Retrieval ===")
    response = requests.get(f"{BASE_URL}/api/data")
    
    print(f"Status code: {response.status_code}")
    print("Stored data:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print("🚀 Starting tests...")
    print("Make sure the server is running at http://localhost:8000")
    
    try:
        test_home()
        test_send_data()
        test_get_all_data()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server")
        print("Make sure the server is running and accessible at http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}") 