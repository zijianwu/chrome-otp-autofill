import re

class CodeExtractor:
    def __init__(self):
        # Regular expression for finding 2FA codes (e.g., six-digit numbers)
        self.code_pattern = re.compile(r'\b\d{6}\b')

    def extract_code(self, message):
        match = self.code_pattern.search(message)
        return match.group(0) if match else None