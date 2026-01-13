"""
Unit tests for ML DevOps application
"""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestMLDevOpsApp(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.client = self.app.test_client()
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('model_loaded', data)
    
    def test_model_info_endpoint(self):
        """Test model info endpoint"""
        response = self.client.get('/api/model/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['model_type'], 'RandomForestClassifier')
        self.assertEqual(len(data['classes']), 3)
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = self.client.get('/api/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
        self.assertIn('model_status', data)
    
    def test_predict_valid_input(self):
        """Test prediction with valid input"""
        payload = {
            'features': [5.1, 3.5, 1.4, 0.2]
        }
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('prediction', data)
        self.assertIn('class', data)
        self.assertIn('confidence', data)
        self.assertIn('probabilities', data)
        self.assertIsInstance(data['confidence'], float)
        self.assertGreaterEqual(data['confidence'], 0)
        self.assertLessEqual(data['confidence'], 1)
    
    def test_predict_missing_features(self):
        """Test prediction with missing features"""
        payload = {}
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_predict_wrong_feature_count(self):
        """Test prediction with wrong number of features"""
        payload = {
            'features': [5.1, 3.5, 1.4]  # Only 3 features instead of 4
        }
        response = self.client.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
    
    def test_cors_headers(self):
        """Test CORS headers"""
        response = self.client.get('/health')
        self.assertIn('Access-Control-Allow-Origin', response.headers)

if __name__ == '__main__':
    unittest.main()
