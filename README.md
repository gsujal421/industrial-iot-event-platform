# Industrial IoT Event Streaming Platform

A real-time event streaming project built to understand the fundamentals of data engineering using Apache Kafka.

The project simulates industrial IoT sensor data, streams it through Kafka, validates every incoming event, and routes it based on its severity. Valid events are stored as historical records, critical events are published to a dedicated alert topic, and invalid events are redirected to a Dead Letter Queue (DLQ) for further inspection.

The primary goal of this project was to learn how streaming systems are designed and how different components work together while keeping the implementation simple, modular, and easy to understand.

---

## Architecture

```text

         Industrial IoT Event Streaming Platform

                     CSV Sensor Dataset
                             │
                             ▼
                    Sensor Simulator
                             │
                             ▼
                     Kafka Producer
                             │
                             ▼
              Kafka Topic (iot.sensor.data)
                             │
                             ▼
                     Kafka Consumer
                             │
                             ▼
                     Event Processor
                             │
                             ▼
                        Validator
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     Storage Service    Alert Service      DLQ Service
          │                  │                  │
          ▼                  ▼                  ▼
  Parquet History     iot.sensor.alerts   iot.sensor.dlq
            │
            ▼
  Amazon S3 Bucket
            │
            ▼
  AWS Glue Crawler
            │
            ▼
  AWS Glue Data Catalog
            │
            ▼
      Amazon Athena
            │
            ▼
      SQL Analytics

                     
```
---


## Features

- Simulates industrial IoT sensor events from a CSV dataset
- Streams events using Apache Kafka
- Serializes and deserializes custom event objects
- Validates incoming sensor data using business rules
- Routes critical events to a separate Kafka alert topic
- Sends invalid events to a Dead Letter Queue (DLQ)
- Stores processed events in Parquet format for historical analysis

---

## Tech Stack

- Python
- Apache Kafka
- Docker & Docker Compose
- Pandas
- PyArrow
- AWS S3
- AWS IAM
- AWS Glue
- Amazon Athena

---

## Project Structure

```text
industrial-iot-event-platform/

├── app/
│   ├── common/
│   ├── simulator/
│   ├── producer/
│   ├── consumer/
│   ├── processing/
│   ├── validation/
│   └── services/
│
├── data/
│   ├── smart_manufacturing_data/
│   ├── processed_events/
├── docker/
│   ├── docker-compose.yml/
├── run_producer.py
├── run_consumer.py
├── requirements.txt
└── README.md
```

---

## Processing Flow

1. Sensor data is loaded from a CSV dataset.
2. The simulator converts each row into a `SensorEvent`.
3. The producer serializes and publishes events to Kafka.
4. The consumer reads events from the Kafka topic.
5. The processor validates every event.
6. Based on the validation result:
   - **Valid** → Stored as historical data
   - **Critical** → Published to the Alert topic and stored
   - **Invalid** → Published to the Dead Letter Queue (DLQ)

---

## Validation Logic

Each incoming event is checked for:

- Required fields
- Machine status
- Temperature range
- Vibration range
- Pressure range
- Humidity range
- Energy consumption range

The validator classifies every event into one of three categories:

| Status | Action |
|--------|--------|
| **Valid** | Store the event |
| **Critical** | Send an alert and store the event |
| **Invalid** | Send the event to the Dead Letter Queue |

---

## Historical Data & AWS Integration

Processed events are stored locally as Parquet files.

As the next stage of the pipeline, these Parquet files are uploaded to an Amazon S3 bucket. An IAM policy is configured to allow AWS Glue to crawl the dataset and create the required metadata catalog. The processed data can then be queried using Amazon Athena, making it easy to perform SQL-based analysis without managing a database server.

This keeps the streaming pipeline independent from the analytics layer while preparing the data for downstream reporting and exploration.

---

## Running the Project

### 1. Start Kafka

```bash
docker compose up -d
```

### 2. Start the Consumer

```bash
python run_consumer.py
```

### 3. Start the Producer

```bash
python run_producer.py
```

### 4. Open Kafka UI

```
http://localhost:8081
```

You can monitor:

- `iot.sensor.data`
- `iot.sensor.alerts`
- `iot.sensor.dlq`

---

## Future Improvements

Some improvements I would like to add in the future:

- Automate downstream workflows using Apache Airflow
- Batch Parquet writes instead of writing every event individually
- Add structured logging and monitoring
- Store processed data directly in Amazon S3
- Build dashboards on top of Athena for monitoring sensor trends

---

## Author

**Sujal Gupta**

GitHub: https://github.com/gsujal421
