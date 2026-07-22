from dataclasses import asdict, is_dataclass
import json
from kafka import KafkaProducer


class ProducerService:
    def __init__(self, bootstrap_servers:str, topic:str):
        self.bootstrap_servers= bootstrap_servers
        self.topic= topic
        self.producer= None
    
    def serialize_payload(self, payload):
        if is_dataclass(payload):
            payload = asdict(payload)

        def json_default(value):
            if hasattr(value, "isoformat"):
                return value.isoformat()
            raise TypeError(f"Cannot serialize {type(value).__name__} to JSON")

        return json.dumps(payload, default=json_default).encode("utf-8")
        
    def connect(self):
        self.producer= KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        print(f"Connected to Kafka at {self.bootstrap_servers}")

    def send_event(self, sensor_event):
        return self.send_payload(sensor_event)

    def send_payload(self, payload):
        if self.producer is None:
            raise RuntimeError("Producer is not connected. Call connect() first.")
        event_bytes = self.serialize_payload(payload)
        future = self.producer.send(self.topic, event_bytes)
        future.get(timeout=10)
        print(f"Sent event to topic {self.topic}: {event_bytes}")

    def close(self):
        if self.producer is not None:
            self.producer.flush(timeout=10)
            self.producer.close()
            self.producer = None
