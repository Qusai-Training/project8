from datetime import datetime, timezone
import json

def parse_simulated_log(raw_message: str) -> dict:
    """Parses simulated JSON or key-value test log payloads."""
    try:
        data = json.loads(raw_message)
        return {
            "timestamp": datetime.now(timezone.utc),
            "source_ip": data.get("src_ip", "10.0.0.50"),
            "destination_ip": data.get("dst_ip", "10.0.0.1"),
            "event_type": data.get("event_type", "simulated_event"),
            "severity": data.get("severity", "medium"),
            "raw_message": raw_message,
            "parsed_data": data
        }
    except json.JSONDecodeError:
        return {
            "timestamp": datetime.now(timezone.utc),
            "source_ip": "10.0.0.50",
            "destination_ip": "10.0.0.1",
            "event_type": "simulated_event",
            "severity": "low",
            "raw_message": raw_message,
            "parsed_data": {"format": "simulated_raw"}
        }