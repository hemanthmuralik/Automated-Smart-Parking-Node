# Base image: Lightweight Python for Edge devices
FROM python:3.9-slim-buster

# 1. Install System Dependencies (GCC for C, OpenCV libs)
RUN apt-get update && apt-get install -y \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Setup Working Directory
WORKDIR /app
COPY . /app

# 3. Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 4. Compile the Embedded Controller
RUN gcc main.c utility.c -o parking_node

# 5. Permission cleanup (optional but good practice)
RUN chmod +x parking_node

# 6. Start the Edge AI Node
CMD ["python3", "edge_vision_gate.py"]
