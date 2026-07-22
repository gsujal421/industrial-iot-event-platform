from app.producer.producer import ProducerService
from app.simulator.sensor_simulator import SensorSimulator
from app.common.config import BOOTSTRAP_SERVERS, SENSOR_TOPIC, SIMULATION_DELAY, SOURCE_DATA_PATH


def main():
    producer = ProducerService(bootstrap_servers=BOOTSTRAP_SERVERS, topic=SENSOR_TOPIC)
    producer.connect()
    
    try:
        simulator = SensorSimulator(csv_path=SOURCE_DATA_PATH, delay=SIMULATION_DELAY)
        simulator.load_data()

        for sensor_event in simulator.generate_events():
            producer.send_event(sensor_event)
    finally:
        producer.close()

if __name__ == "__main__":
    main()
