"""
Training script for ML model
Can be run manually to retrain the model
"""

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

def train_iris_model():
    """Train a Random Forest model on iris dataset"""
    
    print("Loading iris dataset...")
    iris = load_iris()
    X = iris.data
    y = iris.target
    
    print(f"Dataset shape: {X.shape}")
    print(f"Classes: {iris.target_names}")
    
    # Scale features
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_scaled, y)
    
    # Save model and scaler
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/iris_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    print("✓ Model saved to models/iris_model.pkl")
    print("✓ Scaler saved to models/scaler.pkl")
    
    # Feature importance
    print("\nFeature Importance:")
    for feature, importance in zip(iris.feature_names, model.feature_importances_):
        print(f"  {feature}: {importance:.4f}")
    
    # Test accuracy
    accuracy = model.score(X_scaled, y)
    print(f"\nTraining Accuracy: {accuracy:.4f}")
    
    return model, scaler

if __name__ == '__main__':
    train_iris_model()
