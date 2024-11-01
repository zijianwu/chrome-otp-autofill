import sqlite3
import pytest
from unittest.mock import patch, MagicMock
from chrome_otp_autofill.message_watcher import MessageWatcher, CHAT_DB_PATH

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

@patch('chrome_otp_autofill.message_watcher.sqlite3.connect')
def test_get_latest_message(mock_connect):
    # Create an instance of MessageWatcher with the mocked connection
    message_watcher = MessageWatcher()

    # Mock the database connection and cursor
    mock_cursor = mock_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = ("Your OTP code is 123456",)

    # Test get_latest_message retrieves the correct message
    message = message_watcher.get_latest_message()
    assert message == "Your OTP code is 123456"

    # Verify database interaction
    mock_cursor.execute.assert_called_once_with("SELECT text FROM message ORDER BY ROWID DESC LIMIT 1")

# @patch('chrome_otp_autofill.message_watcher.sqlite3.connect')
# def test_watch_for_new_messages_no_duplicates(mock_connect, message_watcher, callback_mock):
#     # Mock the database connection and cursor
#     mock_cursor = mock_connect.return_value.cursor.return_value
#     mock_cursor.fetchone.side_effect = [
#         ("Your OTP code is 123456",),
#         ("Your OTP code is 123456",),
#         ("Your OTP code is 654321",)
#     ]

#     # Run the watch_for_new_messages method in a separate thread or process
#     with patch('time.sleep', return_value=None):
#         message_watcher.watch_for_new_messages(callback_mock)

#     # Verify that the callback was called only for unique messages
#     assert callback_mock.call_count == 2
#     callback_mock.assert_any_call("Your OTP code is 123456")
#     callback_mock.assert_any_call("Your OTP code is 654321")
