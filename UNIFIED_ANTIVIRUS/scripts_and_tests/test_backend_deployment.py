#!/usr/bin/env python3
"""
Test script para verificar que el backend web desplegado funciona correctamente
"""

import requests
import json
import time
from datetime import datetime

# URL del backend desplegado
BASE_URL = "https://unified-antivirus-backend-blnbfe04p.vercel.app"
API_KEY = "unified-antivirus-api-key-2024"

def test_endpoint(url, method="GET", data=None, headers=None):
    """Test an endpoint and return response"""
    try:
        print(f"\n🔍 Testing {method} {url}")
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success!")
            try:
                json_data = response.json()
                print(f"Response: {json.dumps(json_data, indent=2)}")
                return json_data
            except:
                print(f"Response: {response.text}")
                return response.text
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def main():
    print("🛡️ UNIFIED_ANTIVIRUS Backend Test")
    print("=====================================")
    print(f"Testing backend at: {BASE_URL}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Dashboard page
    print("\n📊 Testing Dashboard Page")
    test_endpoint(BASE_URL)
    
    # Test 2: Clients API
    print("\n👥 Testing Clients API")
    test_endpoint(f"{BASE_URL}/api/clients", headers=headers)
    
    # Test 3: Dashboard API
    print("\n📈 Testing Dashboard API")
    test_endpoint(f"{BASE_URL}/api/dashboard", headers=headers)
    
    # Test 4: Send test log
    print("\n📝 Testing Log Submission")
    test_log = {
        "client_id": "test-client-001",
        "hostname": "test-machine",
        "ip_address": "192.168.1.100",
        "version": "1.0.0",
        "logs": [
            {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "logger": "test_logger",
                "message": "Test log message from test script",
                "component": "test_component",
                "plugin": "test_plugin",
                "metadata": {
                    "test": True,
                    "deployment_test": True
                }
            }
        ]
    }
    
    result = test_endpoint(f"{BASE_URL}/api/logs", method="POST", data=test_log, headers=headers)
    
    if result:
        print("\n✅ All tests completed successfully!")
        print(f"🌐 Backend URL: {BASE_URL}")
        print(f"🔑 API Key: {API_KEY}")
        print("\n📋 Next steps:")
        print("1. Configure your antivirus to use this backend URL")
        print("2. Update the API key in your config.json")
        print("3. Enable web_logging in your antivirus configuration")
    else:
        print("\n❌ Some tests failed. Check the backend deployment.")

if __name__ == "__main__":
    main()