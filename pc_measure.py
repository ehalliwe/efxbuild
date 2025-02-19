import cv2
import numpy as np

def preprocess_image(image):
    """Converts image to grayscale and applies thresholding."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)
    return thresh

def find_reference_scale(thresh, ref_object_mm):
    """Finds the reference object and calculates pixels per mm."""
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:  # Filter out noise
            x, y, w, h = cv2.boundingRect(cnt)
            pixel_size = max(w, h)
            return ref_object_mm / pixel_size  # Pixels per mm
    return None

def measure_objects(thresh, pixel_per_mm, image):
    """Finds and measures objects in the image."""
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:  # Ignore small noise
            x, y, w, h = cv2.boundingRect(cnt)
            width_mm = w * pixel_per_mm
            height_mm = h * pixel_per_mm
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, f"{width_mm:.2f}mm x {height_mm:.2f}mm", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def main():
    """Main function to receive and measure objects from the Raspberry Pi stream."""
    reference_object_size = 10.0  # mm (adjust based on your reference object)
    
    cap = cv2.VideoCapture("udp://0.0.0.0:5000", cv2.CAP_FFMPEG)  # Listen for stream
    
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        thresh = preprocess_image(frame)
        pixel_per_mm = find_reference_scale(thresh, reference_object_size)
        if pixel_per_mm:
            measure_objects(thresh, pixel_per_mm, frame)
        
        cv2.imshow("Real-Time Measurement", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()