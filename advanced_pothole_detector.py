import cv2
import numpy as np
from ultralytics import YOLO
import os
import json
from datetime import datetime

class PotholeDetector:
    def __init__(self, model_path='yolov8n-seg.pt', scale_factor=0.5, cost_rate=2):
        """
        Advanced Pothole Detection System
        
        Args:
            model_path: Path to YOLOv8 segmentation model
            scale_factor: Conversion factor from pixels to cm²
            cost_rate: Cost per cm² in currency units
        """
        self.model = YOLO(model_path)
        self.scale_factor = scale_factor
        self.cost_rate = cost_rate
        
    def analyze_image(self, image_path, save_results=True):
        """
        Complete pothole analysis pipeline
        """
        if not os.path.exists(image_path):
            return {"error": f"Image not found: {image_path}"}
        
        # Run inference
        results = self.model(image_path)
        
        analysis_result = {
            "timestamp": datetime.now().isoformat(),
            "image_path": image_path,
            "potholes_detected": False,
            "total_potholes": 0,
            "total_area_cm2": 0,
            "severity": "None",
            "estimated_cost": 0,
            "individual_potholes": []
        }
        
        if results[0].masks is not None:
            masks = results[0].masks.data.cpu().numpy()
            boxes = results[0].boxes.xyxy.cpu().numpy() if results[0].boxes is not None else []
            
            analysis_result["potholes_detected"] = True
            analysis_result["total_potholes"] = len(masks)
            
            total_area = 0
            
            # Analyze each pothole individually
            for i, mask in enumerate(masks):
                pothole_pixels = np.sum(mask > 0)
                pothole_area = pothole_pixels * self.scale_factor
                total_area += pothole_area
                
                # Individual pothole severity
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
                    "cost": round(pothole_area * self.cost_rate, 2)
                }
                
                analysis_result["individual_potholes"].append(pothole_info)
            
            # Overall analysis
            analysis_result["total_area_cm2"] = round(total_area, 2)
            analysis_result["estimated_cost"] = round(total_area * self.cost_rate, 2)
            
            # Overall severity classification
            if total_area < 1000:
                analysis_result["severity"] = "Low"
            elif total_area < 3000:
                analysis_result["severity"] = "Medium"
            else:
                analysis_result["severity"] = "High"
            
            # Save annotated image
            if save_results:
                annotated_frame = results[0].plot()
                output_path = f"analyzed_{os.path.basename(image_path)}"
                cv2.imwrite(output_path, annotated_frame)
                analysis_result["annotated_image"] = output_path
        
        return analysis_result
    
    def generate_report(self, analysis_result):
        """
        Generate formatted report
        """
        print("\n" + "="*50)
        print("🚀 POTHOLE-iQ ADVANCED ANALYSIS REPORT")
        print("="*50)
        print(f"📅 Analysis Date: {analysis_result['timestamp'][:19]}")
        print(f"📸 Image: {analysis_result['image_path']}")
        print("-"*50)
        
        if analysis_result["potholes_detected"]:
            print("✅ POTHOLES DETECTED!")
            print(f"🔢 Total Potholes: {analysis_result['total_potholes']}")
            print(f"📏 Total Area: {analysis_result['total_area_cm2']} cm²")
            
            # Severity with emoji
            severity_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
            emoji = severity_emoji.get(analysis_result['severity'], "⚪")
            print(f"⚠️  Overall Severity: {emoji} {analysis_result['severity']}")
            print(f"💰 Total Estimated Cost: ₹{analysis_result['estimated_cost']}")
            
            print("\n📋 INDIVIDUAL POTHOLE DETAILS:")
            print("-"*30)
            for pothole in analysis_result["individual_potholes"]:
                sev_emoji = {"Minor": "🟢", "Moderate": "🟡", "Severe": "🔴"}
                p_emoji = sev_emoji.get(pothole['severity'], "⚪")
                print(f"  Pothole #{pothole['id']}: {pothole['area_cm2']} cm² | {p_emoji} {pothole['severity']} | ₹{pothole['cost']}")
            
            if "annotated_image" in analysis_result:
                print(f"\n💾 Annotated image saved: {analysis_result['annotated_image']}")
        else:
            print("❌ No potholes detected in the image")
        
        print("="*50)
        return analysis_result
    
    def batch_analyze(self, image_folder):
        """
        Analyze multiple images in a folder
        """
        results = []
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        for filename in os.listdir(image_folder):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                image_path = os.path.join(image_folder, filename)
                result = self.analyze_image(image_path)
                results.append(result)
                self.generate_report(result)
        
        return results

def main():
    # Initialize detector
    detector = PotholeDetector()
    
    # Single image analysis
    image_path = 'test.jpg'
    
    if os.path.exists(image_path):
        result = detector.analyze_image(image_path)
        detector.generate_report(result)
        
        # Save detailed JSON report
        with open('pothole_analysis_report.json', 'w') as f:
            json.dump(result, f, indent=2)
        print(f"📄 Detailed JSON report saved: pothole_analysis_report.json")
    else:
        print("📸 Please add a test image named 'test.jpg' to run the analysis")
        print("Or use detector.batch_analyze('folder_path') for multiple images")

if __name__ == "__main__":
    main()