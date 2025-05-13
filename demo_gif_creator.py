import time
import pyautogui
import sys
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

"""
Demo GIF Creator for Context Catcher

This script helps you record your screen to create a demo GIF
of Context Catcher in action. It will capture a series of screenshots
and convert them into a GIF file.

Requirements:
- pip install pyautogui pillow

How to use:
1. Run this script
2. Navigate to your Streamlit app
3. The script will capture the screen at regular intervals
4. Press Ctrl+C to stop recording
5. The screenshots will be combined into a GIF file
"""

# Configuration
OUTPUT_DIR = "demo_screenshots"
GIF_FILENAME = f"context_catcher_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif"
CAPTURE_INTERVAL = 1.0  # seconds between captures
REGION = None  # (left, top, width, height) or None for fullscreen
ADD_TIMESTAMP = True
FONT_SIZE = 14
FONT_COLOR = (255, 0, 0)  # Red
GIF_DURATION = 500  # milliseconds per frame

def create_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

def capture_screen(count):
    """Capture screen and save to file"""
    filename = os.path.join(OUTPUT_DIR, f"screenshot_{count:04d}.png")
    
    # Take screenshot
    screenshot = pyautogui.screenshot(region=REGION)
    
    # Add timestamp if enabled
    if ADD_TIMESTAMP:
        draw = ImageDraw.Draw(screenshot)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Try to get a font, use default if not available
        try:
            font = ImageFont.truetype("arial.ttf", FONT_SIZE)
        except:
            font = ImageFont.load_default()
            
        # Draw timestamp
        draw.text((10, 10), timestamp, font=font, fill=FONT_COLOR)
    
    # Save screenshot
    screenshot.save(filename)
    print(f"Captured screenshot {count}: {filename}")
    return filename

def create_gif(filenames):
    """Create GIF from screenshots"""
    if not filenames:
        print("No screenshots to create GIF")
        return
    
    print(f"Creating GIF from {len(filenames)} screenshots...")
    
    # Open first image to get size
    images = []
    for filename in filenames:
        img = Image.open(filename)
        images.append(img)
    
    # Save GIF
    images[0].save(
        GIF_FILENAME,
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=GIF_DURATION,
        loop=0
    )
    
    print(f"GIF created: {GIF_FILENAME}")

def main():
    print("Demo GIF Creator for Context Catcher")
    print("====================================")
    print("Press Ctrl+C to stop recording")
    
    # Create output directory
    create_output_dir()
    
    # Wait for user to position window
    print("You have 5 seconds to position your window...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Start capturing
    count = 0
    filenames = []
    
    try:
        while True:
            filename = capture_screen(count)
            filenames.append(filename)
            count += 1
            time.sleep(CAPTURE_INTERVAL)
    except KeyboardInterrupt:
        print("\nRecording stopped")
    
    # Create GIF
    create_gif(filenames)
    
    print("Done!")

if __name__ == "__main__":
    main()
