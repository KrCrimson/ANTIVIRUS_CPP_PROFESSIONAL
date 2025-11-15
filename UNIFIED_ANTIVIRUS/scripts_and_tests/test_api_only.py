#!/usr/bin/env python3
"""
API-Only Test Script for UNIFIED_ANTIVIRUS Backend
Tests only the API endpoints that the antivirus will use, bypassing web authentication
"""

import requests
import json
import time
from datetime import datetime

# URL del backend desplegado
BASE_URL = "https://unified-antivirus-csitvest3-sebastians-projects-487d2baa.vercel.app"
API_KEY = "unified-antivirus-api-key-2024"

def test_api_endpoint(url, method="GET", data=None, headers=None, description=""):
    """Test API endpoint directly"""
    try:
        print(f"\n🔍 {description}")
        print(f"Testing {method} {url}")
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=15)
        
        print(f"Status: {response.status_code}")
        
        # Check if it's an HTML response (Vercel auth page)
        content_type = response.headers.get('content-type', '')
        if 'text/html' in content_type and response.status_code == 401:
            print("⚠️  Web authentication required (expected for web interface)")
            print("📡 APIs may still work for programmatic access")
            return "auth_required"
        
        if response.status_code == 200:
            print("✅ Success!")
            try:
                json_data = response.json()
                print(f"Response: {json.dumps(json_data, indent=2)}")
                return json_data
            except:
                print(f"Response: {response.text[:200]}...")
                return response.text
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Response: {response.text[:200]}...")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return None

def test_direct_api_calls():
    """Test API endpoints directly without web interface"""
    print("🛡️ UNIFIED_ANTIVIRUS API-Only Backend Test")
    print("=============================================")
    print(f"Backend: {BASE_URL}")
    print("Testing API endpoints that antivirus will use...")
    
    # Headers for API requests
    api_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "UNIFIED_ANTIVIRUS/1.0.0"
    }
    
    # Test 1: Direct Log Submission (This is what the antivirus will use)
    print("\n" + "="*50)
    test_log_data = {
        "client_id": "test-antivirus-001",
        "hostname": "test-machine",
        "ip_address": "192.168.1.100", 
        "version": "1.0.0",
        "logs": [
            {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "logger": "api_test",
                "message": "API test log from direct backend test",
                "component": "test_api",
                "plugin": "api_tester",
                "metadata": {
                    "test_type": "api_direct",
                    "backend_test": True
                }
            }
        ]
    }
    
    log_result = test_api_endpoint(
        f"{BASE_URL}/api/logs",
        method="POST",
        data=test_log_data,
        headers=api_headers,
        description="📝 Testing Direct Log Submission (Primary API for Antivirus)"
    )
    
    # Test 2: Health Check (if available)
    health_result = test_api_endpoint(
        f"{BASE_URL}/api/health",
        method="GET",
        headers=api_headers,
        description="💓 Testing Health Check Endpoint"
    )
    
    # Test 3: Try API endpoints without headers to see error handling
    print("\n" + "="*50)
    print("🔐 Testing API Security (without auth headers)")
    no_auth_result = test_api_endpoint(
        f"{BASE_URL}/api/logs",
        method="POST",
        data=test_log_data,
        headers={"Content-Type": "application/json"},
        description="Testing API without authentication"
    )
    
    # Test 4: Try with curl-like headers
    print("\n" + "="*50)
    curl_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    curl_result = test_api_endpoint(
        f"{BASE_URL}/api/logs",
        method="POST", 
        data=test_log_data,
        headers=curl_headers,
        description="📤 Testing with curl-style headers"
    )
    
    # Analysis and Results
    print("\n" + "="*60)
    print("📊 TEST RESULTS ANALYSIS")
    print("="*60)
    
    if log_result == "auth_required":
        print("⚠️  Web authentication is enabled on the deployment")
        print("🔍 This affects web browser access but may not affect API calls")
        print("📡 APIs might still work with proper programmatic requests")
    elif log_result and log_result != "auth_required":
        print("✅ Direct API calls are working!")
        print("🎉 Backend is fully functional for antivirus integration")
    else:
        print("❌ API calls are not working as expected")
        print("🔧 May need to investigate further or adjust configuration")
    
    print(f"\n🌐 Backend URL: {BASE_URL}")
    print(f"🔑 API Key: {API_KEY}")
    print(f"📡 Primary Endpoint: {BASE_URL}/api/logs")
    
    print("\n📋 NEXT STEPS:")
    if log_result and log_result != "auth_required":
        print("1. ✅ Backend is ready for antivirus integration")
        print("2. 🔧 Configure your antivirus with the backend URL and API key")
        print("3. 📝 Test log submission from your antivirus system")
    else:
        print("1. 🔍 Verify API endpoint configuration")
        print("2. 🔧 Check if middleware or authentication is blocking API calls")
        print("3. 📞 Consider contacting deployment platform support")
    
    return log_result

if __name__ == "__main__":
    test_direct_api_calls()