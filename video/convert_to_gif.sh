#!/bin/bash

# Convert video clips to GIF for README
# Requires ffmpeg

echo "Creating file list for concatenation..."
# Create a file list for ffmpeg concat
cat > filelist.txt << EOF
file '2025-07-15 13-06-29.mkv'
file '2025-07-15 13-07-05.mkv'
file '2025-07-15 13-07-36.mkv'
EOF

echo "Concatenating videos..."
# Concatenate the videos
ffmpeg -f concat -safe 0 -i filelist.txt -c copy combined.mkv

echo "Converting to GIF..."
# Convert to GIF with optimization for <15MB
# Using lower framerate and resolution to keep size down
ffmpeg -i combined.mkv \
  -vf "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  -loop 0 \
  ../demo.gif

echo "Optimizing GIF size..."
# Additional optimization if gifsicle is available
if command -v gifsicle &> /dev/null; then
    gifsicle -O3 --lossy=80 -o ../demo_optimized.gif ../demo.gif
    mv ../demo_optimized.gif ../demo.gif
fi

# Check file size
size=$(ls -lh ../demo.gif | awk '{print $5}')
echo "GIF created: demo.gif (Size: $size)"

# Cleanup
rm filelist.txt combined.mkv

if [[ $(stat -c%s "../demo.gif") -gt 15728640 ]]; then
    echo "Warning: GIF is larger than 15MB. Trying more aggressive compression..."
    ffmpeg -i combined.mkv \
      -vf "fps=8,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
      -loop 0 \
      ../demo_small.gif
    mv ../demo_small.gif ../demo.gif
fi

echo "Done!"