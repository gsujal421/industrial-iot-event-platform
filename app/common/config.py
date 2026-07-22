# Kafka Configuration
BOOTSTRAP_SERVERS = "localhost:9092"

# Kafka Topics
SENSOR_TOPIC = "iot.sensor.data"
ALERT_TOPIC = "iot.sensor.alerts"
DLQ_TOPIC = "iot.sensor.dlq"

# Source dataset machine-status codes
STATUS_MAP = {
    0: "running",
    1: "idle",
    2: "maintenance",

}
# Consumer
CONSUMER_GROUP = "sensor-consumer-group"

# Data paths
SOURCE_DATA_PATH = "data/smart_manufacturing_data.csv"
PROCESSED_HISTORY_PATH = "data/processed_events.parquet"

# Dataset-specific validation thresholds. Pressure is expressed in bar and
# vibration uses the source dataset's 0–120 scale.
MIN_VIBRATION = 0
MAX_VIBRATION = 120
MIN_PRESSURE = 1
MAX_PRESSURE = 5
CRITICAL_VIBRATION = 80
CRITICAL_LOW_PRESSURE = 1.2

# Simulation
SIMULATION_DELAY = 1
