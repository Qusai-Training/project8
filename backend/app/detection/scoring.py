def calculate_threat_score(weights: list[int]) -> tuple[float, str]:
    """Calculates cumulative score capped at 100 and assigns severity band."""
    total_score = float(min(100, sum(weights)))
    
    if total_score >= 81:
        severity = "Critical"
    elif total_score >= 61:
        severity = "High"
    elif total_score >= 31:
        severity = "Medium"
    else:
        severity = "Low"
        
    return total_score, severity