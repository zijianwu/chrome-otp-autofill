from chrome_otp_autofill.message_watcher import MessageWatcher
from chrome_otp_autofill.code_extractor import CodeExtractor
from chrome_otp_autofill.chrome_extension.extension import ChromeExtension

def main():
    watcher = MessageWatcher()
    extractor = CodeExtractor()
    chrome_extension = ChromeExtension()

    # Start watching for new messages
    watcher.watch_for_new_messages(
        callback=lambda message: process_message(message, extractor, chrome_extension)
    )

def process_message(message, extractor, chrome_extension):
    # Extract potential 2FA code
    print(message)
    code = extractor.extract_code(message)
    if code:
        # Send code to Chrome extension for autofill
        chrome_extension.send_code_to_browser(code)

if __name__ == "__main__":
    main()
