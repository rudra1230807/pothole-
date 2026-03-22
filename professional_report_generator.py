import math
import json
from datetime import datetime
import cv2
import numpy as np

class ProfessionalReportGenerator:
    def __init__(self, location="Nashik, Maharashtra"):
        self.location = location
        self.report_id = f"PR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
    def calculate_diameter(self, area_cm2):
        """Calculate estimated diameter from area"""
        return 2 * math.sqrt(area_cm2 / math.pi)
    
    def calculate_cost_breakdown(self, area_cm2, cost_rate=2.5):
        """Advanced cost calculation with breakdown"""
        # Use the provided cost_rate instead of fixed 2.5
        base_cost = area_cm2 * cost_rate
        
        # Cost distribution based on industry standards
        material_cost = base_cost * 0.45  # Asphalt, concrete
        labor_cost = base_cost * 0.35     # Workers, supervision
        equipment_cost = base_cost * 0.20  # Machinery, tools
        
        total_cost = material_cost + labor_cost + equipment_cost
        
        return {
            "base_cost": round(base_cost, 2),
            "material_cost": round(material_cost, 2),
            "labor_cost": round(labor_cost, 2),
            "equipment_cost": round(equipment_cost, 2),
            "total_cost": round(total_cost, 2)
        }
    
    def assess_risk_and_priority(self, area_cm2, severity):
        """Determine risk level and repair priority"""
        if area_cm2 < 800:
            risk_level = "Low"
            priority = "Low"
            urgency = "within 2 weeks"
        elif area_cm2 < 2500:
            risk_level = "Moderate"
            priority = "Medium"
            urgency = "within 1 week"
        else:
            risk_level = "High"
            priority = "High"
            urgency = "within 2-3 days"
        
        return {
            "risk_level": risk_level,
            "priority": priority,
            "urgency": urgency
        }
    
    def estimate_repair_time(self, area_cm2, pothole_count):
        """Estimate repair time based on size and complexity"""
        base_time_per_cm2 = 0.002  # hours per cm²
        base_time = area_cm2 * base_time_per_cm2
        
        # Add complexity factor for multiple potholes
        complexity_factor = 1 + (pothole_count - 1) * 0.3
        total_time = base_time * complexity_factor
        
        if total_time < 1:
            return "30-60 minutes"
        elif total_time < 2:
            return "1-2 hours"
        elif total_time < 4:
            return "2-4 hours"
        elif total_time < 8:
            return "4-8 hours"
        else:
            return "1-2 days"
    
    def determine_damage_type(self, area_cm2, individual_potholes):
        """Classify damage type based on characteristics"""
        if len(individual_potholes) == 1:
            if area_cm2 < 500:
                return "Minor Surface Crack"
            elif area_cm2 < 1500:
                return "Surface Pothole"
            else:
                return "Deep Pothole"
        else:
            return "Multiple Surface Damage"
    
    def calculate_confidence_score(self, detection_method, area_cm2):
        """Calculate detection confidence based on method and size"""
        if detection_method == "AI":
            base_confidence = 0.85
        else:
            base_confidence = 0.72
        
        # Adjust based on size (larger potholes = higher confidence)
        size_factor = min(area_cm2 / 2000, 1.0) * 0.15
        confidence = min(base_confidence + size_factor, 0.95)
        
        return round(confidence, 2)
    
    def generate_professional_report(self, analysis_result, cost_rate=2.5):
        """Generate comprehensive professional report"""
        if not analysis_result.get("potholes_detected", False):
            return self._generate_no_detection_report()
        
        # Extract data
        total_area = analysis_result["total_area_cm2"]
        severity = analysis_result["severity"]
        pothole_count = analysis_result["total_potholes"]
        individual_potholes = analysis_result.get("individual_potholes", [])
        detection_method = analysis_result.get("detection_method", "AI")
        
        # Calculate advanced metrics using the same cost_rate
        diameter = self.calculate_diameter(total_area)
        cost_breakdown = self.calculate_cost_breakdown(total_area, cost_rate)
        risk_assessment = self.assess_risk_and_priority(total_area, severity)
        repair_time = self.estimate_repair_time(total_area, pothole_count)
        damage_type = self.determine_damage_type(total_area, individual_potholes)
        confidence = self.calculate_confidence_score(detection_method, total_area)
        
        # Generate comprehensive report
        report = {
            "report_metadata": {
                "report_id": self.report_id,
                "generated_at": datetime.now().isoformat(),
                "system_version": "Pothole-iQ v2.0 Professional",
                "location": self.location
            },
            "detection_summary": {
                "potholes_detected": pothole_count,
                "detection_method": detection_method,
                "detection_confidence": confidence,
                "analysis_status": "Complete"
            },
            "physical_analysis": {
                "total_area_cm2": total_area,
                "estimated_diameter_cm": round(diameter, 2),
                "severity_level": severity,
                "damage_type": damage_type
            },
            "risk_assessment": {
                "risk_level": risk_assessment["risk_level"],
                "repair_priority": risk_assessment["priority"],
                "recommended_action": f"Schedule repair {risk_assessment['urgency']}"
            },
            "cost_analysis": {
                "base_repair_cost": cost_breakdown["base_cost"],
                "material_cost_asphalt": cost_breakdown["material_cost"],
                "labor_cost": cost_breakdown["labor_cost"],
                "equipment_cost": cost_breakdown["equipment_cost"],
                "total_estimated_cost": cost_breakdown["total_cost"],
                "currency": "INR"
            },
            "repair_estimation": {
                "estimated_repair_time": repair_time,
                "recommended_materials": ["Hot Mix Asphalt", "Tack Coat", "Compaction Equipment"],
                "weather_dependency": "Avoid repair during monsoon season"
            },
            "individual_potholes": individual_potholes,
            "recommendations": self._generate_recommendations(risk_assessment, total_area)
        }
        
        return report
    
    def _generate_no_detection_report(self):
        """Generate report when no potholes detected"""
        return {
            "report_metadata": {
                "report_id": self.report_id,
                "generated_at": datetime.now().isoformat(),
                "system_version": "Pothole-iQ v2.0 Professional",
                "location": self.location
            },
            "detection_summary": {
                "potholes_detected": 0,
                "analysis_status": "No damage detected",
                "road_condition": "Good"
            },
            "recommendations": ["Continue regular monitoring", "Schedule routine maintenance check"]
        }
    
    def _generate_recommendations(self, risk_assessment, area_cm2):
        """Generate actionable recommendations"""
        recommendations = []
        
        if risk_assessment["risk_level"] == "High":
            recommendations.extend([
                "🚨 URGENT: Immediate repair required",
                "🚧 Consider temporary traffic diversion",
                "📋 Schedule professional assessment"
            ])
        elif risk_assessment["risk_level"] == "Moderate":
            recommendations.extend([
                "⚠️ Schedule repair within recommended timeframe",
                "🔍 Monitor for expansion",
                "📊 Include in next maintenance cycle"
            ])
        else:
            recommendations.extend([
                "📅 Add to routine maintenance schedule",
                "👀 Monitor during regular inspections"
            ])
        
        # Size-based recommendations
        if area_cm2 > 3000:
            recommendations.append("🏗️ Consider full section replacement")
        
        return recommendations
    
    def print_formatted_report(self, report):
        """Print beautifully formatted console report"""
        if not report.get("detection_summary", {}).get("potholes_detected", 0):
            self._print_no_detection_report(report)
            return
        
        print("\n" + "="*60)
        print("🚀 POTHOLE-iQ PROFESSIONAL ANALYSIS REPORT")
        print("="*60)
        
        # Header Info
        print(f"📋 Report ID: {report['report_metadata']['report_id']}")
        print(f"📍 Location: {report['report_metadata']['location']}")
        print(f"📅 Generated: {report['report_metadata']['generated_at'][:19]}")
        print(f"🖼️  Image Analysis: Complete")
        
        print("\n" + "-"*40)
        print("🧠 DETECTION SUMMARY")
        print("-"*40)
        detection = report["detection_summary"]
        print(f"✅ Potholes Detected: {detection['potholes_detected']}")
        print(f"🤖 Detection Method: {detection['detection_method']}")
        print(f"📊 Confidence Score: {detection['detection_confidence']}")
        
        print("\n" + "-"*40)
        print("📏 PHYSICAL ANALYSIS")
        print("-"*40)
        physical = report["physical_analysis"]
        print(f"📐 Total Area: {physical['total_area_cm2']} cm²")
        print(f"⭕ Estimated Diameter: {physical['estimated_diameter_cm']} cm")
        print(f"⚠️  Severity Level: {physical['severity_level']}")
        print(f"🔍 Damage Type: {physical['damage_type']}")
        
        print("\n" + "-"*40)
        print("🚨 RISK ASSESSMENT")
        print("-"*40)
        risk = report["risk_assessment"]
        print(f"⚡ Risk Level: {risk['risk_level']}")
        print(f"📊 Repair Priority: {risk['repair_priority']}")
        print(f"⏰ Action Required: {risk['recommended_action']}")
        
        print("\n" + "-"*40)
        print("💰 COST ANALYSIS BREAKDOWN")
        print("-"*40)
        cost = report["cost_analysis"]
        print(f"🏗️  Material Cost (Asphalt): ₹{cost['material_cost_asphalt']}")
        print(f"👷 Labor Cost: ₹{cost['labor_cost']}")
        print(f"🚜 Equipment Cost: ₹{cost['equipment_cost']}")
        print(f"➡️  TOTAL ESTIMATED COST: ₹{cost['total_estimated_cost']}")
        
        print("\n" + "-"*40)
        print("⏱️  REPAIR ESTIMATION")
        print("-"*40)
        repair = report["repair_estimation"]
        print(f"🕐 Estimated Time: {repair['estimated_repair_time']}")
        print(f"🧱 Materials Needed: {', '.join(repair['recommended_materials'])}")
        print(f"🌦️  Weather Note: {repair['weather_dependency']}")
        
        print("\n" + "-"*40)
        print("📋 RECOMMENDATIONS")
        print("-"*40)
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"{i}. {rec}")
        
        print("\n" + "="*60)
        print("🏆 Report generated by Pothole-iQ Professional System")
        print("="*60)
    
    def _print_no_detection_report(self, report):
        """Print report for no detection case"""
        print("\n" + "="*50)
        print("🚀 POTHOLE-iQ ANALYSIS REPORT")
        print("="*50)
        print(f"📋 Report ID: {report['report_metadata']['report_id']}")
        print(f"📍 Location: {report['report_metadata']['location']}")
        print(f"✅ Road Condition: {report['detection_summary']['road_condition']}")
        print(f"📊 Status: {report['detection_summary']['analysis_status']}")
        print("\n📋 Recommendations:")
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"{i}. {rec}")
        print("="*50)

# Example usage function
def generate_professional_analysis(analysis_result, location="Nashik, Maharashtra", cost_rate=2.5):
    """Generate and display professional report"""
    generator = ProfessionalReportGenerator(location)
    professional_report = generator.generate_professional_report(analysis_result, cost_rate)
    generator.print_formatted_report(professional_report)
    return professional_report