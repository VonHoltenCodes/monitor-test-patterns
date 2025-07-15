#!/usr/bin/env python3
"""
Create a placeholder image for the demo GIF
Since video conversion requires ffmpeg which may not be installed
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create a placeholder image
width, height = 800, 450
img = Image.new('RGB', (width, height), color='black')
draw = ImageDraw.Draw(img)

# Draw some test pattern elements
# Grid
for x in range(0, width, 50):
    draw.line([(x, 0), (x, height)], fill='gray', width=1)
for y in range(0, height, 50):
    draw.line([(0, y), (width, y)], fill='gray', width=1)

# Center cross
draw.line([(width//2, 0), (width//2, height)], fill='#00ff41', width=3)
draw.line([(0, height//2), (width, height//2)], fill='#00ff41', width=3)

# Corner markers
marker_size = 50
corners = [(0, 0), (width-marker_size, 0), 
           (0, height-marker_size), (width-marker_size, height-marker_size)]
for x, y in corners:
    draw.rectangle([x, y, x+marker_size, y+marker_size], outline='white', width=2)

# NEONpulseTechshop branding
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
except:
    font = None

text = "NEONpulseTechshop"
if font:
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
else:
    text_width = len(text) * 20
    text_height = 40

text_x = (width - text_width) // 2
text_y = (height - text_height) // 2

# Draw text with glow effect
for offset in range(3, 0, -1):
    color = (255, 0, 255, 100) if offset > 1 else (255, 0, 255)
    if font:
        draw.text((text_x-offset, text_y-offset), "NEON", font=font, fill=color)
        draw.text((text_x+offset+100, text_y-offset), "pulse", font=font, fill=(0, 255, 65))
    else:
        draw.text((text_x-offset, text_y-offset), "NEON", fill=color)
        draw.text((text_x+offset+60, text_y-offset), "pulse", fill=(0, 255, 65))

# Add description
desc = "Monitor Test Pattern Demo"
if font:
    desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    draw.text((width//2 - 100, height - 50), desc, font=desc_font, fill='white')
else:
    draw.text((width//2 - 100, height - 50), desc, fill='white')

# Save as GIF
output_path = os.path.join(os.path.dirname(__file__), '..', 'demo.gif')
img.save(output_path, 'GIF')

print(f"Demo placeholder created: {output_path}")
print("Note: To create an actual demo GIF from the video files, install ffmpeg and run convert_to_gif.sh")