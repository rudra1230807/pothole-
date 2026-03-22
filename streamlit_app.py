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
    page_title="🚀 Pothole-iQ Dashboard",
    page_icon="🚧",
    layout="wide",
    initial_sidebar_state="expanded"
)

class StreamlitPotholeDetector:
    def __init__(self):
        self.model = None
        self.scale_factor = 0.5
        self.cost_rate = 2
        
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

def main():
    # Header
    st.title("🚀 Pothole-iQ Dashboard")
    st.markdown("### AI-Powered Pothole Detection & Cost Analysis")
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    
    # Location input
    location = st.sidebar.text_input(
        "📍 Location", 
        value="Nashik, Maharashtra",
        help="Enter the location where the image was taken"
    )
    
    # Parameters
    scale_factor = st.sidebar.slider(
        "Scale Factor (cm²/pixel)", 
        min_value=0.1, 
        max_value=2.0, 
        value=0.5, 
        step=0.1,
        help="Adjust based on camera distance and resolution"
    )
    
    cost_rate = st.sidebar.slider(
        "Cost Rate (₹/cm²)", 
        min_value=1.0, 
        max_value=10.0, 
        value=2.0, 
        step=0.5,
        help="Repair cost per square centimeter"
    )
    
    # Info section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Severity Levels")
    st.sidebar.markdown("🟢 **Low**: < 1000 cm²")
    st.sidebar.markdown("🟡 **Medium**: 1000-3000 cm²") 
    st.sidebar.markdown("🔴 **High**: > 3000 cm²")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔬 Detection Methods")
    st.sidebar.markdown("🤖 **AI**: YOLOv8 segmentation")
    st.sidebar.markdown("🔬 **Fallback CV**: Classical computer vision")
    st.sidebar.markdown("💡 System automatically uses fallback if AI fails")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🎨 Create Sample Images"):
        with st.spinner("Generating sample pothole images..."):
            exec(open('create_sample_images.py').read())
        st.sidebar.success("✅ Sample images created!")
    
    # Initialize detector
    detector = StreamlitPotholeDetector()
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose a road image...",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Upload an image containing potholes for analysis"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            image_array = np.array(image)
            
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Analysis button
            if st.button("🔍 Analyze Potholes", type="primary"):
                with st.spinner("🤖 AI is analyzing the image..."):
                    result = detector.analyze_image(image_array, scale_factor, cost_rate)
                    
                    # Generate professional report
                    if result:
                        report_generator = ProfessionalReportGenerator(location)
                        professional_report = report_generator.generate_professional_report(result, cost_rate)
                        result["professional_report"] = professional_report
                
                if result:
                    st.session_state['analysis_result'] = result
                    st.success("✅ Analysis completed!")
                else:
                    st.error("❌ Analysis failed. Please try again.")
    
    with col2:
        st.header("📊 Analysis Results")
        
        if 'analysis_result' in st.session_state:
            result = st.session_state['analysis_result']
            
            if result["potholes_detected"]:
                # Key metrics
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    st.metric(
                        "🔢 Potholes Found", 
                        result["total_potholes"]
                    )
                
                with col_b:
                    st.metric(
                        "📏 Total Area", 
                        f"{result['total_area_cm2']} cm²"
                    )
                
                with col_c:
                    st.metric(
                        "💰 Estimated Cost", 
                        f"₹{result['estimated_cost']}"
                    )
                
                with col_d:
                    method_emoji = "🤖" if result.get("detection_method") == "AI" else "🔬"
                    st.metric(
                        "🔬 Detection Method",
                        f"{method_emoji} {result.get('detection_method', 'AI')}"
                    )
                
                # Severity indicator
                severity = result["severity"]
                severity_colors = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                st.markdown(f"### ⚠️ Overall Severity: {severity_colors.get(severity, '⚪')} {severity}")
                
                # Annotated image
                if result["annotated_image"] is not None:
                    st.image(
                        result["annotated_image"], 
                        caption="🎯 Detected Potholes", 
                        use_column_width=True
                    )
                
                # Individual pothole details
                if result["individual_potholes"]:
                    st.markdown("### 📋 Individual Pothole Details")
                    
                    # Create DataFrame for table
                    df = pd.DataFrame(result["individual_potholes"])
                    df.columns = ["ID", "Area (cm²)", "Severity", "Cost (₹)"]
                    
                    st.dataframe(df, use_container_width=True)
                    
                    # Visualization
                    fig = px.bar(
                        df, 
                        x="ID", 
                        y="Area (cm²)", 
                        color="Severity",
                        title="Pothole Size Distribution",
                        color_discrete_map={
                            "Minor": "#90EE90",
                            "Moderate": "#FFD700", 
                            "Severe": "#FF6B6B"
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Cost breakdown pie chart
                    fig_pie = px.pie(
                        df, 
                        values="Cost (₹)", 
                        names="ID",
                        title="Cost Distribution by Pothole"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Download report
                st.markdown("### 📄 Download Reports")
                
                col_dl1, col_dl2 = st.columns(2)
                
                with col_dl1:
                    # Basic JSON report
                    basic_report = json.dumps(result, indent=2, default=str)
                    st.download_button(
                        label="📥 Download Basic Report (JSON)",
                        data=basic_report,
                        file_name=f"basic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with col_dl2:
                    # Professional report
                    if "professional_report" in result:
                        professional_json = json.dumps(result["professional_report"], indent=2, default=str)
                        st.download_button(
                            label="🏆 Download Professional Report (JSON)",
                            data=professional_json,
                            file_name=f"professional_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                
                # PDF Report Generation
                if "professional_report" in result:
                    st.markdown("### 📄 Generate PDF Report")
                    if st.button("📋 Generate Professional PDF Report"):
                        with st.spinner("Generating PDF report..."):
                            try:
                                from pdf_report_generator import generate_pdf_report
                                pdf_filename = generate_pdf_report(result["professional_report"])
                                
                                # Read PDF file for download
                                with open(pdf_filename, "rb") as pdf_file:
                                    pdf_data = pdf_file.read()
                                
                                st.download_button(
                                    label="📥 Download PDF Report",
                                    data=pdf_data,
                                    file_name=pdf_filename,
                                    mime="application/pdf"
                                )
                                st.success(f"✅ PDF report generated: {pdf_filename}")
                                
                                # Clean up
                                if os.path.exists(pdf_filename):
                                    os.remove(pdf_filename)
                                    
                            except ImportError:
                                st.error("❌ PDF generation requires reportlab. Install with: pip install reportlab matplotlib")
                            except Exception as e:
                                st.error(f"❌ Error generating PDF: {str(e)}")
                
                # Display professional report summary
                if "professional_report" in result:
                    st.markdown("### 🏆 Professional Analysis Summary")
                    prof_report = result["professional_report"]
                    
                    # Key professional metrics
                    col_p1, col_p2, col_p3 = st.columns(3)
                    
                    with col_p1:
                        confidence = prof_report["detection_summary"]["detection_confidence"]
                        st.metric("🎯 Detection Confidence", f"{confidence:.2f}")
                    
                    with col_p2:
                        diameter = prof_report["physical_analysis"]["estimated_diameter_cm"]
                        st.metric("📐 Estimated Diameter", f"{diameter} cm")
                    
                    with col_p3:
                        risk_level = prof_report["risk_assessment"]["risk_level"]
                        risk_emoji = {"Low": "🟢", "Moderate": "🟡", "High": "🔴"}
                        st.metric("🚨 Risk Level", f"{risk_emoji.get(risk_level, '⚪')} {risk_level}")
                    
                    # Cost breakdown chart
                    if "cost_analysis" in prof_report:
                        cost_data = prof_report["cost_analysis"]
                        cost_breakdown = {
                            "Material": cost_data["material_cost_asphalt"],
                            "Labor": cost_data["labor_cost"],
                            "Equipment": cost_data["equipment_cost"]
                        }
                        
                        fig_cost = px.pie(
                            values=list(cost_breakdown.values()),
                            names=list(cost_breakdown.keys()),
                            title="💰 Professional Cost Breakdown"
                        )
                        st.plotly_chart(fig_cost, use_container_width=True)
                    
                    # Recommendations
                    if "recommendations" in prof_report:
                        st.markdown("### 📋 Professional Recommendations")
                        for i, rec in enumerate(prof_report["recommendations"], 1):
                            st.markdown(f"{i}. {rec}")
                    
                    # Repair estimation
                    if "repair_estimation" in prof_report:
                        repair_info = prof_report["repair_estimation"]
                        st.markdown("### ⏱️ Repair Estimation")
                        st.info(f"**Time Required:** {repair_info['estimated_repair_time']}")
                        st.info(f"**Materials:** {', '.join(repair_info['recommended_materials'])}")
                        st.warning(f"**Weather Note:** {repair_info['weather_dependency']}")
                
            else:
                st.info("❌ No potholes detected in the uploaded image.")
                st.markdown("💡 **Pro Tips for Better Detection:**")
                st.markdown("• Use images with clear contrast between potholes and road")
                st.markdown("• Ensure potholes are visible and not too small")
                st.markdown("• Try different lighting conditions")
                st.markdown("• Use the sample images below for testing")
                
                # Show sample images for download
                st.markdown("### 📸 Try These Sample Images")
                if st.button("🎨 Generate Sample Images"):
                    with st.spinner("Creating sample pothole images..."):
                        # Import and run sample creation
                        exec(open('create_sample_images.py').read())
                    st.success("✅ Sample images created! Check your directory.")
        
        else:
            st.info("👆 Upload an image and click 'Analyze Potholes' to see results here.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🚀 <strong>Pothole-iQ</strong> - AI-Powered Road Infrastructure Analysis</p>
            <p>Built with YOLOv8 Segmentation • Streamlit • Computer Vision</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()