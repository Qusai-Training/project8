from app.parsers.pfsense_parser import parse_pfsense_log
from app.parsers.auth_log_parser import parse_auth_log
from app.parsers.network_parser import parse_network_log
from app.parsers.simulated_parser import parse_simulated_log

def parse_log(raw_message: str, force_format: str = "auto") -> dict:
    """Auto-detects format if set to 'auto', otherwise routes to specific parser."""
    msg_lower = raw_message.lower()

    if force_format == "pfsense" or "pfsense" in msg_lower or "filterlog" in msg_lower:
        return parse_pfsense_log(raw_message)
    elif force_format == "auth" or "sshd" in msg_lower or "failed password" in msg_lower or "sudo" in msg_lower:
        return parse_auth_log(raw_message)
    elif force_format == "simulated" or msg_lower.startswith("{"):
        return parse_simulated_log(raw_message)
    else:
        return parse_network_log(raw_message)