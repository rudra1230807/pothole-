"""
Create sample pothole images for guaranteed demo success
"""

import cv2
import numpy as np
import os

def create_sample_pothole_1():
    """Create a synthetic pothole image - Road with dark circular hole"""
    # Create road-like background
    img = np.ones((400, 600, 3), dtype=np.uint8) * 120  # Gray road
    
    # Add road texture
    noise = np.random.normal(0, 10, (400, 600, 3))
    img = np.clip(img + noise, 0, 255).astype(np.uint8)
    
    # Create pothole (dark circular region)
    center = (300, 200)
    radius = 60
    cv2.circle(img, center, radius, (30, 30, 30), -1)  # Dark hole
    
    # Add some irregular edges to make it more realistic
    for i in range(10):
        angle = np.random.uniform(0, 2*np.pi)
        r = np.random.uniform(radius-15, radius+15)
        x = int(center[0] + r * np.cos(angle))
        y = int(center[1] + r * np.sin(angle))
        cv2.circle(img, (x, y), 8, (20, 20, 20), -1)
    
    # Add smaller pothole
    center2 = (450, 300)
    radius2 = 35
    cv2.circle(img, center2, radius2, (25, 25, 25), -1)
    
    return img

def create_sample_pothole_2():
    """Create another synthetic pothole - Cracked road surface"""
    # Create asphalt-like background
    img = np.ones((350, 500, 3), dtype=np.uint8) * 80  # Darker road
    
    # Add texture
    noise = np.random.normal(0, 15, (350, 500, 3))
    img = np.clip(img + noise, 0, 255).astype(np.uint8)
    
    # Create irregular pothole shape
    points = np.array([
        [200, 150], [280, 140], [320, 180], [310, 220], 
        [270, 240], [220, 235], [180, 200], [190, 160]
    ], np.int32)
    
    cv2.fillPoly(img, [points], (15, 15, 15))  # Very dark pothole
    
    # Add some depth variation
    cv2.fillPoly(img, [points[1:6]], (10, 10, 10))  # Even darker center
    
    return img

def create_sample_pothole_3():
    """Create a realistic road crack pattern"""
    # Create concrete-like background
    img = np.ones((300, 450, 3), dtype=np.uint8) * 140  # Light gray concrete
    
    # Add concrete texture
    for _ in range(1000):
        x, y = np.random.randint(0, 450), np.random.randint(0, 300)
        color = np.random.randint(130, 150)
        cv2.circle(img, (x, y), 1, (color, color, color), -1)
    
    # Create crack pattern (dark lines)
    # Main crack
    pts = [(50, 150), (120, 140), (200, 160), (280, 150), (350, 170), (400, 160)]
    for i in range(len(pts)-1):
        cv2.line(img, pts[i], pts[i+1], (40, 40, 40), 3)
    
    # Branch cracks
    cv2.line(img, (150, 145), (140, 100), (45, 45, 45), 2)
    cv2.line(img, (250, 155), (270, 200), (45, 45, 45), 2)
    
    # Create pothole at intersection
    center = (200, 160)
    cv2.circle(img, center, 25, (20, 20, 20), -1)
    cv2.circle(img, center, 15, (10, 10, 10), -1)  # Deeper center
    
    return img

def main():
    """Generate sample images for testing"""
    print("🎨 Creating sample pothole images for guaranteed demo success...")
    
    # Create samples directory
    if not os.path.exists('sample_images'):
        os.makedirs('sample_images')
    
    # Generate sample images
    samples = [
        ("sample_pothole_1.jpg", create_sample_pothole_1()),
        ("sample_pothole_2.jpg", create_sample_pothole_2()),
        ("sample_pothole_3.jpg", create_sample_pothole_3())
    ]
    
    for filename, img in samples:
        # Save in root directory
        cv2.imwrite(filename, img)
        # Also save in samples folder
        cv2.imwrite(f"sample_images/{filename}", img)
        print(f"✅ Created: {filename}")
    
    # Create the main test image
    cv2.imwrite("test.jpg", create_sample_pothole_1())
    print("✅ Created: test.jpg (main test image)")
    
    print("\n🚀 Sample images created successfully!")
    print("📸 Available test images:")
    print("   • test.jpg (main)")
    print("   • sample_pothole_1.jpg")
    print("   • sample_pothole_2.jpg") 
    print("   • sample_pothole_3.jpg")
    print("\n💡 These images are designed to work with both AI and fallback detection!")
    print("🏆 Your demo is now guaranteed to work!")

if __name__ == "__main__":
    main()