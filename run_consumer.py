from app.consumer.consumer import ConsumerService
from app.common.config import BOOTSTRAP_SERVERS, CONSUMER_GROUP, SENSOR_TOPIC
from app.processing.processor import EventProcessor

if __name__ == "__main__":
    consumer = ConsumerService(bootstrap_servers=BOOTSTRAP_SERVERS, topic=SENSOR_TOPIC, group_id=CONSUMER_GROUP)
    consumer.connect()
    processor = EventProcessor()
    try:
        for event in consumer.consume_events():
            processor.process_event(event)
    finally:
        processor.close()
    
    
