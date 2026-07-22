from app.common.event import SensorEvent
from app.validation.status import ValidationStatus


class Validator:
    def validate(self, event: SensorEvent) -> ValidationStatus:
        if self.is_invalid(event):
            return ValidationStatus.Invalid
        if self.is_critical(event):
            return ValidationStatus.Critical
        return ValidationStatus.Valid

    def is_invalid(self, event: SensorEvent) -> bool:
        return len(self.get_invalid_reasons(event)) > 0

    def get_invalid_reasons(self, event: SensorEvent) -> list[str]:
        reasons = []
        allowed_statuses = {
            "running",
            "idle",
            "maintenance", 
        }
        if event.event_id is None:
            reasons.append("Missing event_id")

        if event.timestamp is None:
            reasons.append("Missing timestamp")

        if event.machine_id is None:
            reasons.append("Missing machine_id")

        if event.machine_status is None:
            reasons.append("Missing machine_status")

        # Machine status
        if event.machine_status not in allowed_statuses:
            reasons.append(f"Unknown machine status: {event.machine_status}")

        # Telemetry values
        if event.temperature is None:
            reasons.append("Missing temperature")

        if event.vibration is None:
            reasons.append("Missing vibration")

        if event.humidity is None:
            reasons.append("Missing humidity")

        if event.pressure is None:
            reasons.append("Missing pressure")

        if event.energy_consumption is None:
            reasons.append("Missing energy consumption")

        if event.temperature is not None:
            if event.temperature < -40 or event.temperature > 200:
                reasons.append("Temperature out of range")

        if event.vibration is not None:
            if event.vibration < 0 or event.vibration > 100:
                reasons.append("Vibration out of range")

        if event.pressure is not None:
            if event.pressure < 1 or event.pressure > 5:
                reasons.append("Pressure out of range")

        if event.humidity is not None:
            if event.humidity < 0 or event.humidity > 100:
                reasons.append("Humidity out of range")

        if event.energy_consumption is not None:
            if event.energy_consumption < 0 or event.energy_consumption > 10000:
                reasons.append("Energy consumption out of range")

        return reasons

    def is_critical(self, event: SensorEvent) -> bool:
        return len(self.get_critical_reasons(event)) > 0

    def get_critical_reasons(self, event: SensorEvent) -> list[str]:

        reasons = []

        if event.temperature >= 85:
            reasons.append("High temperature")

        if event.vibration >= 70:
            reasons.append("High vibration")

        if event.pressure <= 1.5:
            reasons.append("Low pressure")

        return reasons