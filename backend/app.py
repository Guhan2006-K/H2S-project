from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys
import uuid


# Get main project folder
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# Allow Python to find backend and ai folders
sys.path.append(BASE_DIR)


# Database functions
from backend.database import (
    create_database,
    insert_scan,
    get_history
)


# AI prediction function
from ai.predictor import predict_h2s


# Create Flask application
app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app)


# Upload folder
UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER


# Create database when server starts
create_database()


# ------------------------------------------------
# HOME API
# ------------------------------------------------

@app.route("/")
def home():

    return jsonify({

        "project": "SensaBand H₂S",

        "project_id": "SIH16118",

        "status": "online",

        "message":
            "H₂S-SafeBand backend is running"

    })


# ------------------------------------------------
# SCAN API
# ------------------------------------------------

@app.route(
    "/api/h2s/scan",
    methods=["POST"]
)
def scan():

    try:

        # Receive image
        image = request.files.get(
            "image"
        )


        # Receive worker details
        worker_id = request.form.get(
            "worker_id",
            "SB-0000"
        )

        worker_name = request.form.get(
            "worker_name",
            "Unknown Worker"
        )


        # Check image
        if image is None:

            return jsonify({

                "success": False,

                "message":
                    "No image uploaded"

            }), 400


        # Get image extension
        extension = os.path.splitext(
            image.filename
        )[1]


        # Generate unique filename
        filename = (
            str(uuid.uuid4())
            + extension
        )


        # Complete image path
        image_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        # Save uploaded image
        image.save(
            image_path
        )


        # Send image to AI
        prediction = predict_h2s(
            image_path
        )


        # Save result into database
        insert_scan(

            worker_id,

            worker_name,

            prediction["exposure"],

            prediction["status"],

            prediction["confidence"],

            filename

        )


        # Send result to frontend
        return jsonify({

            "success": True,

            "worker_id":
                worker_id,

            "worker_name":
                worker_name,

            "exposure":
                prediction["exposure"],

            "unit":
                "ppm",

            "status":
                prediction["status"],

            "action":
                prediction["action"],

            "confidence":
                prediction["confidence"]

        })


    except Exception as error:

        print(error)

        return jsonify({

            "success": False,

            "message":
                str(error)

        }), 500


# ------------------------------------------------
# HISTORY API
# ------------------------------------------------

@app.route(
    "/api/h2s/history",
    methods=["GET"]
)
def history():

    data = get_history()

    return jsonify(data)


# ------------------------------------------------
# RUN SERVER
# ------------------------------------------------

if __name__ == "__main__":

    import os as _os

    app.run(

        host="0.0.0.0",

        port=int(_os.environ.get("PORT", 5000)),

        debug=False

    )