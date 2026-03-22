
# 🚀 Pothole-iQ: AI-Powered Pothole Detection & Analysis

Complete pothole detection system using pretrained YOLOv8 segmentation model with severity classification and cost estimation.

## 🔥 Features

- ✅ **No Training Required** - Uses pretrained YOLOv8-seg model
- 🏗️ **Professional Dashboard** - Enterprise-grade interface with advanced styling
- 🌐 **Web Dashboard** - Interactive Streamlit interface with image upload
- 🔍 **Real-time Detection** - Instant pothole identification
- 📏 **Area Calculation** - Precise pothole size measurement
- ⚠️ **Severity Classification** - Low/Medium/High severity levels
- 💰 **Advanced Cost Analysis** - Material, Labor, Equipment breakdown
- 🖼️ **Visual Output** - Annotated images with detection results
- 📊 **Professional Charts** - Plotly visualizations and data tables
- 📄 **Multiple Report Formats** - JSON and PDF professional reports
- 🎯 **Confidence Scoring** - Detection reliability metrics
- 📐 **Engineering Calculations** - Diameter, risk assessment, repair time

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Professional Dashboard (Recommended)
```bash
python launch_professional.py
```
Or directly:
```bash
streamlit run professional_dashboard.py
```

### 3. Basic Dashboard
```bash
streamlit run streamlit_app.py
```

### 4. Command Line Usage
Place your pothole image as `test.jpg` and run:
```bash
python main.py
```

## 📊 How It Works

1. **Input Image** → Load test image
2. **YOLOv8-Seg Model** → Pretrained segmentation model
3. **Detection & Segmentation** → Identify pothole areas
4. **Mask Extraction** → Extract pixel-level masks
5. **Area Calculation** → Convert pixels to real-world area
6. **Severity Classification** → Categorize damage level
7. **Cost Estimation** → Calculate repair costs
8. **Report Generation** → Output comprehensive analysis

## 🎯 Severity Levels

- 🟢 **Low**: < 1000 cm²
- 🟡 **Medium**: 1000-3000 cm²
- 🔴 **High**: > 3000 cm²

## 💰 Cost Calculation

- Rate: ₹2 per cm²
- Formula: `Total Area × Rate = Estimated Cost`

## 🔧 Configuration

Adjust these parameters in `main.py`:
- `scale_factor`: Pixels to cm² conversion (default: 0.5)
- `rate_per_cm2`: Cost per square cm (default: ₹2)

## 📈 Sample Output

```
========================================
🚀 POTHOLE-iQ ANALYSIS REPORT
========================================
✅ Pothole Detected!
📏 Area: 1250.50 cm²
⚠️  Severity: 🟡 Medium
💰 Estimated Repair Cost: ₹2501.00
🔢 Number of potholes: 2
========================================
```

## 🏆 Technical Highlights

- **Pretrained Model**: No training overhead
- **Real-world Application**: Addresses infrastructure problems
- **Scalable Solution**: Works with any image input
- **Professional Output**: Detailed analysis reports

## 🌐 Web Dashboard Features

The Streamlit dashboard provides:

- **📸 Image Upload**: Drag & drop or browse for images
- **⚙️ Real-time Configuration**: Adjust scale factors and cost rates
- **📊 Interactive Visualizations**: 
  - Bar charts showing pothole size distribution
  - Pie charts for cost breakdown
  - Data tables with detailed metrics
- **🎯 Visual Detection**: Annotated images with pothole boundaries
- **📄 Report Export**: Download detailed JSON reports
- **📱 Responsive Design**: Works on desktop and mobile

### Dashboard Screenshots

The dashboard includes:
- Upload interface with drag-and-drop support
- Real-time parameter adjustment sliders
- Interactive charts and visualizations
- Detailed pothole analysis tables
- Professional report generation

## 🚀 Usage Options

### Option 1: Web Dashboard (Recommended)
```bash
streamlit run streamlit_app.py
```
- Interactive web interface
- Real-time parameter adjustment
- Visual results with charts
- Easy image upload

### Option 2: Command Line
```bash
python main.py
```
- Quick analysis for single images
- Terminal-based output
- Good for automation

### Option 3: Advanced Analysis
```bash
python advanced_pothole_detector.py
```
- Detailed JSON reports
- Batch processing capabilities
- Professional analysis features
>>>>>>> 4ced406 (Initial commit: Complete Pothole-iQ system)
