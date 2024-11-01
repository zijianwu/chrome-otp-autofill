from flask import Flask, request

app = Flask(__name__)

@app.route('/receive_code', methods=['POST'])
def receive_code():
    code = request.json.get("code")
    print(code)
    if code:
        # Send message to Chrome extension
        return "Code received", 200
    return "No code found", 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)