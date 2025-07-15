#!/usr/bin/env python3
"""
Create an animated GIF showcasing all test pattern screenshots
"""

import os
from PIL import Image
import glob

# Get all screenshot files
screenshot_dir = "/home/retroxps/repos/projects/monitor-test-patterns/screenshots"
screenshots = sorted(glob.glob(os.path.join(screenshot_dir, "*.png")))

# Filter out any files that aren't test patterns
pattern_files = [f for f in screenshots if os.path.basename(f) != "README.md"]

print(f"Found {len(pattern_files)} screenshots to process...")

# Load all images
images = []
for i, filepath in enumerate(pattern_files):
    print(f"Loading {i+1}/{len(pattern_files)}: {os.path.basename(filepath)}")
    img = Image.open(filepath)
    
    # Resize to a consistent size (800x600 for reasonable file size)
    img = img.resize((800, 600), Image.Resampling.LANCZOS)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    images.append(img)

# Create title card
title_card = Image.new('RGB', (800, 600), color='black')
from PIL import ImageDraw, ImageFont

draw = ImageDraw.Draw(title_card)

# Try to use a nice font, fallback to default if not available
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except:
    title_font = None
    subtitle_font = None
    small_font = None

# Draw title
texts = [
    ("MONITOR", 150, (255, 0, 255)),  # Magenta
    ("TEST PATTERNS", 220, (0, 255, 65)),  # Green
    ("Professional Calibration Suite", 320, (255, 255, 255)),
    ("github.com/VonHoltenCodes", 450, (128, 128, 128))
]

for text, y, color in texts:
    if y < 300:  # Title texts
        font = title_font
    elif y < 400:  # Subtitle
        font = subtitle_font
    else:  # URL
        font = small_font
    
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
    else:
        text_width = len(text) * 10
    
    x = (800 - text_width) // 2
    
    # Add glow effect for title texts
    if y < 300:
        for offset in range(3, 0, -1):
            glow_color = (*color, 100) if len(color) == 3 else color
            draw.text((x-offset, y-offset), text, font=font, fill=glow_color)
    
    draw.text((x, y), text, font=font, fill=color)

# Add NEONpulseTechshop branding
draw.text((20, 560), "NEONpulseTechshop", font=small_font, fill=(255, 0, 255))

# Create end card
end_card = title_card.copy()
draw_end = ImageDraw.Draw(end_card)
draw_end.rectangle([0, 0, 800, 600], fill='black')

end_texts = [
    ("15+ Test Patterns", 150, (255, 255, 255)),
    ("CRT • LCD • OLED", 220, (0, 255, 65)),
    ("Open Source • MIT License", 320, (255, 0, 255)),
    ("Star on GitHub! ⭐", 420, (255, 255, 255))
]

for text, y, color in end_texts:
    if font:
        bbox = draw_end.textbbox((0, 0), text, font=subtitle_font if y < 300 else small_font)
        text_width = bbox[2] - bbox[0]
    else:
        text_width = len(text) * 10
    
    x = (800 - text_width) // 2
    draw_end.text((x, y), text, font=subtitle_font if y < 300 else small_font, fill=color)

# Combine all frames
all_frames = [title_card] + images + [end_card]

# Save as animated GIF
output_path = "/home/retroxps/repos/projects/monitor-test-patterns/showcase.gif"
print(f"\nCreating animated GIF with {len(all_frames)} frames...")

# Save with optimized settings
all_frames[0].save(
    output_path,
    save_all=True,
    append_images=all_frames[1:],
    duration=600,  # 600ms per frame
    loop=0,
    optimize=True
)

print(f"✅ Created showcase.gif ({os.path.getsize(output_path) / 1024 / 1024:.1f} MB)")

# Also create a faster version for X/Twitter
twitter_output = "/home/retroxps/repos/projects/monitor-test-patterns/showcase-twitter.gif"
print("\nCreating faster version for X/Twitter...")

# Use fewer frames and faster timing for Twitter
twitter_frames = [title_card] + images[::2] + [end_card]  # Every other frame
twitter_frames[0].save(
    twitter_output,
    save_all=True,
    append_images=twitter_frames[1:],
    duration=400,  # 400ms per frame (faster)
    loop=0,
    optimize=True
)

print(f"✅ Created showcase-twitter.gif ({os.path.getsize(twitter_output) / 1024 / 1024:.1f} MB)")
print("\nDone! Use showcase.gif for GitHub and showcase-twitter.gif for X")