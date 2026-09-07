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
│   ├── index.html, scan.html, dashboard.html, history.html, about.html
│   ├── css/style.css
│   └── js/main.js, scan.js, dashboard.js
└── requirements.txt
```

## Run it locally

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Start the backend (from the `backend/` folder):
   ```
   cd backend
   python app.py
   ```
   This runs on `http://127.0.0.1:5000` and creates `database/h2s.db` and an
   `uploads/` folder automatically.

3. Open the frontend: just open `frontend/index.html` in your browser
   (or serve the `frontend/` folder with any static file server). The pages
   call the API at `http://127.0.0.1:5000`, so keep the backend running.

## Deploying for real

This project ships ready to deploy on **Render** (see the step-by-step guide
in chat). Key things already set up for you:

- `backend/app.py` binds to `0.0.0.0` and reads the `PORT` environment
  variable (Render sets this automatically) instead of hardcoding
  `127.0.0.1:5000`, and `debug` is off.
- `requirements.txt` includes `gunicorn` (production server) and
  `opencv-python-headless` (lighter, server-friendly build of OpenCV).

After deploying the backend, update the frontend's `fetch()` URLs
(`frontend/js/scan.js`, `frontend/js/dashboard.js`, `frontend/history.html`)
from `http://127.0.0.1:5000` to your live backend URL, and tighten
`CORS(app)` in `app.py` to your frontend's real domain once you have it.

## Note on the prediction model

`ai/predictor.py` currently uses a simple placeholder formula based on the
strip's average saturation/value (HSV). For real accuracy you'd want to
calibrate this against your actual reference color chart (time vs. exposure)
rather than a linear formula.
