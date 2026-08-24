from datetime import datetime, timezone

def parse_pfsense_log(raw_message: str) -> dict:
    """Parses raw pfSense firewall logs into a normalized schema."""
    # Example format: "pfsense: filterlog: pass,in,4,tcp,192.168.1.50,10.0.0.1,high"
    parts = raw_message.split(",")
    
    src_ip = parts[4].strip() if len(parts) > 4 else "0.0.0.0"
    dst_ip = parts[5].strip() if len(parts) > 5 else "0.0.0.0"
    severity = parts[6].strip() if len(parts) > 6 else "medium"

    return {
        "timestamp": datetime.now(timezone.utc),
        "source_ip": src_ip,
        "destination_ip": dst_ip,
        "event_type": "firewall_block" if "block" in raw_message.lower() else "firewall_pass",
        "severity": severity,
        "raw_message": raw_message,
        "parsed_data": {"format": "pfsense", "action": parts[0] if parts else "unknown"}
    }