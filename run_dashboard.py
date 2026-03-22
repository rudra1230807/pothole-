"""
Quick launcher for Pothole-iQ Professional Dashboard
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit', 'ultralytics', 'opencv-python', 
        'numpy', 'pillow', 'plotly', 'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def launch_dashboard():
    """Launch the Professional Streamlit dashboard"""
    print("🏗️ Launching Pothole-iQ Professional Dashboard...")
    print("📱 Professional dashboard will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("\n⚡ Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Launch Professional Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "professional_dashboard.py", 
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false",
            "--theme.primaryColor", "#1f4e79",
            "--theme.backgroundColor", "#f8f9fa",
            "--theme.secondaryBackgroundColor", "#ffffff",
            "--theme.textColor", "#2c3e50"
        ])
    except KeyboardInterrupt:
        print("\n👋 Professional dashboard stopped. Thanks for using Pothole-iQ!")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

def main():
    print("🏗️ POTHOLE-iQ PROFESSIONAL DASHBOARD LAUNCHER")
    print("=" * 50)
    
    # Check if professional_dashboard.py exists
    if not os.path.exists('professional_dashboard.py'):
        print("❌ professional_dashboard.py not found!")
        print("Make sure you're in the correct directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("✅ All dependencies found!")
    print("🎯 Ready to launch professional dashboard...")
    
    # Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main()