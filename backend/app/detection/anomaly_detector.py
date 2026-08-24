from collections import deque
from datetime import datetime, timezone
import numpy as np

class AnomalyDetector:
    def __init__(self, window_size: int = 20):
        # Keeps timestamp history per IP address
        self.ip_histories: dict[str, deque] = {}
        self.window_size = window_size

    def track_and_check(self, ip: str, timestamp: datetime) -> bool:
        if ip not in self.ip_histories:
            self.ip_histories[ip] = deque(maxlen=self.window_size)
            
        history = self.ip_histories[ip]
        history.append(timestamp.timestamp())

        if len(history) < 5:
            return False  # Not enough data points to compute baseline standard deviation

        # Calculate connection intervals in seconds
        intervals = np.diff(list(history))
        if len(intervals) < 2:
            return False

        mean = float(np.mean(intervals))
        std = float(np.std(intervals))

        if std == 0:
            return False

        current_interval = intervals[-1]
        # Flag if interval frequency is > 3 standard deviations from rolling mean
        return abs(current_interval - mean) > (3 * std)

anomaly_detector = AnomalyDetector()    