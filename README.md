# SensaBand H₂S — Full-Stack Project

A passive colorimetric H₂S exposure wristband concept: upload a photo of the
test strip, and the backend estimates exposure (ppm) from the strip's color.

## Structure
```
fullstack-project/
├── ai/
│   └── predictor.py       # color extraction + exposure prediction (OpenCV)
├── backend/
│   ├── app.py             # Flask API (/api/h2s/scan, /api/h2s/history)
│   └── database.py        # SQLite storage
├── frontend/
│   └── sensaband-website-2.html # Connected demo frontend
├── arduino/
│   └── sensaband_esp32c3/        # ESP32-C3 + MQ-136 telemetry sketch
└── requirements.txt
```

## Run it locally

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Start the backend from the project root:
   ```
   python -m backend.app
   ```
   This runs on `http://127.0.0.1:5000` and creates `database/h2s.db` and an
   `uploads/` folder automatically.

3. In a second terminal, serve the frontend from the project root:
   ```
   python -m http.server 8000 --directory frontend
   ```

4. Open `http://127.0.0.1:8000/sensaband-website-2.html` and log in with the
   demo account `supervisor` / `demo123`. Use **Backend Scan** to upload an
   image to the Flask API and view saved results. Keep both servers running.

## Arduino / ESP32 telemetry

Open `arduino/sensaband_esp32c3/sensaband_esp32c3.ino` in Arduino IDE, select
an ESP32-C3 board, and set `WIFI_SSID`, `WIFI_PASSWORD`, and
`TELEMETRY_URL`. The URL must use the computer's LAN IP when the ESP32 is on
the same Wi-Fi network, for example `http://192.168.1.20:5000/api/telemetry`.

The sketch reads MQ-136 on GPIO 2 and battery voltage on GPIO 3, then sends
telemetry every five seconds. Read recent device readings at
`GET /api/telemetry`. The exposure conversion is a prototype formula and
must be calibrated against real MQ-136 measurements before safety use.

## Deploying for real

This project ships ready to deploy on **Render** (see the step-by-step guide
in chat). Key things already set up for you:

- `backend/app.py` binds to `0.0.0.0` and reads the `PORT` environment
  variable (Render sets this automatically) instead of hardcoding
  `127.0.0.1:5000`, and `debug` is off.
- `requirements.txt` includes `gunicorn` (production server) and
  `opencv-python-headless` (lighter, server-friendly build of OpenCV).

After deploying the backend, update the `API_BASE` value in
`frontend/sensaband-website-2.html` from `http://127.0.0.1:5000` to your live
backend URL, and tighten
`CORS(app)` in `app.py` to your frontend's real domain once you have it.

## Note on the prediction model

`ai/predictor.py` currently uses a simple placeholder formula based on the
strip's average saturation/value (HSV). For real accuracy you'd want to
calibrate this against your actual reference color chart (time vs. exposure)
rather than a linear formula.
