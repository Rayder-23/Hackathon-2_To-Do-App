import os
from dotenv import load_dotenv
import requests
import time

# Load environment variables
load_dotenv()

def test_api_endpoints():
    """Test the API endpoints to make sure they are working."""
    base_url = "http://localhost:8000"  # Default FastAPI port

    print("Testing API endpoints...")
    print("=" * 50)

    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint (/): Status {response.status_code}")
        if response.status_code == 200:
            print("  SUCCESS: Root endpoint is accessible")
        else:
            print(f"  ERROR: Root endpoint returned {response.status_code}")
    except Exception as e:
        print(f"Root endpoint (/): ERROR - {e}")

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health endpoint (/health): Status {response.status_code}")
        if response.status_code == 200:
            print("  SUCCESS: Health endpoint is accessible")
        else:
            print(f"  ERROR: Health endpoint returned {response.status_code}")
    except Exception as e:
        print(f"Health endpoint (/health): ERROR - {e}")

    # Test users endpoint (expecting 401/405 since it requires authentication)
    try:
        response = requests.get(f"{base_url}/api/users")
        print(f"Users endpoint (/api/users): Status {response.status_code}")
        # This is expected to return 401/405 depending on implementation
        print(f"  INFO: Users endpoint returned {response.status_code} (expected for protected route)")
    except Exception as e:
        print(f"Users endpoint (/api/users): ERROR - {e}")

    # Test tasks endpoint (expecting 401 since it requires authentication)
    try:
        response = requests.get(f"{base_url}/api/1/tasks")
        print(f"Tasks endpoint (/api/1/tasks): Status {response.status_code}")
        # This is expected to return 401 for unauthorized access
        print(f"  INFO: Tasks endpoint returned {response.status_code} (expected for protected route)")
    except Exception as e:
        print(f"Tasks endpoint (/api/1/tasks): ERROR - {e}")

    print("=" * 50)
    print("API endpoint testing completed!")

if __name__ == "__main__":
    print("Starting API endpoint tests...")
    test_api_endpoints()