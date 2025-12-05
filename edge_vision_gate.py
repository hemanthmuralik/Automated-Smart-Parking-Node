import cv2
import subprocess
import time
import sys
import platform

# Determine binary name based on OS (for cross-platform testing)
BINARY_NAME = "parking_node.exe" if platform.system() == "Windows" else "./parking_node"

def alpr_pipeline():
    """
    Simulates the Computer Vision Pipeline:
    Frame Capture -> GrayScale -> Contour Filtering -> OCR
    """
    print("[Vision Node] Initializing Camera Stream...")
    time.sleep(1) # Warmup
    
    # Simulate processing a frame
    detected_plate = "KL-13-AB-9999"
    confidence = 0.98
    
    print(f"[Vision Node] Vehicle Detected. Processing...")
    time.sleep(0.5) # Inference latency
    print(f"[Vision Node] OCR Result: {detected_plate} (Conf: {confidence*100}%)")
    
    return detected_plate

def trigger_embedded_controller(plate):
    """
    Inter-Process Communication (IPC) Bridge
    Sends data to the Secure C Backend
    """
    print(f"[IPC] Sending payload to Embedded Controller ({BINARY_NAME})...")
    
    try:
        # Secure subprocess call
        result = subprocess.run(
            [BINARY_NAME, "--park", plate], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print(f"[Controller Response]\n{result.stdout}")
        else:
            print(f"[Controller Error] {result.stderr}")
            
    except FileNotFoundError:
        print(f"[Error] Binary '{BINARY_NAME}' not found. Did you compile main.c?")

if __name__ == "__main__":
    print("--- Automated Smart Parking Gate (Edge AI) ---")
    
    # In a real loop, this would trigger on motion detection
    plate_data = alpr_pipeline()
    trigger_embedded_controller(plate_data)
