import os
from app.config import settings

class BlacklistManager:
    def __init__(self):
        self.blacklisted_ips: set[str] = set()
        self.load_blacklist()

    def load_blacklist(self):
        file_path = settings.BLACKLIST_FILE_PATH
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.blacklisted_ips = {line.strip() for line in f if line.strip()}

    def is_blacklisted(self, ip: str) -> bool:
        return ip in self.blacklisted_ips

    def add_to_blacklist(self, ip: str):
        self.blacklisted_ips.add(ip)

blacklist_manager = BlacklistManager()