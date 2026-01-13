"""
ML DevOps Web App Backend
A production-ready Flask application with ML inference, logging, and monitoring
"""

import os
import json
import logging
import joblib
import numpy as np
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables for model and scaler
model = None
scaler = None
model_metadata = {}

def load_or_train_model():
    """Load existing model or train a new one"""
    global model, scaler, model_metadata
    
    model_path = 'models/iris_model.pkl'
    scaler_path = 'models/scaler.pkl'
    
    try:
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            logger.info("Loading existing model from disk")
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            model_metadata['source'] = 'disk'
        else:
            logger.info("Training new model")
            train_model()
            os.makedirs('models', exist_ok=True)
            joblib.dump(model, model_path)
            joblib.dump(scaler, scaler_path)
            model_metadata['source'] = 'training'
        
        model_metadata['loaded_at'] = datetime.now().isoformat()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading/training model: {str(e)}")
        train_model()

def train_model():
    """Train a simple ML model on sample iris data"""
    global model, scaler
    
    # Sample iris dataset
    X = np.array([
        [5.1, 3.5, 1.4, 0.2], [7.0, 3.2, 4.7, 1.4], [6.3, 3.3, 6.0, 2.5],
        [5.9, 3.0, 4.2, 1.5], [6.5, 3.0, 5.5, 1.8], [5.4, 3.9, 1.7, 0.4],
        [7.1, 3.0, 5.9, 2.1], [6.3, 2.9, 5.6, 1.8], [5.0, 3.4, 1.5, 0.2]
    ])
    y = np.array([0, 1, 2, 1, 2, 0, 2, 2, 0])
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_scaled, y)
    
    logger.info("Model trained successfully")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model is not None
    }), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    ML prediction endpoint
    Expected JSON: {"features": [5.1, 3.5, 1.4, 0.2]}
    """
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            logger.warning("Invalid request: missing features")
            return jsonify({'error': 'Missing features in request'}), 400
        
        features = np.array(data['features']).reshape(1, -1)
        
        if features.shape[1] != 4:
            logger.warning(f"Invalid feature count: {features.shape[1]}")
            return jsonify({'error': 'Expected 4 features'}), 400
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0].tolist()
        
        iris_classes = ['Setosa', 'Versicolor', 'Virginica']
        
        logger.info(f"Prediction made: class={iris_classes[prediction]}, confidence={max(probability):.4f}")
        
        return jsonify({
            'prediction': int(prediction),
            'class': iris_classes[prediction],
            'confidence': float(max(probability)),
            'probabilities': {
                iris_classes[i]: float(probability[i]) for i in range(3)
            },
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        'model_type': 'RandomForestClassifier',
        'n_estimators': 10,
        'classes': ['Setosa', 'Versicolor', 'Virginica'],
        'metadata': model_metadata
    }), 200

@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Get application metrics"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'model_status': 'loaded' if model is not None else 'not_loaded',
        'version': '1.0.0'
    }), 200

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.path}")
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting ML DevOps application")
    load_or_train_model()
    app.run(host='0.0.0.0', port=5000, debug=False)
