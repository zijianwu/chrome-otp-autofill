import requests

class ChromeExtension:
    def __init__(self, host="http://localhost", port=5000):
        self.url = f"{host}:{port}/receive_code"

    def send_code_to_browser(self, code):
        requests.post(self.url, json={"code": code})