# GitHub Setup Instructions

## Quick Push Commands

```bash
# First time push
git remote add origin https://github.com/VonHoltenCodes/monitor-test-patterns.git
git push -u origin main

# Future updates
git add .
git commit -m "Your commit message"
git push
```

## Repository Settings to Configure

After pushing, go to your GitHub repository settings:

### 1. About Section
- **Description**: Professional monitor test patterns for CRT, LCD, OLED calibration
- **Website**: https://neonpulsetechshop.com
- **Topics**: 
  - `crt`
  - `monitor-calibration`
  - `test-patterns`
  - `display-testing`
  - `vintage-computing`
  - `electron-gun`
  - `phosphor-display`

### 2. GitHub Pages (Optional)
To host the HTML patterns online:
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: main
4. Folder: /html-patterns
5. Save

Your patterns will be available at:
`https://vonholtencodes.github.io/monitor-test-patterns/`

### 3. Releases
Create a release with:
- Standalone Windows executable
- Zip of all HTML patterns
- Release notes highlighting key features

### 4. Social Preview
Consider adding a custom social preview image using one of the screenshots

## Collaboration Settings

- Add collaborators if needed
- Enable issues for bug reports
- Enable discussions for community support
- Consider adding CONTRIBUTING.md for contribution guidelines

## Promotion Ideas

1. Post on:
   - r/crtgaming
   - r/vintagecomputing
   - Vintage computer forums
   - Hackaday
   
2. Create a demo video showing patterns in action

3. Add shields/badges to README:
   ```markdown
   ![GitHub stars](https://img.shields.io/github/stars/VonHoltenCodes/monitor-test-patterns)
   ![GitHub forks](https://img.shields.io/github/forks/VonHoltenCodes/monitor-test-patterns)
   ```

4. Consider submitting to:
   - Awesome lists for display calibration
   - CRT community resources
   - Retro gaming tool collections