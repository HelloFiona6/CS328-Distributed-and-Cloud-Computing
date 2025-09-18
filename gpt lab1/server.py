from flask import Flask, jsonify
import os, socket, time, random

app = Flask(__name__)
START = time.time()
INSTANCE = f"{socket.gethostname()}:{os.getenv('PORT','5000')}"

@app.get("/ping")
def ping():
    jitter = float(os.getenv("JITTER_MS","0"))  # 用于模拟网络/负载抖动
    if jitter > 0:
        time.sleep(random.uniform(0, jitter)/1000.0)
    return jsonify(instance=INSTANCE, uptime=round(time.time()-START,2))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
