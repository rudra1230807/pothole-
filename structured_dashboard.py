import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import os
import json
from datetime import datetime
from PIL import Image
import tempfile
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from professional_report_generator import ProfessionalReportGenerator

# Page config
st.set_page_config(
    page_title="Pothole-iQ Dashboard",
    page_icon="🚧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for structured layout
st.markdown("""
<style>
    /* Main container styling */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Header section */
    .header-section {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Section styling */
    .section-container {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e8ed;
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 3px solid #3498db;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Upload section */
    .upload-container {
        display: flex;
        gap: 20px;
        align-items: flex-start;
    }
    
    .upload-left {
        flex: 1;
    }
    
    .upload-right {
        flex: 1;
    }
    
    /* Metric cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 8px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .metric-label {
        font-size: 0.95rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Status indicators */
    .status-low { 
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
    }
    .status-medium { 
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .status-high { 
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
    }
    
    /* Button styling */
    .analyze-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        width: 100%;
        margin-top: 20px;
    }
    
    .analyze-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Chart container */
    .chart-container {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* Report section */
    .report-section {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 25px;
        margin-top: 20px;
    }
    
    .download-buttons {
        display: flex;
        gap: 15px;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    
    .download-btn {
        flex: 1;
        min-width: 150px;
    }
    
    /* Image containers */
    .image-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .upload-container {
            flex-direction: column;
        }
        
        .metrics-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }
        
        .download-buttons {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

class StructuredPotholeDetector:
    def __init__(self):
        self.model = None
        
    @st.cache_resource
    def load_model(_self):
        """Load YOLOv8 model with caching"""
        try:
            model = YOLO('yolov8n-seg.pt')
            return model
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return None
    
    def analyze_image(self, image_array, scale_factor, cost_rate):
        """Analyze uploaded image with robust fallback system"""
        if self.model is None:
            self.model = self.load_model()
            
        if self.model is None:
            return None
            
        # Save temp image for YOLO processing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            cv2.imwrite(tmp_file.name, cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR))
            temp_path = tmp_file.name
        
        try:
            # Run AI inference first
            results = self.model(temp_path)
            
            analysis_result = {
                "timestamp": datetime.now().isoformat(),
                "potholes_detected": False,
                "total_potholes": 0,
                "total_area_cm2": 0,
                "severity": "None",
                "estimated_cost": 0,
                "individual_potholes": [],
                "annotated_image": None,
                "detection_method": "AI"
            }
            
            masks = None
            annotated_image = None
            
            # Check AI detection results
            if results[0].masks is not None:
                masks = results[0].masks.data.cpu().numpy()
                annotated_image = results[0].plot()
                analysis_result["detection_method"] = "AI"
            else:
                # Use fallback detection
                masks, annotated_image, _ = self._fallback_detection(image_array)
                analysis_result["detection_method"] = "Fallback CV"
            
            if masks is not None and len(masks) > 0:
                analysis_result["potholes_detected"] = True
                analysis_result["total_potholes"] = len(masks)
                
                total_area = 0
                
                # Analyze each pothole
                for i, mask in enumerate(masks):
                    if isinstance(mask, np.ndarray):
                        pothole_pixels = np.sum(mask > 0)
                    else:
                        pothole_pixels = np.sum(mask)
                        
                    pothole_area = pothole_pixels * scale_factor
                    total_area += pothole_area
                    
                    # Individual severity
                    if pothole_area < 500:
                        individual_severity = "Minor"
                    elif pothole_area < 1500:
                        individual_severity = "Moderate"
                    else:
                        individual_severity = "Severe"
                    
                    pothole_info = {
                        "id": i + 1,
                        "area_cm2": round(pothole_area, 2),
                        "severity": individual_severity,
                        "cost": round(pothole_area * cost_rate, 2)
                    }
                    
                    analysis_result["individual_potholes"].append(pothole_info)
                
                # Overall analysis
                analysis_result["total_area_cm2"] = round(total_area, 2)
                
                # Use professional cost calculation for consistency
                from professional_report_generator import ProfessionalReportGenerator
                temp_generator = ProfessionalReportGenerator()
                cost_breakdown = temp_generator.calculate_cost_breakdown(total_area, cost_rate)
                analysis_result["estimated_cost"] = cost_breakdown["total_cost"]
                
                # Overall severity
                if total_area < 1000:
                    analysis_result["severity"] = "Low"
                elif total_area < 3000:
                    analysis_result["severity"] = "Medium"
                else:
                    analysis_result["severity"] = "High"
                
                # Convert annotated image for display
                if annotated_image is not None:
                    if analysis_result["detection_method"] == "AI":
                        analysis_result["annotated_image"] = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                    else:
                        analysis_result["annotated_image"] = annotated_image
            
            return analysis_result
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _fallback_detection(self, image_array):
        """Fallback pothole detection using classical computer vision"""
        # Convert to grayscale
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
        
        # Morphological operations
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None, "fallback"
        
        # Filter by area
        min_area = 100
        valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
        
        if not valid_contours:
            return None, None, "fallback"
        
        # Sort by area and take largest ones
        valid_contours = sorted(valid_contours, key=cv2.contourArea, reverse=True)
        
        # Create masks
        masks = []
        annotated_img = image_array.copy()
        
        # Take up to 3 largest regions
        for i, contour in enumerate(valid_contours[:3]):
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.drawContours(mask, [contour], -1, 255, -1)
            masks.append(mask)
            
            # Draw on annotated image
            cv2.drawContours(annotated_img, [contour], -1, (0, 255, 0), 2)
            
            # Add label
            x, y, w, h = cv2.boundingRect(contour)
            cv2.putText(annotated_img, f'Pothole {i+1}', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return masks, annotated_img, "fallback"

def create_header():
    """Create the main header section"""
    st.markdown("""
    <div class="header-section">
        <div class="header-title">🚧 POTHOLE-iQ Dashboard</div>
        <div class="header-subtitle">AI-Powered Road Infrastructure Analysis System</div>
    </div>
    """, unsafe_allow_html=True)

def create_upload_section():
    """Create upload image section with location and analyze button"""
    st.markdown("""
    <div class="section-container">
        <div class="section-title">📸 Upload Image</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a road image for analysis",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Upload high-quality road images for best results"
        )
    
    with col2:
        location = st.text_input(
            "📍 Location", 
            value="Nashik, Maharashtra",
            help="Enter the location where image was taken"
        )
        
        scale_factor = st.slider(
            "Scale Factor", 
            min_value=0.1, 
            max_value=2.0, 
            value=0.5, 
            step=0.1,
            help="Adjust based on camera distance"
        )
        
        cost_rate = st.slider(
            "Cost Rate (₹/cm²)", 
            min_value=1.0, 
            max_value=10.0, 
            value=2.5, 
            step=0.5
        )
    
    return uploaded_file, location, scale_factor, cost_rate

def create_image_preview_section(uploaded_file, image_array):
    """Create image preview section"""
    st.markdown("""
    <div class="section-container">
        <div class="section-title">🖼️ Image Preview</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original Image**")
        st.image(image_array, use_container_width=True)
    
    with col2:
        if 'analysis_result' in st.session_state and st.session_state['analysis_result']['annotated_image'] is not None:
            st.markdown("**Detection Result**")
            st.image(st.session_state['analysis_result']['annotated_image'], use_container_width=True)
        else:
            st.markdown("**Detection Result**")
            st.info("Click 'Analyze Image' to see detection results here")

def create_analysis_button(detector, image_array, scale_factor, cost_rate, location):
    """Create analyze button"""
    if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
        with st.spinner("🤖 Analyzing image with AI..."):
            result = detector.analyze_image(image_array, scale_factor, cost_rate)
            
            # Generate professional report
            if result:
                report_generator = ProfessionalReportGenerator(location)
                professional_report = report_generator.generate_professional_report(result, cost_rate)
                result["professional_report"] = professional_report
        
        if result:
            st.session_state['analysis_result'] = result
            st.success("✅ Analysis completed successfully!")
            st.rerun()
        else:
            st.error("❌ Analysis failed. Please try again.")

def create_metrics_section(result):
    """Create analysis metrics cards"""
    st.markdown("""
    <div class="section-container">
        <div class="section-title">📊 Analysis Metrics</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get professional report data
    prof_report = result.get("professional_report", {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{result['total_area_cm2']}</div>
            <div class="metric-label">Area (cm²)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        severity = result["severity"]
        severity_class = f"status-{severity.lower()}"
        severity_icons = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
        st.markdown(f"""
        <div class="metric-card {severity_class}">
            <div class="metric-value">{severity_icons.get(severity, '⚪')}</div>
            <div class="metric-label">{severity} Severity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{result['estimated_cost']:.0f}</div>
            <div class="metric-label">Total Cost</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if prof_report and "risk_assessment" in prof_report:
            risk_level = prof_report["risk_assessment"]["risk_level"]
            risk_icons = {"Low": "🟢", "Moderate": "🟡", "High": "🔴"}
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{risk_icons.get(risk_level, '⚪')}</div>
                <div class="metric-label">{risk_level} Risk</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">-</div>
                <div class="metric-label">Risk Level</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col5:
        if prof_report and "repair_estimation" in prof_report:
            repair_time = prof_report["repair_estimation"]["estimated_repair_time"]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">⏱️</div>
                <div class="metric-label">{repair_time}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">-</div>
                <div class="metric-label">Repair Time</div>
            </div>
            """, unsafe_allow_html=True)

def create_cost_breakdown_chart(result):
    """Create cost breakdown pie chart"""
    st.markdown("""
    <div class="section-container">
        <div class="section-title">💰 Cost Breakdown Chart</div>
    </div>
    """, unsafe_allow_html=True)
    
    prof_report = result.get("professional_report", {})
    
    if prof_report and "cost_analysis" in prof_report:
        cost_data = prof_report["cost_analysis"]
        
        # Create pie chart data
        labels = ['Material (45%)', 'Labor (35%)', 'Equipment (20%)']
        values = [
            cost_data["material_cost_asphalt"],
            cost_data["labor_cost"], 
            cost_data["equipment_cost"]
        ]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent',
            textfont_size=12,
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )])
        
        fig.update_layout(
            title={
                'text': f'Total Cost: ₹{cost_data["total_estimated_cost"]:.0f}',
                'x': 0.5,
                'font': {'size': 18, 'color': '#2c3e50'}
            },
            font=dict(family="Arial, sans-serif", size=12),
            showlegend=True,
            height=400,
            margin=dict(t=80, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Cost breakdown will appear here after analysis")

def create_detailed_report_section(result):
    """Create detailed report section"""
    st.markdown("""
    <div class="section-container">
        <div class="section-title">📄 Detailed Report</div>
    </div>
    """, unsafe_allow_html=True)
    
    prof_report = result.get("professional_report", {})
    
    if prof_report:
        # Key insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔍 Detection Summary**")
            detection = prof_report["detection_summary"]
            st.write(f"• Method: {detection['detection_method']}")
            st.write(f"• Confidence: {detection['detection_confidence']:.1%}")
            st.write(f"• Potholes Found: {detection['potholes_detected']}")
            
            st.markdown("**📏 Physical Analysis**")
            physical = prof_report["physical_analysis"]
            st.write(f"• Diameter: {physical['estimated_diameter_cm']:.1f} cm")
            st.write(f"• Damage Type: {physical['damage_type']}")
        
        with col2:
            st.markdown("**🚨 Risk Assessment**")
            risk = prof_report["risk_assessment"]
            st.write(f"• Priority: {risk['repair_priority']}")
            st.write(f"• Action: {risk['recommended_action']}")
            
            st.markdown("**⏱️ Repair Information**")
            repair = prof_report["repair_estimation"]
            st.write(f"• Time: {repair['estimated_repair_time']}")
            st.write(f"• Materials: {', '.join(repair['recommended_materials'][:2])}")
        
        # Recommendations
        if "recommendations" in prof_report:
            st.markdown("**📋 Professional Recommendations**")
            for i, rec in enumerate(prof_report["recommendations"][:3], 1):
                st.write(f"{i}. {rec}")
        
        # Download buttons
        st.markdown("**📥 Download Options**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            basic_report = json.dumps(result, indent=2, default=str)
            st.download_button(
                label="📊 Analysis Data (JSON)",
                data=basic_report,
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            professional_json = json.dumps(prof_report, indent=2, default=str)
            st.download_button(
                label="🏆 Professional Report (JSON)",
                data=professional_json,
                file_name=f"professional_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            if st.button("📋 Generate PDF", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    try:
                        from pdf_report_generator import generate_pdf_report
                        pdf_filename = generate_pdf_report(prof_report)
                        
                        with open(pdf_filename, "rb") as pdf_file:
                            pdf_data = pdf_file.read()
                        
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_data,
                            file_name=pdf_filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("✅ PDF generated!")
                        
                        if os.path.exists(pdf_filename):
                            os.remove(pdf_filename)
                            
                    except Exception as e:
                        st.error(f"❌ PDF Error: {str(e)}")

def main():
    # Initialize detector
    detector = StructuredPotholeDetector()
    
    # Header section
    create_header()
    
    # Upload section
    uploaded_file, location, scale_factor, cost_rate = create_upload_section()
    
    if uploaded_file is not None:
        # Process uploaded image
        image = Image.open(uploaded_file)
        image_array = np.array(image)
        
        # Image preview section
        create_image_preview_section(uploaded_file, image_array)
        
        # Analyze button
        create_analysis_button(detector, image_array, scale_factor, cost_rate, location)
        
        # Show results if analysis is complete
        if 'analysis_result' in st.session_state:
            result = st.session_state['analysis_result']
            
            if result["potholes_detected"]:
                # Analysis metrics section
                create_metrics_section(result)
                
                # Cost breakdown chart section
                create_cost_breakdown_chart(result)
                
                # Detailed report section
                create_detailed_report_section(result)
                
            else:
                st.markdown("""
                <div class="section-container">
                    <div class="section-title">ℹ️ Analysis Result</div>
                    <p>✅ No potholes detected - Road condition appears good</p>
                    <p>💡 Try uploading an image with visible road damage or use sample images</p>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="section-container">
            <div class="section-title">👆 Getting Started</div>
            <p>1. Upload a road image using the file uploader above</p>
            <p>2. Set your location and adjust parameters if needed</p>
            <p>3. Click 'Analyze Image' to start the AI analysis</p>
            <p>4. View results in the sections below</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show sample generation option
        if st.button("🎨 Generate Sample Images for Testing"):
            with st.spinner("Creating sample images..."):
                exec(open('create_sample_images.py').read())
            st.success("✅ Sample images created! Check your directory.")

if __name__ == "__main__":
    main()