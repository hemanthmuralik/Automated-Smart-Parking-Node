#!/usr/bin/env python3
"""
Automated Smart Parking - Edge AI Vision Node
---------------------------------------------
Role: Performs Vehicle Detection & OCR, controls physical Gate HW, 
      and communicates with the Safety-Critical C Controller.

Features:
- TFLite Inference (Quantized)
- GPIO Hardware Control (Servo/LED)
- IPC with C Backend
"""

import cv2
import time
import sys
import os
import platform
import subprocess
import argparse
import random

# --- CONFIGURATION ---
CONF_THRESHOLD = 0.6
MODEL_PATH = "models/mobilenet_v2_quant.tflite"
CAMERA_ID = 0  # Use 0 for Webcam, or path to video file
BINARY_NAME = "parking_node.exe" if platform.system() == "Windows" else "./parking_node"

# --- 1. HARDWARE ABSTRACTION LAYER (HAL) ---
try:
    import RPi.GPIO as GPIO
    HARDWARE_MODE = True
    PIN_SERVO = 18
    PIN_LED_RED = 23
    PIN_LED_GREEN = 24
except ImportError:
    HARDWARE_MODE = False
    print("[System] RPi.GPIO not found. Running in Virtual Hardware Mode.")

def setup_hardware():
    if HARDWARE_MODE:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_SERVO, GPIO.OUT)
        GPIO.setup(PIN_LED_RED, GPIO.OUT)
        GPIO.setup(PIN_LED_GREEN, GPIO.OUT)
        # Reset state
        GPIO.output(PIN_LED_RED, GPIO.HIGH) # Red light on (Gate Closed)
        GPIO.output(PIN_LED_GREEN, GPIO.LOW)

def control_gate(open_gate=True):
    """Controls physical servo and status LEDs"""
    if HARDWARE_MODE:
        if open_gate:
            print("[GPIO] Gate Opening (Servo 90°)...")
            GPIO.output(PIN_LED_RED, GPIO.LOW)
            GPIO.output(PIN_LED_GREEN, GPIO.HIGH)
            # Add PWM code for servo here
        else:
            print("[GPIO] Gate Closing (Servo 0°)...")
            GPIO.output(PIN_LED_GREEN, GPIO.LOW)
            GPIO.output(PIN_LED_RED, GPIO.HIGH)
    else:
        # Simulation for Laptop Demo
        status = "OPEN  [|||||||      ]" if open_gate else "CLOSE [|||||||||||||]"
        color = "🟢 GREEN" if open_gate else "🔴 RED"
        print(f"[Hardware] ACTUATOR: Gate {status} | LED: {color}")

# --- 2. EDGE AI INFERENCE ENGINE ---
try:
    import tflite_runtime.interpreter as tflite
    TFLITE_AVAILABLE = True
except ImportError:
    print("[System] TFLite Runtime not found. Using Simulation Engine.")
    TFLITE_AVAILABLE = False

class InferenceEngine:
    def __init__(self, model_path):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        
        if TFLITE_AVAILABLE and os.path.exists(model_path):
            print(f"[AI] Loading Quantized Model: {model_path}...")
            self.interpreter = tflite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        else:
            print("[AI] Running in Fallback/Demo Mode (No Model Loaded)")

    def detect_vehicle(self, frame):
        """
        Runs the actual inference. 
        Returns: (detected: bool, latency: float)
        """
        start_time = time.time()
        
        if self.interpreter:
            # 1. Preprocess (Resize to 300x300, Normalize)
            input_shape = self.input_details[0]['shape']
            resized = cv2.resize(frame, (input_shape[1], input_shape[2]))
            # 2. Set Tensor
            self.interpreter.set_tensor(self.input_details[0]['index'], [resized])
            # 3. Invoke
            self.interpreter.invoke()
            # 4. Parse Results (Simplified for demo)
            # scores = self.interpreter.get_tensor(self.output_details[0]['index'])
            # detected = scores[0] > CONF_THRESHOLD
            detected = True # Placeholder logic for the template
        else:
            # Simulation latency (Processing time)
            time.sleep(0.1) 
            detected = True
            
        latency_ms = (time.time() - start_time) * 1000
        return detected, latency_ms

    def perform_ocr(self, frame):
        """
        Simulates OCR pipeline (Tesseract/EasyOCR would go here).
        Generates a semi-random plate for the demo.
        """
        # In a real build: import pytesseract; return pytesseract.image_to_string(crop)
        return f"KL-{random.randint(10,99)}-AB-{random.randint(1000,9999)}"

# --- 3. IPC BRIDGE (COMMUNICATION) ---
def send_to_controller(plate):
    """Calls the C Binary safely using Subprocess"""
    print(f"[IPC] 📡 Transmitting '{plate}' to Embedded Controller...")
    
    if not os.path.exists(BINARY_NAME):
        print(f"[Error] Critical: C Binary '{BINARY_NAME}' not found. Run 'make' first.")
        return False

    try:
        # Call C program with arguments
        result = subprocess.run(
            [BINARY_NAME, "--park", plate],
            capture_output=True,
            text=True,
            timeout=2 # Watchdog timer
        )
        
        if result.returncode == 0:
            print(f"[Backend Response] ✅ {result.stdout.strip()}")
            return True
        else:
            print(f"[Backend Error] ❌ {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"[IPC Failure] {e}")
        return False

# --- 4. MAIN APPLICATION LOOP ---
def main():
    # Argument Parser for Debugging
    parser = argparse.ArgumentParser(description='Smart Parking Edge Vision Node')
    parser.add_argument('--debug', action='store_true', help='Show Camera Feed')
    args = parser.parse_args()

    setup_hardware()
    ai_engine = InferenceEngine(MODEL_PATH)
    
    print("\n[System] 🟢 Node Online. Waiting for vehicles...")
    
    # Simulate an Event Loop (In real life, this runs on cv2.VideoCapture)
    try:
        while True:
            # 1. Simulate "Motion Detection" Trigger
            input("Press Enter to simulate vehicle arrival (Ctrl+C to exit)...")
            
            # 2. Capture Frame (Dummy frame for demo)
            frame = cv2.imread("examples/car_test.jpg") if os.path.exists("examples/car_test.jpg") else None
            if frame is None:
                frame = 255 * (1 - cv2.merge([cv2.imread("examples/car.jpg")]*3)) # Fallback if no image
            
            # 3. AI Inference
            detected, latency = ai_engine.detect_vehicle(frame)
            
            if detected:
                print(f"[AI] 🚙 Vehicle Detected! (Inference: {latency:.2f}ms)")
                
                # 4. Optical Character Recognition
                plate_text = ai_engine.perform_ocr(frame)
                print(f"[OCR] License Plate: {plate_text}")
                
                # 5. Send to C Backend
                authorized = send_to_controller(plate_text)
                
                # 6. Actuate Hardware
                if authorized:
                    control_gate(open_gate=True)
                    time.sleep(3) # Keep gate open for 3s
                    control_gate(open_gate=False)
            
            print("-" * 40)

    except KeyboardInterrupt:
        print("\n[System] Shutting down...")
        if HARDWARE_MODE:
            GPIO.cleanup()

if __name__ == "__main__":
    main()
  
