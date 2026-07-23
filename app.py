from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():

    hostname = socket.gethostname()

    return f"""
    <h2>Python Application</h2>

    Running inside Kubernetes

    Pod : {hostname}
    """

@app.route("/health")

def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
