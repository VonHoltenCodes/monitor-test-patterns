#!/bin/bash

# Helper script to push to GitHub

echo "🚀 Pushing NEONpulseTechshop Monitor Test Patterns to GitHub..."

# Add remote if not already added
if ! git remote | grep -q origin; then
    echo "Adding GitHub remote..."
    git remote add origin https://github.com/VonHoltenCodes/monitor-test-patterns.git
fi

# Push to GitHub
echo "Pushing to main branch..."
git push -u origin main

echo "✅ Done! Your project is now live at:"
echo "https://github.com/VonHoltenCodes/monitor-test-patterns"
echo ""
echo "Next steps:"
echo "1. Add topics: crt, monitor-calibration, test-patterns, display-testing"
echo "2. Add description: Professional monitor test patterns for CRT, LCD, OLED calibration"
echo "3. Add website: https://neonpulsetechshop.com"
echo "4. Consider creating releases for standalone executables"