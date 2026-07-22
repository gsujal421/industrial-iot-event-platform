from app.common.event import SensorEvent
import pandas as pd
from dataclasses import asdict
from pathlib import Path

class StorageService:

    def __init__(self,output_path: str):
        self.output_path= Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def store(self, event: SensorEvent):
        event_dict = asdict(event)
        event_dict['timestamp']= event_dict['timestamp'].isoformat()
        df= pd.DataFrame([event_dict])

        if self.output_path.exists():
            existing_df = pd.read_parquet(self.output_path, engine='pyarrow')
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_parquet(self.output_path, engine='pyarrow', index=False)
            print(f"Appended Event {event.event_id} to {self.output_path} successfully")
        
        else:
            df.to_parquet(self.output_path, engine='pyarrow', index=False)
            print(f"Stored Event {event.event_id} in {self.output_path} successfully")
        
