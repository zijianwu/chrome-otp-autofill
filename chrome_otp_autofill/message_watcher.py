import sqlite3
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CHAT_DB_PATH = os.path.expanduser("~/Library/Messages/chat.db")

class MessageWatcher:
    def __init__(self):
        self.observer = Observer()

    def watch_for_new_messages(self, callback):
        event_handler = MessageEventHandler(callback)
        self.observer.schedule(event_handler, os.path.dirname(CHAT_DB_PATH), recursive=False)
        self.observer.start()
        self.observer.join()

class MessageEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if event.src_path == CHAT_DB_PATH:
            message = self.get_latest_message()
            if message:
                self.callback(message)

    def get_latest_message(self):
        conn = sqlite3.connect(CHAT_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT text FROM message ORDER BY ROWID DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None