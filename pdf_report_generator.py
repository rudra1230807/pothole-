"""
PDF Report Generator for Professional Pothole Analysis
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import os

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkgreen
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.darkred,
            fontName='Helvetica-Bold'
        ))
    
    def create_cost_breakdown_chart(self, cost_data):
        """Create cost breakdown pie chart"""
        labels = ['Material', 'Labor', 'Equipment']
        sizes = [
            cost_data['material_cost_asphalt'],
            cost_data['labor_cost'],
            cost_data['equipment_cost']
        ]
        colors_chart = ['#ff9999', '#66b3ff', '#99ff99']
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(sizes, labels=labels, colors=colors_chart, autopct='%1.1f%%', startangle=90)
        ax.set_title('Cost Breakdown Analysis', fontsize=14, fontweight='bold')
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer
    
    def generate_pdf_report(self, professional_report, output_filename=None):
        """Generate comprehensive PDF report"""
        if output_filename is None:
            output_filename = f"pothole_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(output_filename, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph("🚀 POTHOLE-iQ PROFESSIONAL ANALYSIS REPORT", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report metadata
        metadata = professional_report['report_metadata']
        meta_data = [
            ['Report ID:', metadata['report_id']],
            ['Generated:', metadata['generated_at'][:19]],
            ['Location:', metadata['location']],
            ['System Version:', metadata['system_version']]
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 20))
        
        # Check if potholes were detected
        if not professional_report.get('detection_summary', {}).get('potholes_detected', 0):
            # No detection case
            story.append(Paragraph("ANALYSIS RESULT", self.styles['SectionHeader']))
            story.append(Paragraph("✅ No potholes detected - Road condition appears good", self.styles['Normal']))
            
            if 'recommendations' in professional_report:
                story.append(Spacer(1, 12))
                story.append(Paragraph("RECOMMENDATIONS", self.styles['SectionHeader']))
                for rec in professional_report['recommendations']:
                    story.append(Paragraph(f"• {rec}", self.styles['Normal']))
            
            doc.build(story)
            return output_filename
        
        # Detection Summary
        detection = professional_report['detection_summary']
        story.append(Paragraph("🧠 DETECTION SUMMARY", self.styles['SectionHeader']))
        
        detection_data = [
            ['Potholes Detected:', str(detection['potholes_detected'])],
            ['Detection Method:', detection['detection_method']],
            ['Confidence Score:', f"{detection['detection_confidence']:.2f}"],
            ['Analysis Status:', detection['analysis_status']]
        ]
        
        detection_table = Table(detection_data, colWidths=[2.5*inch, 3.5*inch])
        detection_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(detection_table)
        story.append(Spacer(1, 20))
        
        # Physical Analysis
        physical = professional_report['physical_analysis']
        story.append(Paragraph("📏 PHYSICAL ANALYSIS", self.styles['SectionHeader']))
        
        physical_data = [
            ['Total Area:', f"{physical['total_area_cm2']} cm²"],
            ['Estimated Diameter:', f"{physical['estimated_diameter_cm']} cm"],
            ['Severity Level:', physical['severity_level']],
            ['Damage Type:', physical['damage_type']]
        ]
        
        physical_table = Table(physical_data, colWidths=[2.5*inch, 3.5*inch])
        physical_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(physical_table)
        story.append(Spacer(1, 20))
        
        # Risk Assessment
        risk = professional_report['risk_assessment']
        story.append(Paragraph("🚨 RISK ASSESSMENT", self.styles['SectionHeader']))
        
        risk_data = [
            ['Risk Level:', risk['risk_level']],
            ['Repair Priority:', risk['repair_priority']],
            ['Recommended Action:', risk['recommended_action']]
        ]
        
        risk_table = Table(risk_data, colWidths=[2.5*inch, 3.5*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightyellow),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(risk_table)
        story.append(Spacer(1, 20))
        
        # Cost Analysis
        cost = professional_report['cost_analysis']
        story.append(Paragraph("💰 COST ANALYSIS", self.styles['SectionHeader']))
        
        cost_data = [
            ['Material Cost (Asphalt):', f"₹{cost['material_cost_asphalt']:.2f}"],
            ['Labor Cost:', f"₹{cost['labor_cost']:.2f}"],
            ['Equipment Cost:', f"₹{cost['equipment_cost']:.2f}"],
            ['TOTAL ESTIMATED COST:', f"₹{cost['total_estimated_cost']:.2f}"]
        ]
        
        cost_table = Table(cost_data, colWidths=[2.5*inch, 3.5*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -2), colors.lightcoral),
            ('BACKGROUND', (0, -1), (-1, -1), colors.red),
            ('TEXTCOLOR', (0, 0), (-1, -2), colors.black),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(cost_table)
        story.append(Spacer(1, 20))
        
        # Add cost breakdown chart
        try:
            chart_buffer = self.create_cost_breakdown_chart(cost)
            chart_img = RLImage(chart_buffer, width=4*inch, height=3*inch)
            story.append(chart_img)
            story.append(Spacer(1, 20))
        except Exception as e:
            print(f"Could not generate chart: {e}")
        
        # Repair Estimation
        repair = professional_report['repair_estimation']
        story.append(Paragraph("⏱️ REPAIR ESTIMATION", self.styles['SectionHeader']))
        
        repair_data = [
            ['Estimated Time:', repair['estimated_repair_time']],
            ['Materials Needed:', ', '.join(repair['recommended_materials'])],
            ['Weather Dependency:', repair['weather_dependency']]
        ]
        
        repair_table = Table(repair_data, colWidths=[2.5*inch, 3.5*inch])
        repair_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightsteelblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(repair_table)
        story.append(Spacer(1, 20))
        
        # Individual Potholes (if multiple)
        if 'individual_potholes' in professional_report and len(professional_report['individual_potholes']) > 1:
            story.append(Paragraph("📋 INDIVIDUAL POTHOLE DETAILS", self.styles['SectionHeader']))
            
            pothole_data = [['ID', 'Area (cm²)', 'Severity', 'Cost (₹)']]
            for pothole in professional_report['individual_potholes']:
                pothole_data.append([
                    str(pothole['id']),
                    f"{pothole['area_cm2']:.2f}",
                    pothole['severity'],
                    f"₹{pothole['cost']:.2f}"
                ])
            
            pothole_table = Table(pothole_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 2*inch])
            pothole_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(pothole_table)
            story.append(Spacer(1, 20))
        
        # Recommendations
        if 'recommendations' in professional_report:
            story.append(Paragraph("📋 PROFESSIONAL RECOMMENDATIONS", self.styles['SectionHeader']))
            for i, rec in enumerate(professional_report['recommendations'], 1):
                story.append(Paragraph(f"{i}. {rec}", self.styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Footer
        story.append(Spacer(1, 30))
        footer = Paragraph("🏆 Report generated by Pothole-iQ Professional System", 
                          ParagraphStyle('Footer', parent=self.styles['Normal'], 
                                       alignment=TA_CENTER, fontSize=10, textColor=colors.grey))
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        return output_filename

# Example usage
def generate_pdf_report(professional_report, output_filename=None):
    """Generate PDF report from professional analysis"""
    generator = PDFReportGenerator()
    return generator.generate_pdf_report(professional_report, output_filename)