from kafka import KafkaConsumer
import json
from datetime import datetime
from app.common.event import SensorEvent


class ConsumerService:
    def __init__(self, bootstrap_servers: str, 
                 topic: str,
                 group_id: str):
        self.bootstrap_servers= bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
    
    def connect(self):
        self.consumer= KafkaConsumer(bootstrap_servers= self.bootstrap_servers,group_id= self.group_id,auto_offset_reset= 'earliest',
                 api_version=(3,7,0))
        print(f"Connected to Kafka at {self.bootstrap_servers} with group_id {self.group_id}")
        self.consumer.subscribe([self.topic])
        print(f"Subscribed to topic {self.topic}")

    def deserialize_event(self, event_bytes):
        event_json = event_bytes.decode('utf-8')
        event_dict = json.loads(event_json)
        return SensorEvent(
            event_id= event_dict['event_id'],
            timestamp= datetime.fromisoformat(event_dict['timestamp']),
            machine_id= event_dict['machine_id'],
            temperature= event_dict['temperature'],
            vibration= event_dict['vibration'],
            humidity= event_dict['humidity'],
            pressure= event_dict['pressure'],
            energy_consumption= event_dict['energy_consumption'],
            machine_status= event_dict['machine_status']

            )

    def consume_events(self):
        if self.consumer is None:
            raise RuntimeError("Consumer is not connected. Call connect() first.")
        try:
            for message in self.consumer:
                event = self.deserialize_event(message.value)
                yield event
        finally:
            self.consumer.close()
            print("Consumer connection closed.")
    



