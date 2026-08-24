from datetime import datetime, timezone, timedelta
from app.detection.blacklist import blacklist_manager
from app.detection.scoring import calculate_threat_score
from app.detection.anomaly_detector import anomaly_detector

# Track authentication attempts per IP (IP -> list of timestamps)
failed_login_tracker: dict[str, list[datetime]] = {}

def evaluate_threats(parsed_log: dict) -> dict | None:
    weights = []
    reasons = []
    src_ip = parsed_log.get("source_ip", "")
    event_type = parsed_log.get("event_type", "")
    now = datetime.now(timezone.utc)

    # 1. Blacklisted IP Rule (+50)
    if blacklist_manager.is_blacklisted(src_ip):
        weights.append(50)
        reasons.append(f"Connection from blacklisted IP: {src_ip}")

    # 2. Authentication Rule (≥5 failed logins in 1 min) (+30)
    if event_type == "failed_login":
        if src_ip not in failed_login_tracker:
            failed_login_tracker[src_ip] = []
        
        # Keep attempts within the last 60 seconds
        cutoff = now - timedelta(seconds=60)
        failed_login_tracker[src_ip] = [t for t in failed_login_tracker[src_ip] if t > cutoff]
        failed_login_tracker[src_ip].append(now)

        if len(failed_login_tracker[src_ip]) >= 5:
            weights.append(30)
            reasons.append("Multiple failed login attempts threshold reached (≥5 in 1 min)")

    # 3. Repeated Firewall Block Rule (+20)
    if event_type == "firewall_block":
        weights.append(20)
        reasons.append("Firewall block event detected")

    # 4. Anomaly Detection (+40 for 3-sigma anomaly)
    if anomaly_detector.track_and_check(src_ip, parsed_log.get("timestamp", now)):
        weights.append(40)
        reasons.append("Unusual connection frequency pattern (3-sigma statistical anomaly)")

    if not weights:
        return None  # No threats detected

    score, severity_band = calculate_threat_score(weights)
    
    return {
        "threat_type": severity_band,
        "threat_score": score,
        "description": " | ".join(reasons)
    }