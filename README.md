# Chrome OTP Autofill

## Installation Instructions

### Setting up the Development Environment

1. Clone the repository:
   ```sh
   git clone https://github.com/zijianwu/chrome-otp-autofill.git
   cd chrome-otp-autofill
   ```

2. Install dependencies using Poetry:
   ```sh
   poetry install
   ```

## Running the Server

1. Start the Flask server:
   ```sh
   poetry run python chrome_otp_autofill/chrome_extension/server.py
   ```

## Adding the Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable "Developer mode" by toggling the switch in the top right corner.
3. Click on "Load unpacked" and select the `chrome_otp_autofill/chrome_extension` directory.

## Usage Instructions

1. Start the tool by running the main script:
   ```sh
   poetry run python chrome_otp_autofill/main.py
   ```

2. The tool will watch for new messages and extract potential 2FA codes.

3. When a 2FA code is detected, it will be sent to the Chrome extension for autofill.

4. The Chrome extension will autofill the 2FA code in the appropriate input fields on the web page.
