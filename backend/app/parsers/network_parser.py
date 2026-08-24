from datetime import datetime, timezone

def parse_network_log(raw_message: str) -> dict:
    """Parses general network traffic logs."""
    parts = raw_message.split(" ")
    
    src_ip = parts[0] if len(parts) > 0 else "0.0.0.0"
    dst_ip = parts[1] if len(parts) > 1 else "0.0.0.0"

    return {
        "timestamp": datetime.now(timezone.utc),
        "source_ip": src_ip,
        "destination_ip": dst_ip,
        "event_type": "network_connection",
        "severity": "low",
        "raw_message": raw_message,
        "parsed_data": {"format": "network_traffic"}
    }