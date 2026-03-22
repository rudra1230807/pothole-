import cv2
import numpy as np
from ultralytics import YOLO
import os
from professional_report_generator import generate_professional_analysis

def detect_potholes_fallback(img):
    """
    Fallback pothole detection using classical computer vision
    """
    print("⚠️  AI model couldn't detect potholes directly. Using advanced fallback...")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use adaptive thresholding for better results
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    # Morphological operations to clean up
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
    
    # Find contours (potential potholes)
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None, None, None
    
    # Filter contours by area (remove very small ones)
    min_area = 100  # Minimum pothole area in pixels
    valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
    
    if not valid_contours:
        return None, None, None
    
    # Sort by area and take largest ones (likely potholes)
    valid_contours = sorted(valid_contours, key=cv2.contourArea, reverse=True)
    
    # Create masks for detected regions
    masks = []
    annotated_img = img.copy()
    
    # Take up to 3 largest regions as potential potholes
    for i, contour in enumerate(valid_contours[:3]):
        # Create mask for this contour
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

def detect_potholes(image_path, location="Nashik, Maharashtra"):
    """
    Robust pothole detection with AI + fallback system + Professional Report
    """
    # Load pretrained YOLOv8 segmentation model
    print("🤖 Loading YOLOv8 segmentation model...")
    model = YOLO('yolov8n-seg.pt')
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print(f"🔍 Analyzing image: {image_path}")
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Could not load image")
        return
    
    # Run AI model inference
    results = model(image_path)
    
    masks = None
    annotated_img = None
    detection_method = "AI"
    
    # Check if AI detected anything
    if results[0].masks is not None:
        print("✅ AI model detected objects!")
        masks = results[0].masks.data.cpu().numpy()
        annotated_img = results[0].plot()
        detection_method = "AI"
    else:
        # Use fallback detection
        masks, annotated_img, detection_method = detect_potholes_fallback(img)
    
    # Process results
    if masks is not None and len(masks) > 0:
        # Calculate total pothole area
        total_pixels = 0
        individual_areas = []
        individual_potholes = []
        
        for i, mask in enumerate(masks):
            if isinstance(mask, np.ndarray):
                area = np.sum(mask > 0)
            else:
                area = np.sum(mask)
            total_pixels += area
            individual_areas.append(area)
            
            # Create individual pothole data
            pothole_area_cm2 = area * 0.5  # scale factor
            if pothole_area_cm2 < 500:
                individual_severity = "Minor"
            elif pothole_area_cm2 < 1500:
                individual_severity = "Moderate"
            else:
                individual_severity = "Severe"
            
            individual_potholes.append({
                "id": i + 1,
                "area_cm2": round(pothole_area_cm2, 2),
                "severity": individual_severity,
                "cost": round(pothole_area_cm2 * 2.5, 2)
            })
        
        # Convert to real-world area
        scale_factor = 0.5  # cm² per pixel
        area_cm2 = total_pixels * scale_factor
        
        # Severity classification
        if area_cm2 < 1000:
            severity = "Low"
        elif area_cm2 < 3000:
            severity = "Medium" 
        else:
            severity = "High"
        
        # Cost estimation using professional calculation
        rate_per_cm2 = 2.5
        from professional_report_generator import ProfessionalReportGenerator
        temp_generator = ProfessionalReportGenerator()
        cost_breakdown = temp_generator.calculate_cost_breakdown(area_cm2, rate_per_cm2)
        estimated_cost = cost_breakdown["total_cost"]
        
        # Create analysis result for professional report
        analysis_result = {
            "potholes_detected": True,
            "total_potholes": len(masks),
            "total_area_cm2": round(area_cm2, 2),
            "severity": severity,
            "estimated_cost": round(estimated_cost, 2),
            "individual_potholes": individual_potholes,
            "detection_method": detection_method
        }
        
        # Generate Professional Report
        professional_report = generate_professional_analysis(analysis_result, location, rate_per_cm2)
        
        # Save annotated image
        output_path = f"pothole_detected_{os.path.basename(image_path)}"
        if annotated_img is not None:
            cv2.imwrite(output_path, annotated_img)
            print(f"\n💾 Annotated image saved: {output_path}")
        
        # Save professional report as JSON
        import json
        report_filename = f"professional_report_{professional_report['report_metadata']['report_id']}.json"
        with open(report_filename, 'w') as f:
            json.dump(professional_report, f, indent=2)
        print(f"📄 Professional report saved: {report_filename}")
        
        return analysis_result
        
    else:
        # No detection case
        analysis_result = {
            "potholes_detected": False,
            "total_potholes": 0,
            "total_area_cm2": 0,
            "severity": "None",
            "estimated_cost": 0,
            "individual_potholes": [],
            "detection_method": "none"
        }
        
        # Generate no-detection report
        professional_report = generate_professional_analysis(analysis_result, location)
        
        return analysis_result

if __name__ == "__main__":
    # Default test image
    image_path = 'test.jpg'
    location = "Nashik, Maharashtra"  # You can change this or make it user input
    
    # Check if test image exists, if not provide instructions
    if not os.path.exists(image_path):
        print("📸 Please add a test image named 'test.jpg' to the current directory")
        print("Or modify the 'image_path' variable to point to your image")
        print("💡 Run 'python create_sample_images.py' to generate test images")
    else:
        detect_potholes(image_path, location)