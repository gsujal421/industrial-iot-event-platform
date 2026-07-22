import pandas as pd
import uuid
import time
from app.common import event
from app.common.config import STATUS_MAP

class SensorSimulator:
    def __init__(self, csv_path:str, delay:float=1.0):
        self.csv_path= csv_path
        self.delay=delay
        self.data: pd.DataFrame | None = None

    def load_data(self):
        self.data = pd.read_csv(self.csv_path)
        # Temporary limit for validating the Kafka producer/consumer flow.
        self.data = self.data.head(100)
        print(f"loaded {len(self.data)} rows of sensor data.")
    
    def generate_events(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        for _, row in self.data.iterrows():
            status_code = int(row['machine_status'])
            try:
                machine_status = STATUS_MAP[status_code]
            except KeyError as exc:
                raise ValueError(
                    f"Unknown machine_status code {status_code}; expected one of {sorted(STATUS_MAP)}."
                ) from exc

            sensor_event = event.SensorEvent(
                event_id=str(uuid.uuid4()),
                timestamp=pd.to_datetime(row['timestamp']),
                machine_id=int(row['machine_id']),
                temperature=float(row['temperature']),
                vibration=float(row['vibration']),
                humidity=float(row['humidity']),
                pressure=float(row['pressure']),
                energy_consumption=float(row['energy_consumption']),
                machine_status=machine_status
            )
            yield sensor_event
            time.sleep(self.delay)
    
