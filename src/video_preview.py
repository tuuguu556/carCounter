import cv2
import time

points = [] 

def on_mouse(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 2:
            points.append((x, y))
            print(f"Clicked: {(x, y)}")
        else:
            # If you want: reset on 3rd click
            points = [(x, y)]
            print("Reset line. New P1:", (x, y))

VIDEO_PATH = "data/traffic.mp4"

FALLBACK_FPS = 30.0

LINE_P1 = (100, 300)
LINE_P2 = (600, 300)

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise SystemExit(f"Could not open video: {VIDEO_PATH}")

reported_fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

estimated_duration = (frame_count / reported_fps) if (reported_fps and reported_fps > 0) else None

print(f"Reported FPS: {reported_fps}")
print(f"Frame count:  {frame_count}")
print(f"Estimated duration (sec): {estimated_duration}")

use_fps = reported_fps
if (not use_fps) or (use_fps <= 1) or (use_fps > 120):
    use_fps = FALLBACK_FPS

delay_ms = max(1, int(1000 / use_fps))
print(f"Using FPS for playback: {use_fps:.2f} -> delay {delay_ms} ms")

prev = time.time()
proc_fps = 0.0

cv2.namedWindow("Car Counter - Preview")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    # now i dont usually do comments but i keep forgetting so this is where fps is calculated
    now = time.time()
    dt = now - prev
    prev = now
    if dt > 0:
        inst = 1.0 / dt
        proc_fps = inst if proc_fps == 0.0 else (0.9 * proc_fps + 0.1 * inst)
    if len(points) >= 1:
        cv2.circle(frame, points[0], 5, (255, 255, 255), -1)
    if len(points) == 2:
        cv2.line(frame, points[0], points[1], (255, 255, 255), 2)


    cv2.putText(frame, f"Proc FPS: {proc_fps:.1f}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Playback FPS: {use_fps:.1f}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Car Counter - Preview", frame)
    cv2.namedWindow("Car Counter - Preview")
    cv2.setMouseCallback("Car Counter - Preview", on_mouse)


    key = cv2.waitKey(delay_ms) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
