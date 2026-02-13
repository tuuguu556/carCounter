import cv2
from ultralytics import YOLO

VIDEO_PATH = "data/traffic.mp4"
MODEL_NAME = "yolov8n.pt" 
CONF = 0.35

# COCO class IDs:
# 2 = car, 3 = motorcycle, 5 = bus, 7 = truck
VEHICLE_CLASS_IDS = {2, 3, 5, 7}

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise SystemExit(f"Could not open video: {VIDEO_PATH}")

reported_fps = cap.get(cv2.CAP_PROP_FPS)
use_fps = reported_fps if (reported_fps and 1 < reported_fps <= 120) else 30.0
delay_ms = max(1, int(1000 / use_fps))

model = YOLO(MODEL_NAME)

cv2.namedWindow("Detection Preview")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    results = model.predict(frame, conf=CONF, verbose=False)[0]

    for box in results.boxes:
        cls_id = int(box.cls[0])
        if cls_id not in VEHICLE_CLASS_IDS:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cv2.putText(frame, f"id={cls_id} {conf:.2f}", (x1, y1 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Detection Preview", frame)
    key = cv2.waitKey(delay_ms) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
