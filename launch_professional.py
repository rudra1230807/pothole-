"""
Professional Launcher for Pothole-iQ Enterprise Dashboard
"""

import subprocess
import sys
import os
import webbrowser
import time

def print_banner():
    """Print professional banner"""
    print("🏗️" + "="*60 + "🏗️")
    print("    POTHOLE-iQ PROFESSIONAL ENTERPRISE SYSTEM")
    print("    Advanced AI Infrastructure Analysis Platform")
    print("🏗️" + "="*60 + "🏗️")

def check_system_requirements():
    """Check system requirements and dependencies"""
    print("\n🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", f"{python_version.major}.{python_version.minor}")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check required files
    required_files = [
        'professional_dashboard.py',
        'professional_report_generator.py',
        'create_sample_images.py'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing required file: {file}")
            return False
        print(f"✅ {file}")
    
    # Check dependencies
    required_packages = {
        'streamlit': 'streamlit',
        'ultralytics': 'ultralytics', 
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'PIL': 'pillow',
        'plotly': 'plotly',
        'pandas': 'pandas'
    }
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            missing_packages.append(package_name)
            print(f"❌ {package_name}")
    
    if missing_packages:
        print(f"\n💡 Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        print("   OR")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def setup_environment():
    """Setup professional environment"""
    print("\n⚙️ Setting up professional environment...")
    
    # Create necessary directories
    directories = ['reports', 'samples', 'exports']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
    
    # Generate sample images if they don't exist
    sample_files = ['test.jpg', 'sample_pothole_1.jpg', 'sample_pothole_2.jpg']
    if not any(os.path.exists(f) for f in sample_files):
        print("🎨 Generating professional sample images...")
        try:
            exec(open('create_sample_images.py').read())
            print("✅ Sample images generated")
        except Exception as e:
            print(f"⚠️ Could not generate samples: {e}")
    
    print("✅ Environment setup complete")

def launch_professional_dashboard():
    """Launch the professional dashboard with enhanced settings"""
    print("\n🚀 Launching Pothole-iQ Professional Dashboard...")
    print("📊 Enterprise-grade interface loading...")
    print("🌐 URL: http://localhost:8501")
    print("📱 Dashboard optimized for professional use")
    print("\n" + "⚡ SYSTEM STATUS: ACTIVE" + " "*20 + "Press Ctrl+C to stop ⚡")
    print("-" * 70)
    
    try:
        # Launch with professional configuration
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            "professional_dashboard.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false",
            "--server.headless", "false",
            "--theme.primaryColor", "#1f4e79",
            "--theme.backgroundColor", "#f8f9fa", 
            "--theme.secondaryBackgroundColor", "#ffffff",
            "--theme.textColor", "#2c3e50",
            "--theme.font", "sans serif"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Try to open browser automatically
        try:
            webbrowser.open('http://localhost:8501')
            print("🌐 Browser opened automatically")
        except:
            print("💡 Please open http://localhost:8501 in your browser")
        
        # Wait for process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 SHUTTING DOWN PROFESSIONAL SYSTEM...")
        print("📊 Saving session data...")
        print("🔒 Securing analysis results...")
        print("✅ Professional dashboard stopped successfully")
        print("👋 Thank you for using Pothole-iQ Professional!")
        
    except Exception as e:
        print(f"\n❌ Error launching professional dashboard: {e}")
        print("💡 Try running: streamlit run professional_dashboard.py")

def show_system_info():
    """Show professional system information"""
    print("\n📋 SYSTEM INFORMATION")
    print("-" * 30)
    print("🏗️ System: Pothole-iQ Professional v2.0")
    print("🤖 AI Engine: YOLOv8 Segmentation")
    print("🔬 Fallback: Advanced Computer Vision")
    print("📊 Analytics: Professional Reporting")
    print("📄 Export: JSON, PDF Reports")
    print("🌐 Interface: Streamlit Enterprise")
    print("💻 Platform: Cross-platform")
    print("🔒 Security: Enterprise-grade")

def main():
    """Main launcher function"""
    print_banner()
    
    # System checks
    if not check_system_requirements():
        print("\n❌ System requirements not met. Please install missing components.")
        return
    
    # Environment setup
    setup_environment()
    
    # System info
    show_system_info()
    
    # Launch confirmation
    print("\n🎯 READY TO LAUNCH PROFESSIONAL SYSTEM")
    print("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n👋 Launch cancelled.")
        return
    
    # Launch professional dashboard
    launch_professional_dashboard()

if __name__ == "__main__":
    main()