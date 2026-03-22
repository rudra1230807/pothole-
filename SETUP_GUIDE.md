# 🚀 Pothole-iQ Setup Guide

Complete setup guide for getting Pothole-iQ running on your system.

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Internet**: Required for initial model download

### Recommended Requirements
- **RAM**: 16GB for better performance
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster processing)
- **Storage**: SSD for faster model loading

## 🛠️ Installation Methods

### Method 1: Quick Setup (Recommended)

1. **Clone Repository**
   ```bash
   git clone https://github.com/rudra1230807/pothole-.git
   cd pothole-
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Sample Images**
   ```bash
   python create_sample_images.py
   ```

4. **Launch Dashboard**
   ```bash
   python launch_structured.py
   ```

### Method 2: Virtual Environment Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/rudra1230807/pothole-.git
   cd pothole-
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv pothole_env
   pothole_env\Scripts\activate
   
   # macOS/Linux
   python3 -m venv pothole_env
   source pothole_env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python -c "import streamlit, cv2, ultralytics; print('✅ All dependencies installed!')"
   ```

### Method 3: Conda Environment

1. **Create Conda Environment**
   ```bash
   conda create -n pothole python=3.9
   conda activate pothole
   ```

2. **Clone and Install**
   ```bash
   git clone https://github.com/rudra1230807/pothole-.git
   cd pothole-
   pip install -r requirements.txt
   ```

## 🔧 Configuration

### 1. Model Setup
The YOLOv8 model will be automatically downloaded on first run. If you encounter issues:

```bash
# Manual model download
python -c "from ultralytics import YOLO; YOLO('yolov8n-seg.pt')"
```

### 2. Environment Variables (Optional)
Create a `.env` file for custom configurations:

```bash
# .env file
POTHOLE_MODEL_PATH=yolov8n-seg.pt
DEFAULT_LOCATION=Your City, Your State
DEFAULT_SCALE_FACTOR=0.5
DEFAULT_COST_RATE=2.5
```

### 3. Directory Structure
The system will create these directories automatically:
```
pothole-/
├── reports/          # Generated reports
├── samples/          # Sample images
├── exports/          # Exported files
└── temp/            # Temporary files
```

## 🚀 Launch Options

### Dashboard Options

1. **Structured Dashboard** (Clean Layout)
   ```bash
   python launch_structured.py
   # OR
   streamlit run structured_dashboard.py
   ```

2. **Professional Dashboard** (Enterprise)
   ```bash
   python launch_professional.py
   # OR
   streamlit run professional_dashboard.py
   ```

3. **Basic Dashboard**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Command Line Interface**
   ```bash
   python main.py
   ```

### Custom Launch Parameters

```bash
# Custom port
streamlit run structured_dashboard.py --server.port 8502

# Custom host
streamlit run structured_dashboard.py --server.address 0.0.0.0

# Disable browser auto-open
streamlit run structured_dashboard.py --server.headless true
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Error: No module named 'cv2'
pip install opencv-python

# Error: No module named 'ultralytics'
pip install ultralytics

# Error: No module named 'streamlit'
pip install streamlit
```

#### 2. Model Download Issues
```bash
# If automatic download fails
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-seg.pt
# OR
curl -L https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-seg.pt -o yolov8n-seg.pt
```

#### 3. Permission Issues (Linux/macOS)
```bash
# Make scripts executable
chmod +x launch_structured.py
chmod +x launch_professional.py
```

#### 4. Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

#### 5. Memory Issues
```bash
# Reduce model size (if needed)
# Edit the model loading in detector files:
# YOLO('yolov8n-seg.pt')  # Nano (smallest)
# YOLO('yolov8s-seg.pt')  # Small
# YOLO('yolov8m-seg.pt')  # Medium
```

### Performance Optimization

#### 1. GPU Acceleration (NVIDIA)
```bash
# Install CUDA-enabled PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Verify GPU support
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

#### 2. CPU Optimization
```bash
# Set environment variables for better CPU performance
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
```

## 📊 Verification

### Test Installation
```bash
# Run system check
python -c "
import sys
print('Python version:', sys.version)
import streamlit as st
print('Streamlit version:', st.__version__)
import cv2
print('OpenCV version:', cv2.__version__)
from ultralytics import YOLO
print('✅ All systems operational!')
"
```

### Test Dashboard
1. Launch structured dashboard: `python launch_structured.py`
2. Open browser to `http://localhost:8501`
3. Generate sample images using the button
4. Upload a sample image
5. Click "Analyze Image"
6. Verify results appear

### Test Command Line
```bash
# Generate sample images
python create_sample_images.py

# Run analysis
python main.py

# Check for output files
ls -la *.jpg *.json
```

## 🔄 Updates

### Update System
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Clear cache (if needed)
streamlit cache clear
```

### Version Check
```bash
# Check current version
python -c "
import json
with open('package.json', 'r') as f:
    data = json.load(f)
    print('Pothole-iQ version:', data['version'])
"
```

## 📞 Support

If you encounter issues:

1. **Check this guide** for common solutions
2. **Search existing issues** on GitHub
3. **Create new issue** with:
   - System information
   - Error messages
   - Steps to reproduce
   - Screenshots

### System Information Script
```bash
python -c "
import sys, platform, cv2, streamlit
print('System:', platform.system(), platform.release())
print('Python:', sys.version)
print('OpenCV:', cv2.__version__)
print('Streamlit:', streamlit.__version__)
"
```

## 🎉 Success!

Once setup is complete, you should have:
- ✅ All dependencies installed
- ✅ Sample images generated
- ✅ Dashboard accessible at `http://localhost:8501`
- ✅ Command line interface working
- ✅ Professional reports generating

**You're ready to analyze potholes! 🚧🚀**