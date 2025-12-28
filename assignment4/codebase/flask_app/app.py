from flask import Flask, request, jsonify
import os
import signal
import sys
import threading

app = Flask(__name__)

shutting_down = False

@app.route('/')
def hello():
    # server_name = os.getenv('SERVER_NAME', 'Unknown Server')
    # return f'Hello from {server_name}!'
    
    if shutting_down:
        return "Server shutting down", 503
    
    pod_name = os.getenv('HOSTNAME', 'unknown-pod')
    pod_ip = os.getenv('POD_IP', 'unknown-ip')
    node_name = os.getenv('NODE_NAME', 'unknown-node')

    return (
        f'Hello! This is server in pod "{pod_name}" '
        f'(IP={pod_ip}) from node "{node_name}"!'
    )

@app.route('/chat/<username>')
def chat(username):
    institution = request.args.get('institution', 'unknown')
    return jsonify({
        "message": f"Hello {username} from {institution}!"
    })

def handle_sigterm(signum, frame):
    # print("Received SIGTERM, shutting down gracefully...")
    # sys.exit(0)
    global shutting_down
    print("SIGTERM received, stopping new requests...")
    shutting_down = True
    # allow in-flight requests to finish
    threading.Timer(5, sys.exit).start()

signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('FLASK_PORT', 5000)))
