// Pattern generation algorithms

class PatternGenerator {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
    }

    updateDimensions(width, height) {
        this.width = width;
        this.height = height;
    }

    clear() {
        this.ctx.clearRect(0, 0, this.width, this.height);
    }

    // Grid Pattern
    drawGrid(options) {
        const { size, spacing, lineWidth, primaryColor, bgColor, rotation } = options;
        
        this.clear();
        this.ctx.fillStyle = bgColor;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        this.ctx.save();
        this.ctx.translate(this.width / 2, this.height / 2);
        this.ctx.rotate(rotation * Math.PI / 180);
        this.ctx.translate(-this.width / 2, -this.height / 2);
        
        this.ctx.strokeStyle = primaryColor;
        this.ctx.lineWidth = lineWidth;
        
        const step = size + spacing;
        
        // Vertical lines
        for (let x = -this.width; x <= this.width * 2; x += step) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, -this.height);
            this.ctx.lineTo(x, this.height * 2);
            this.ctx.stroke();
        }
        
        // Horizontal lines
        for (let y = -this.height; y <= this.height * 2; y += step) {
            this.ctx.beginPath();
            this.ctx.moveTo(-this.width, y);
            this.ctx.lineTo(this.width * 2, y);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }

    // Color Bars (SMPTE-style)
    drawColorBars(options) {
        const { primaryColor, secondaryColor, bgColor } = options;
        
        this.clear();
        
        // Main color bars (75% intensity)
        const colors = [
            '#c0c0c0', // 75% white
            '#c0c000', // yellow
            '#00c0c0', // cyan
            '#00c000', // green
            '#c000c0', // magenta
            '#c00000', // red
            '#0000c0'  // blue
        ];
        
        const barWidth = this.width / colors.length;
        const mainHeight = this.height * 0.75;
        
        colors.forEach((color, i) => {
            this.ctx.fillStyle = color;
            this.ctx.fillRect(i * barWidth, 0, barWidth, mainHeight);
        });
        
        // PLUGE section
        const plugeHeight = this.height * 0.25;
        const plugeColors = ['#000000', '#0d0d0d', '#1a1a1a', '#333333'];
        const plugeWidth = this.width / plugeColors.length;
        
        plugeColors.forEach((color, i) => {
            this.ctx.fillStyle = color;
            this.ctx.fillRect(i * plugeWidth, mainHeight, plugeWidth, plugeHeight);
        });
    }

    // Circle Pattern
    drawCircles(options) {
        const { size, spacing, lineWidth, primaryColor, secondaryColor, bgColor } = options;
        
        this.clear();
        this.ctx.fillStyle = bgColor;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        const centerX = this.width / 2;
        const centerY = this.height / 2;
        const maxRadius = Math.min(this.width, this.height) / 2;
        
        this.ctx.strokeStyle = primaryColor;
        this.ctx.lineWidth = lineWidth;
        
        for (let radius = size; radius < maxRadius; radius += size + spacing) {
            this.ctx.beginPath();
            this.ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
            this.ctx.stroke();
        }
        
        // Add crosshairs
        this.ctx.strokeStyle = secondaryColor;
        this.ctx.beginPath();
        this.ctx.moveTo(0, centerY);
        this.ctx.lineTo(this.width, centerY);
        this.ctx.moveTo(centerX, 0);
        this.ctx.lineTo(centerX, this.height);
        this.ctx.stroke();
    }

    // Gradient Pattern
    drawGradient(options) {
        const { primaryColor, secondaryColor, bgColor, rotation } = options;
        
        this.clear();
        
        this.ctx.save();
        this.ctx.translate(this.width / 2, this.height / 2);
        this.ctx.rotate(rotation * Math.PI / 180);
        this.ctx.translate(-this.width / 2, -this.height / 2);
        
        const gradient = this.ctx.createLinearGradient(0, 0, this.width, this.height);
        gradient.addColorStop(0, bgColor);
        gradient.addColorStop(0.5, primaryColor);
        gradient.addColorStop(1, secondaryColor);
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(-this.width, -this.height, this.width * 3, this.height * 3);
        
        this.ctx.restore();
    }

    // Checkerboard Pattern
    drawCheckerboard(options) {
        const { size, primaryColor, secondaryColor, bgColor } = options;
        
        this.clear();
        this.ctx.fillStyle = bgColor;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        const rows = Math.ceil(this.height / size);
        const cols = Math.ceil(this.width / size);
        
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const isEven = (row + col) % 2 === 0;
                this.ctx.fillStyle = isEven ? primaryColor : secondaryColor;
                this.ctx.fillRect(col * size, row * size, size, size);
            }
        }
    }

    // Line Pattern
    drawLines(options) {
        const { size, spacing, lineWidth, primaryColor, secondaryColor, bgColor, rotation } = options;
        
        this.clear();
        this.ctx.fillStyle = bgColor;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        this.ctx.save();
        this.ctx.translate(this.width / 2, this.height / 2);
        this.ctx.rotate(rotation * Math.PI / 180);
        this.ctx.translate(-this.width / 2, -this.height / 2);
        
        this.ctx.lineWidth = lineWidth;
        
        // Alternating colored lines
        const step = size + spacing;
        let colorIndex = 0;
        
        for (let y = -this.height; y <= this.height * 2; y += step) {
            this.ctx.strokeStyle = colorIndex % 2 === 0 ? primaryColor : secondaryColor;
            this.ctx.beginPath();
            this.ctx.moveTo(-this.width, y);
            this.ctx.lineTo(this.width * 2, y);
            this.ctx.stroke();
            colorIndex++;
        }
        
        this.ctx.restore();
    }

    // Dot Matrix Pattern
    drawDots(options) {
        const { size, spacing, primaryColor, secondaryColor, bgColor } = options;
        
        this.clear();
        this.ctx.fillStyle = bgColor;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        const step = size + spacing;
        const dotRadius = size / 2;
        
        for (let y = dotRadius; y < this.height; y += step) {
            for (let x = dotRadius; x < this.width; x += step) {
                // RGB dot pattern
                this.ctx.fillStyle = primaryColor;
                this.ctx.beginPath();
                this.ctx.arc(x - dotRadius/3, y, dotRadius/3, 0, Math.PI * 2);
                this.ctx.fill();
                
                this.ctx.fillStyle = secondaryColor;
                this.ctx.beginPath();
                this.ctx.arc(x + dotRadius/3, y, dotRadius/3, 0, Math.PI * 2);
                this.ctx.fill();
                
                this.ctx.fillStyle = '#0000ff';
                this.ctx.beginPath();
                this.ctx.arc(x, y - dotRadius/3, dotRadius/3, 0, Math.PI * 2);
                this.ctx.fill();
            }
        }
    }

    // Custom Pattern (combines multiple elements)
    drawCustom(options) {
        const { size, spacing, lineWidth, primaryColor, secondaryColor, bgColor, rotation } = options;
        
        this.clear();
        this.ctx.fillStyle = bgColor;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Draw a combination of patterns
        this.ctx.save();
        this.ctx.globalAlpha = 0.5;
        
        // Grid
        this.drawGrid({ ...options, lineWidth: 1 });
        
        // Center circle
        this.ctx.globalAlpha = 1;
        this.ctx.strokeStyle = primaryColor;
        this.ctx.lineWidth = lineWidth;
        this.ctx.beginPath();
        this.ctx.arc(this.width / 2, this.height / 2, Math.min(this.width, this.height) / 4, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Corner markers
        const markerSize = 50;
        this.ctx.fillStyle = secondaryColor;
        
        // Top-left
        this.ctx.fillRect(0, 0, markerSize, lineWidth);
        this.ctx.fillRect(0, 0, lineWidth, markerSize);
        
        // Top-right
        this.ctx.fillRect(this.width - markerSize, 0, markerSize, lineWidth);
        this.ctx.fillRect(this.width - lineWidth, 0, lineWidth, markerSize);
        
        // Bottom-left
        this.ctx.fillRect(0, this.height - lineWidth, markerSize, lineWidth);
        this.ctx.fillRect(0, this.height - markerSize, lineWidth, markerSize);
        
        // Bottom-right
        this.ctx.fillRect(this.width - markerSize, this.height - lineWidth, markerSize, lineWidth);
        this.ctx.fillRect(this.width - lineWidth, this.height - markerSize, lineWidth, markerSize);
        
        this.ctx.restore();
    }

    // Preset patterns
    applyPreset(presetName, options) {
        switch(presetName) {
            case 'convergence':
                this.drawGrid({
                    ...options,
                    size: 20,
                    spacing: 0,
                    lineWidth: 1,
                    primaryColor: '#ffffff',
                    bgColor: '#000000'
                });
                break;
                
            case 'focus':
                this.drawCircles({
                    ...options,
                    size: 30,
                    spacing: 10,
                    lineWidth: 1,
                    primaryColor: '#ffffff',
                    secondaryColor: '#00ff41',
                    bgColor: '#000000'
                });
                break;
                
            case 'linearity':
                this.drawGrid({
                    ...options,
                    size: 50,
                    spacing: 0,
                    lineWidth: 2,
                    primaryColor: '#00ff41',
                    bgColor: '#000000'
                });
                break;
                
            case 'purity':
                this.ctx.fillStyle = options.primaryColor;
                this.ctx.fillRect(0, 0, this.width, this.height);
                break;
                
            case 'smpte':
                this.drawColorBars(options);
                break;
                
            case 'pluge':
                this.clear();
                const barWidth = this.width / 5;
                const colors = ['#000000', '#070707', '#0f0f0f', '#171717', '#1f1f1f'];
                colors.forEach((color, i) => {
                    this.ctx.fillStyle = color;
                    this.ctx.fillRect(i * barWidth, 0, barWidth, this.height);
                });
                break;
        }
    }
}