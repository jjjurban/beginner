import cv2
from mtcnn import MTCNN
import time

def list_cameras(max_index=10):
    """List all available cameras with basic info."""
    print("Scanning for cameras...")
    available = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                print(f"Index {i}: Works (Resolution: {width}x{height})")
                available.append((i, width, height))
            else:
                print(f"Index {i}: Opens but no frames.")
            cap.release()
        else:
            print(f"Index {i}: Failed to open.")
    return available

def main():
    print("Starting FaceBox... Hunting for your laptop camera.")
    print("Ensure Continuity Camera is OFF and iPhone is disconnected!")

    # List cameras
    cameras = list_cameras()
    if not cameras:
        print("Error: No working cameras found.")
        print("Next steps:")
        print("- Confirm Continuity Camera is disabled and reboot.")
        print("- Test built-in camera in Photo Booth.")
        return

    if len(cameras) > 1:
        print("Multiple cameras found! Trying the last one (likely built-in).")
        camera_index = cameras[-1][0]
    else:
        camera_index = cameras[0][0]
    
    print(f"Using camera at index {camera_index}...")
    cap = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        print(f"Error: Couldn’t reopen index {camera_index}.")
        return
    
    # Initialize MTCNN for detection
    detector = MTCNN()
    print("MTCNN neural network loaded for face detection.")
    
    time.sleep(1)  # Let camera settle
    
    print(f"FaceBox running (index {camera_index})! Press 'q' to quit.")
    print("Green boxes will appear on faces—wave to test!")
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Error: Failed to grab frame.")
            break
        
        # Detect faces with MTCNN
        faces = detector.detect_faces(frame)
        
        # Draw green boxes
        for face in faces:
            x, y, w, h = face['box']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.putText(frame, f"Index {camera_index}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('FaceBox', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("FaceBox stopped.")

if __name__ == "__main__":
    main()