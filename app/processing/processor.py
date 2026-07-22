from app.common.config import (
    ALERT_TOPIC,
    BOOTSTRAP_SERVERS,
    DLQ_TOPIC,
    PROCESSED_HISTORY_PATH,
    SENSOR_TOPIC,
)
from app.common.event import SensorEvent
from app.services.alert import AlertService
from app.services.dlq import DLQService
from app.services.storage import StorageService
from app.validation.status import ValidationStatus
from app.validation.validator import Validator


class EventProcessor:
    def __init__(self):
        self.validator = Validator()
        self.dlq = DLQService(bootstrap_servers=BOOTSTRAP_SERVERS, dlq_topic=DLQ_TOPIC)
        self.alert = AlertService(bootstrap_server=BOOTSTRAP_SERVERS, alert_topic=ALERT_TOPIC)
        self.storage = StorageService(output_path=PROCESSED_HISTORY_PATH)

    def process_event(self, event: SensorEvent) -> ValidationStatus:
        invalid_reasons = self.validator.get_invalid_reasons(event)
        if invalid_reasons:
            self.dlq.send(event, reason="; ".join(invalid_reasons), source_topic=SENSOR_TOPIC)
            return ValidationStatus.Invalid

        critical_reasons = self.validator.get_critical_reasons(event)
        if critical_reasons:
            self.alert.send(event, reason="; ".join(critical_reasons), source_topic=SENSOR_TOPIC)
            self.storage.store(event)
            return ValidationStatus.Critical

        self.storage.store(event)
        return ValidationStatus.Valid

    def close(self):
        self.dlq.close()
        self.alert.close()
