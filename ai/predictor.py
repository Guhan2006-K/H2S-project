import cv2
import numpy as np


def extract_color(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image")

    # Resize image
    image = cv2.resize(image, (300, 300))

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Take center portion of the image
    center = hsv[100:200, 100:200]

    # Calculate average HSV values
    average_hsv = np.mean(center, axis=(0, 1))

    h = float(average_hsv[0])
    s = float(average_hsv[1])
    v = float(average_hsv[2])

    return {
        "h": round(h, 2),
        "s": round(s, 2),
        "v": round(v, 2)
    }


def predict_h2s(image_path):

    color = extract_color(image_path)

    h = color["h"]
    s = color["s"]
    v = color["v"]

    # Prototype H2S exposure estimation
    exposure = ((s / 255) * 10) + ((v / 255) * 5)

    exposure = round(max(0, exposure), 1)

    # Determine safety status
    if exposure < 5:
        status = "SAFE"
        action = "Continue monitoring"

    elif exposure < 10:
        status = "WARNING"
        action = "Move to a safe area and use appropriate PPE"

    else:
        status = "DANGER"
        action = "Evacuate the area and follow emergency procedures"

    # Prototype confidence value
    confidence = round(
        90 + (min(exposure, 10) / 10) * 8,
        1
    )

    return {
        "exposure": exposure,
        "status": status,
        "action": action,
        "confidence": confidence,
        "color": color
    }
    
