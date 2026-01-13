# Configuration file for ML DevOps App

# Application Settings
DEBUG = False
TESTING = False
JSON_SORT_KEYS = False

# CORS Configuration
CORS_ORIGINS = ["*"]  # Restrict in production

# Model Configuration
MODEL_PATH = "models/iris_model.pkl"
SCALER_PATH = "models/scaler.pkl"
AUTO_TRAIN_ON_STARTUP = True

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "logs/app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Feature Configuration
FEATURE_NAMES = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]
CLASS_NAMES = ["Setosa", "Versicolor", "Virginica"]
N_FEATURES = 4
N_CLASSES = 3

# Performance Settings
WORKERS = 4
THREAD_POOL_SIZE = 10
TIMEOUT = 30

# Security
RATE_LIMIT_ENABLED = False
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60

# Monitoring
HEALTH_CHECK_INTERVAL = 30  # seconds
METRICS_ENABLED = True
TRACE_ENABLED = False
