import requests, time, statistics

urls = ["http://localhost:5000/ping", "http://localhost:5001/ping"]
lat = []
for i in range(20):
    url = urls[i % len(urls)]
    t0 = time.perf_counter()
    r = requests.get(url, timeout=3)
    dt = (time.perf_counter() - t0) * 1000
    lat.append(dt)
    print(f"{i:02d}", url, r.json(), f"{dt:.1f} ms")

lat.sort()
p95 = lat[int(len(lat)*0.95)-1]
print(f"avg={statistics.mean(lat):.1f} ms, p95={p95:.1f} ms")
