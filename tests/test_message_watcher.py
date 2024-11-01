import sqlite3
import pytest
from unittest.mock import patch, MagicMock
from chrome_otp_autofill.message_watcher import MessageWatcher, MessageEventHandler, CHAT_DB_PATH
from watchdog.events import FileModifiedEvent
import os

def test_get_live_connection_latest_messages():
    # Connect to chat.db and retrieve the last 5 messages
    conn = sqlite3.connect(CHAT_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM message ORDER BY ROWID DESC LIMIT 5")
    results = cursor.fetchall()
    conn.close()

    # Print the last 5 messages
    latest_messages = [result[0] for result in results] if results else []
    print("Last 5 messages:", latest_messages)

    # Check that there are 5 messages
    assert len(latest_messages) == 5, "There should be 5 messages."

@pytest.fixture
def message_watcher():
    return MessageWatcher()

@pytest.fixture
def callback_mock():
    return MagicMock()

@pytest.fixture
def event_handler(callback_mock):
    return MessageEventHandler(callback_mock)

def test_message_event_handler_init(event_handler, callback_mock):
    # Verify the callback is set correctly in the event handler
    assert event_handler.callback == callback_mock

@patch('chrome_otp_autofill.message_watcher.sqlite3.connect')
def test_get_latest_message(mock_connect, event_handler):
    # Mock the database connection and cursor
    mock_cursor = mock_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = ("Your OTP code is 123456",)

    # Test get_latest_message retrieves the correct message
    message = event_handler.get_latest_message()
    assert message == "Your OTP code is 123456"

    # Verify database interaction
    mock_connect.assert_called_once_with(CHAT_DB_PATH)
    mock_cursor.execute.assert_called_once_with("SELECT text FROM message ORDER BY ROWID DESC LIMIT 1")

@patch('chrome_otp_autofill.message_watcher.CHAT_DB_PATH', "/mock/path/to/chat.db")
def test_on_modified_triggers_callback(event_handler, callback_mock):
    # Simulate a modification event at the mock path
    event = FileModifiedEvent(src_path="/mock/path/to/chat.db")
    with patch.object(event_handler, 'get_latest_message', return_value="Test OTP message"):
        event_handler.on_modified(event)

    # Verify callback was called with the expected message
    callback_mock.assert_called_once_with("Test OTP message")

def test_on_modified_no_trigger(event_handler, callback_mock):
    # Simulate a modification event at an unrelated path
    event = FileModifiedEvent(src_path="/mock/path/to/other.db")
    event_handler.on_modified(event)

    # Verify callback was not called
    callback_mock.assert_not_called()

@patch("chrome_otp_autofill.message_watcher.Observer")
def test_watch_for_new_messages_starts_observer(mock_observer_class, callback_mock):
    # Create the mock observer instance
    mock_observer_instance = mock_observer_class.return_value
    
    # Instantiate MessageWatcher, which will use the mocked Observer
    message_watcher = MessageWatcher()
    
    # Call the watch_for_new_messages function
    message_watcher.watch_for_new_messages(callback_mock)
    
    # Assert that schedule was called with the correct arguments
    mock_observer_instance.schedule.assert_called_once()
    args, kwargs = mock_observer_instance.schedule.call_args
    assert args[1] == os.path.dirname(CHAT_DB_PATH)
    assert kwargs["recursive"] is False

    # Verify that observer.start() was called
    mock_observer_instance.start.assert_called_once()