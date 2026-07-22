from dataclasses import asdict
from app.common.event import SensorEvent
from app.producer.producer import ProducerService

class DLQService:

    def __init__(self,bootstrap_servers: str, dlq_topic: str):
        self.producer= ProducerService(
            bootstrap_servers= bootstrap_servers,
            topic= dlq_topic
        )
        self.producer.connect()

    def send(self, event: SensorEvent, reason: str, source_topic: str):
        self.producer.send_payload({
            "event": asdict(event),
            "reason": reason,
            "source_topic": source_topic,
            "validation_status": "invalid",
        })
        print(f"DLQ event {event.event_id} published: {reason}")

    def close(self):
        self.producer.close()
