import sqlite3
import os
import time

CHAT_DB_PATH = os.path.expanduser("~/Library/Messages/chat.db")

class MessageWatcher:
    def __init__(self):
        self.conn = sqlite3.connect(CHAT_DB_PATH)
        self.cursor = self.conn.cursor()

    def watch_for_new_messages(self, callback):
        while True:
            message = self.get_latest_message()
            if message:
                callback(message)
            time.sleep(0.25)

    def get_latest_message(self):
        self.cursor.execute("SELECT text FROM message ORDER BY ROWID DESC LIMIT 1")
        result = self.cursor.fetchone()
        return result[0] if result else None
