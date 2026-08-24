from datetime import datetime, timezone
import re

def parse_auth_log(raw_message: str) -> dict:
    """Parses system authentication logs (failed SSH/sudo attempts)."""
    # Regex match for IP extraction
    ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", raw_message)
    src_ip = ip_match.group(0) if ip_match else "127.0.0.1"
    
    is_failed = "failed" in raw_message.lower() or "invalid" in raw_message.lower()

    return {
        "timestamp": datetime.now(timezone.utc),
        "source_ip": src_ip,
        "destination_ip": "127.0.0.1",
        "event_type": "failed_login" if is_failed else "successful_login",
        "severity": "high" if is_failed else "low",
        "raw_message": raw_message,
        "parsed_data": {"format": "auth_log", "authentication_status": "failure" if is_failed else "success"}
    }