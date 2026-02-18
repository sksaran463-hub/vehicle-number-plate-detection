from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import easyocr
import os
import uuid
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ================= FOLDERS =================
UPLOAD_FOLDER = "static/uploads"
OUT_IMG = "static/outputs/images"
OUT_VID = "static/outputs/videos"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUT_IMG, exist_ok=True)
os.makedirs(OUT_VID, exist_ok=True)

# ================= HISTORY FILE =================
HISTORY_FILE = "history.json"

# ================= LOAD MODEL =================
model = YOLO("best.pt")
reader = easyocr.Reader(['en'], gpu=False)

# ================= SAVE HISTORY FUNCTION =================
def save_history(plate, confidence, image_path):

    record = {
        "plate_number": plate,
        "confidence": confidence,
        "image_path": image_path,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Read existing history
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(record)

    # Write updated history
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ================= DETECT ROUTE =================
@app.route("/detect", methods=["POST"])
def detect_anpr():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    ext = file.filename.split(".")[-1].lower()
    uid = str(uuid.uuid4())
    upload_path = os.path.join(UPLOAD_FOLDER, f"{uid}.{ext}")
    file.save(upload_path)

    plate_text = None
    confidence_text = None
    output_path = None

    # ================= IMAGE =================
    if ext in ["jpg", "jpeg", "png"]:
        img = cv2.imread(upload_path)
        results = model(img, conf=0.4)

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            plate = img[y1:y2, x1:x2]
            ocr = reader.readtext(plate)
            text = ocr[0][1] if ocr else "Not Read"

            plate_text = text
            confidence_text = round(conf, 2)

            label = f"{text} ({confidence_text})"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                img, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2
            )

        out_name = f"{uid}_out.jpg"
        out_path = os.path.join(OUT_IMG, out_name)
        cv2.imwrite(out_path, img)
        output_path = out_path

    # ================= VIDEO =================
    else:
        cap = cv2.VideoCapture(upload_path)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25

        out_name = f"{uid}_out.mp4"
        out_path = os.path.join(OUT_VID, out_name)

        out = cv2.VideoWriter(
            out_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (w, h)
        )

        last_plate = None
        last_conf = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame, conf=0.4)

            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                plate = frame[y1:y2, x1:x2]
                ocr = reader.readtext(plate)
                text = ocr[0][1] if ocr else "Reading"

                last_plate = text
                last_conf = conf

                label = f"{text} ({round(conf,2)})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2
                )

            out.write(frame)

        cap.release()
        out.release()

        plate_text = last_plate
        confidence_text = round(last_conf, 2) if last_conf else None
        output_path = out_path

    # Save to history if detection happened
    if plate_text:
        save_history(plate_text, confidence_text, output_path)

    return jsonify({
        "plate_number": plate_text,
        "confidence": confidence_text,
        "output_file": output_path
    })


# ================= HISTORY ROUTE =================
@app.route("/history", methods=["GET"])
def get_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    return jsonify(data)


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
