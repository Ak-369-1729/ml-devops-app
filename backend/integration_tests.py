#!/usr/bin/env python3
"""
Integration tests for ML DevOps app
Tests API endpoints and overall system functionality
"""

import requests
import json
import time
from typing import Dict, Any

class APITester:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.results = []
    
    def test_health(self) -> bool:
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'healthy'
            print("✓ Health check passed")
            return True
        except Exception as e:
            print(f"✗ Health check failed: {e}")
            return False
    
    def test_model_info(self) -> bool:
        """Test model info endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/model/info", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['model_type'] == 'RandomForestClassifier'
            assert len(data['classes']) == 3
            print("✓ Model info passed")
            return True
        except Exception as e:
            print(f"✗ Model info failed: {e}")
            return False
    
    def test_prediction(self, features: list, expected_class: str) -> bool:
        """Test prediction endpoint"""
        try:
            payload = {'features': features}
            response = requests.post(
                f"{self.base_url}/api/predict",
                json=payload,
                timeout=5
            )
            assert response.status_code == 200
            data = response.json()
            
            assert 'prediction' in data
            assert 'class' in data
            assert 'confidence' in data
            assert 'probabilities' in data
            
            print(f"✓ Prediction test passed: {data['class']} (confidence: {data['confidence']:.2%})")
            return True
        except Exception as e:
            print(f"✗ Prediction test failed: {e}")
            return False
    
    def test_invalid_input(self) -> bool:
        """Test error handling with invalid input"""
        try:
            payload = {'features': [1.0, 2.0]}  # Only 2 features instead of 4
            response = requests.post(
                f"{self.base_url}/api/predict",
                json=payload,
                timeout=5
            )
            assert response.status_code == 400
            print("✓ Invalid input handling passed")
            return True
        except Exception as e:
            print(f"✗ Invalid input test failed: {e}")
            return False
    
    def test_latency(self) -> bool:
        """Test API response latency"""
        try:
            start = time.time()
            payload = {'features': [5.1, 3.5, 1.4, 0.2]}
            response = requests.post(
                f"{self.base_url}/api/predict",
                json=payload,
                timeout=5
            )
            latency = (time.time() - start) * 1000
            
            assert response.status_code == 200
            assert latency < 1000  # Less than 1 second
            print(f"✓ Latency test passed: {latency:.1f}ms")
            return True
        except Exception as e:
            print(f"✗ Latency test failed: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all tests"""
        print("\n🧪 Running Integration Tests...\n")
        
        tests = [
            ("Health Check", self.test_health),
            ("Model Info", self.test_model_info),
            ("Prediction - Setosa", lambda: self.test_prediction([5.1, 3.5, 1.4, 0.2], "Setosa")),
            ("Prediction - Versicolor", lambda: self.test_prediction([7.0, 3.2, 4.7, 1.4], "Versicolor")),
            ("Prediction - Virginica", lambda: self.test_prediction([6.3, 3.3, 6.0, 2.5], "Virginica")),
            ("Invalid Input Handling", self.test_invalid_input),
            ("API Latency", self.test_latency),
        ]
        
        passed = 0
        for name, test_func in tests:
            print(f"\n{name}:")
            if test_func():
                passed += 1
        
        print(f"\n\n📊 Results: {passed}/{len(tests)} tests passed")
        return passed == len(tests)

if __name__ == "__main__":
    import sys
    
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
