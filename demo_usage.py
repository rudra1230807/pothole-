"""
Demo script showing different ways to use Pothole-iQ
"""

from advanced_pothole_detector import PotholeDetector
import os

def demo_basic_usage():
    """Basic pothole detection demo"""
    print("🔥 DEMO 1: Basic Pothole Detection")
    print("-" * 40)
    
    # Initialize detector with custom parameters
    detector = PotholeDetector(
        scale_factor=0.5,  # Adjust based on your camera setup
        cost_rate=2        # ₹2 per cm²
    )
    
    # Analyze single image
    if os.path.exists('test.jpg'):
        result = detector.analyze_image('test.jpg')
        detector.generate_report(result)
    else:
        print("❌ test.jpg not found. Please add a test image.")

def demo_batch_processing():
    """Batch processing demo"""
    print("\n🔥 DEMO 2: Batch Processing")
    print("-" * 40)
    
    detector = PotholeDetector()
    
    # Create sample folder structure
    sample_folder = 'sample_images'
    if os.path.exists(sample_folder):
        print(f"📁 Processing all images in {sample_folder}/")
        results = detector.batch_analyze(sample_folder)
        print(f"✅ Processed {len(results)} images")
    else:
        print(f"📁 Create a '{sample_folder}' folder and add images for batch processing")

def demo_custom_analysis():
    """Custom analysis with different parameters"""
    print("\n🔥 DEMO 3: Custom Analysis Parameters")
    print("-" * 40)
    
    # High-resolution setup (closer camera, higher precision)
    high_res_detector = PotholeDetector(
        scale_factor=0.1,  # More precise measurement
        cost_rate=5        # Premium repair rate
    )
    
    # Low-resolution setup (distant camera, broader coverage)
    low_res_detector = PotholeDetector(
        scale_factor=1.0,  # Less precise but covers more area
        cost_rate=1.5      # Budget repair rate
    )
    
    print("🎯 High-Resolution Analysis (Precise):")
    print("   - Scale: 0.1 cm²/pixel")
    print("   - Rate: ₹5/cm²")
    
    print("\n🎯 Low-Resolution Analysis (Broad Coverage):")
    print("   - Scale: 1.0 cm²/pixel") 
    print("   - Rate: ₹1.5/cm²")

def demo_professional_workflow():
    """Professional workflow demonstration"""
    print("\n🔥 DEMO 4: Professional Workflow")
    print("-" * 40)
    
    detector = PotholeDetector()
    
    workflow_steps = [
        "1. 📸 Capture road images",
        "2. 🤖 Run AI detection",
        "3. 📏 Calculate areas",
        "4. ⚠️  Classify severity",
        "5. 💰 Estimate costs",
        "6. 📊 Generate reports",
        "7. 🚧 Plan repairs"
    ]
    
    print("Professional Road Maintenance Workflow:")
    for step in workflow_steps:
        print(f"   {step}")
    
    print("\n💡 Pro Tips:")
    print("   • Use consistent camera height for accurate measurements")
    print("   • Calibrate scale_factor based on your setup")
    print("   • Process images in batches for efficiency")
    print("   • Save JSON reports for record keeping")

if __name__ == "__main__":
    print("🚀 POTHOLE-iQ DEMONSTRATION")
    print("=" * 50)
    
    demo_basic_usage()
    demo_batch_processing()
    demo_custom_analysis()
    demo_professional_workflow()
    
    print("\n🏆 Ready to detect potholes like a pro!")
    print("Run 'python main.py' or 'python advanced_pothole_detector.py' to start")