import gps
import requests
import json
import time

# Set up the GPS module
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# Cloud server endpoint
CLOUD_ENDPOINT = "http://your-cloud-server.com/api/upload"
DEVICE_ID = "your_device_id"  # Unique identifier for the device

while True:
    try:
        report = session.next()
        # Wait for a 'TPV' report and get the GPS data
        if report['class'] == 'TPV':
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                data = {
                    "device_id": DEVICE_ID,
                    "latitude": report.lat,
                    "longitude": report.lon,
                    "timestamp": time.time()
                }

                # Send data to the cloud server
                response = requests.post(CLOUD_ENDPOINT, json=data)
                print(f"Data sent: {data} - Status Code: {response.status_code}")

    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print("GPSD has terminated")
