from chrome_otp_autofill.code_extractor import CodeExtractor

def test_extract_code():
    extractor = CodeExtractor()
    message = "Your 2FA code is 123456."
    assert extractor.extract_code(message) == "123456"