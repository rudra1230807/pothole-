"""
Launcher for Structured Pothole-iQ Dashboard
"""

import subprocess
import sys
import os

def print_banner():
    """Print structured dashboard banner"""
    print("🚧" + "="*60 + "🚧")
    print("    POTHOLE-iQ STRUCTURED DASHBOARD")
    print("    Clean Layout • Professional Design • Easy Navigation")
    print("🚧" + "="*60 + "🚧")

def check_requirements():
    """Check system requirements"""
    print("\n🔍 Checking requirements...")
    
    # Check required files
    required_files = [
        'structured_dashboard.py',
        'professional_report_generator.py',
        'create_sample_images.py'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing: {file}")
            return False
        print(f"✅ {file}")
    
    # Check dependencies
    required_packages = ['streamlit', 'ultralytics', 'opencv-python', 'plotly', 'pandas']
    missing = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                __import__('cv2')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")
    
    if missing:
        print(f"\n💡 Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def launch_structured_dashboard():
    """Launch the structured dashboard"""
    print("\n🚀 Launching Structured Dashboard...")
    print("📊 Clean, organized interface loading...")
    print("🌐 URL: http://localhost:8501")
    print("\n" + "⚡ DASHBOARD ACTIVE" + " "*30 + "Press Ctrl+C to stop ⚡")
    print("-" * 70)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "structured_dashboard.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false",
            "--theme.primaryColor", "#667eea",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f8f9fa",
            "--theme.textColor", "#2c3e50"
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 SHUTTING DOWN DASHBOARD...")
        print("✅ Dashboard stopped successfully")
        print("👋 Thank you for using Pothole-iQ!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    """Main launcher"""
    print_banner()
    
    if not check_requirements():
        print("\n❌ Requirements not met. Please install missing components.")
        return
    
    print("\n🎯 STRUCTURED DASHBOARD FEATURES:")
    print("   📸 Clean Upload Section")
    print("   🖼️  Side-by-Side Image Preview")
    print("   📊 Professional Metrics Cards")
    print("   💰 Interactive Cost Breakdown Chart")
    print("   📄 Comprehensive Report Section")
    print("   📱 Fully Responsive Design")
    
    print("\n🚀 Ready to launch! Press Enter to continue...")
    
    try:
        input()
        launch_structured_dashboard()
    except KeyboardInterrupt:
        print("\n👋 Launch cancelled.")

if __name__ == "__main__":
    main()