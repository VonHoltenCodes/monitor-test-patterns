#!/usr/bin/env python3
"""
NEONpulseTechshop CRT Test Pattern Suite
Professional CRT monitor testing patterns with advanced diagnostics
"""

import pygame
import math
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
NEON_GREEN = (0, 255, 65)
NEON_MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)

# Display resolutions by category
RESOLUTIONS = {
    # Classic resolutions
    '1': (640, 480),     # VGA
    '2': (800, 600),     # SVGA
    '3': (1024, 768),    # XGA
    '4': (1280, 1024),   # SXGA
    '5': (1600, 1200),   # UXGA
    # Modern resolutions
    '6': (1920, 1080),   # Full HD / 1080p
    '7': (2560, 1440),   # 2K / QHD / 1440p
    '8': (3840, 2160),   # 4K / UHD
    '9': (7680, 4320),   # 8K / UHD-2
}

class CRTTestSuite:
    def __init__(self, resolution=(1024, 768)):
        self.width, self.height = resolution
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("NEONpulseTechshop CRT Test Suite")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.current_pattern = 0
        self.patterns = [
            self.smpte_color_bars,
            self.convergence_grid,
            self.linearity_grid,
            self.focus_pattern,
            self.purity_test,
            self.contrast_brightness,
            self.geometry_test,
            self.moire_test,
            self.dot_pitch_test,
            self.refresh_rate_test,
            self.burn_in_prevention,
            self.color_gradient,
            self.gray_scale_bars,
            self.resolution_test,
            self.phosphor_persistence_test
        ]
        self.pattern_names = [
            "SMPTE Color Bars",
            "Convergence Grid",
            "Linearity Grid",
            "Focus Pattern",
            "Purity Test",
            "Contrast/Brightness",
            "Geometry Test",
            "Moiré Test",
            "Dot Pitch Test",
            "Refresh Rate Test",
            "Burn-in Prevention",
            "Color Gradients",
            "Gray Scale Bars",
            "Resolution Test",
            "Phosphor Persistence"
        ]
        self.running = True
        self.show_info = True
        self.grid_size = 50
        self.purity_color_index = 0
        self.purity_colors = [WHITE, RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW]
        
    def draw_logo(self, x=None, y=None):
        """Draw NEONpulseTechshop logo"""
        if x is None:
            x = self.width // 2
        if y is None:
            y = 50
            
        # NEON text
        neon_text = self.font.render("NEON", True, NEON_MAGENTA)
        neon_rect = neon_text.get_rect()
        
        # pulse text
        pulse_text = self.font.render("pulse", True, NEON_GREEN)
        pulse_rect = pulse_text.get_rect()
        
        # Techshop text
        tech_text = self.small_font.render("TECHSHOP", True, NEON_GREEN)
        tech_rect = tech_text.get_rect()
        
        # Position elements
        total_width = neon_rect.width + pulse_rect.width
        neon_rect.midright = (x - 2, y)
        pulse_rect.midleft = (x + 2, y)
        tech_rect.midtop = (x, y + 25)
        
        # Draw with glow effect
        for offset in range(3, 0, -1):
            alpha = 100 // offset
            neon_glow = self.font.render("NEON", True, (*NEON_MAGENTA, alpha))
            pulse_glow = self.font.render("pulse", True, (*NEON_GREEN, alpha))
            self.screen.blit(neon_glow, (neon_rect.x - offset, neon_rect.y - offset))
            self.screen.blit(pulse_glow, (pulse_rect.x + offset, pulse_rect.y - offset))
        
        self.screen.blit(neon_text, neon_rect)
        self.screen.blit(pulse_text, pulse_rect)
        self.screen.blit(tech_text, tech_rect)
        
        # Website
        website_text = self.small_font.render("neonpulsetechshop.com", True, WHITE)
        website_rect = website_text.get_rect(midtop=(x, y + 50))
        self.screen.blit(website_text, website_rect)
        
    def draw_info(self):
        """Draw pattern info and controls"""
        if not self.show_info:
            return
            
        info_surface = pygame.Surface((400, 200))
        info_surface.set_alpha(200)
        info_surface.fill(BLACK)
        
        # Pattern name
        name_text = self.small_font.render(self.pattern_names[self.current_pattern], True, WHITE)
        info_surface.blit(name_text, (10, 10))
        
        # Controls
        controls = [
            "← → : Change Pattern",
            "I : Toggle Info",
            "G : Adjust Grid Size",
            "C : Cycle Colors (Purity)",
            "ESC : Exit"
        ]
        
        y = 40
        for control in controls:
            control_text = self.small_font.render(control, True, WHITE)
            info_surface.blit(control_text, (10, y))
            y += 25
            
        # Resolution info
        res_text = self.small_font.render(f"Resolution: {self.width}x{self.height}", True, NEON_GREEN)
        info_surface.blit(res_text, (10, 170))
        
        self.screen.blit(info_surface, (10, 10))
        
    def smpte_color_bars(self):
        """SMPTE standard color bars"""
        self.screen.fill(BLACK)
        
        # Main color bars (75% intensity)
        bar_width = self.width // 7
        colors_75 = [
            (192, 192, 192),  # 75% white
            (192, 192, 0),    # yellow
            (0, 192, 192),    # cyan
            (0, 192, 0),      # green
            (192, 0, 192),    # magenta
            (192, 0, 0),      # red
            (0, 0, 192)       # blue
        ]
        
        # Draw main bars (2/3 height)
        main_height = int(self.height * 2/3)
        for i, color in enumerate(colors_75):
            pygame.draw.rect(self.screen, color, 
                           (i * bar_width, 0, bar_width, main_height))
        
        # Draw reverse bars
        reverse_height = int(self.height * 1/12)
        reverse_colors = [BLUE, BLACK, MAGENTA, BLACK, CYAN, BLACK, WHITE]
        for i, color in enumerate(reverse_colors):
            pygame.draw.rect(self.screen, color,
                           (i * bar_width, main_height, bar_width, reverse_height))
        
        # PLUGE section
        pluge_y = main_height + reverse_height
        pluge_height = int(self.height * 1/12)
        
        # Super black, black, super white
        pluge_width = self.width // 3
        pygame.draw.rect(self.screen, (7, 7, 7), (0, pluge_y, pluge_width, pluge_height))
        pygame.draw.rect(self.screen, (16, 16, 16), (pluge_width, pluge_y, pluge_width, pluge_height))
        pygame.draw.rect(self.screen, (29, 29, 29), (pluge_width * 2, pluge_y, pluge_width, pluge_height))
        
        # Grayscale gradient
        gray_y = pluge_y + pluge_height
        gray_height = self.height - gray_y
        for x in range(self.width):
            gray_value = int(255 * x / self.width)
            pygame.draw.line(self.screen, (gray_value, gray_value, gray_value),
                           (x, gray_y), (x, self.height))
        
        self.draw_logo()
        self.draw_info()
        
    def convergence_grid(self):
        """Convergence test pattern - fine grid with crosshairs"""
        self.screen.fill(BLACK)
        
        # Fine grid
        grid_spacing = 20
        
        # White grid lines
        for x in range(0, self.width, grid_spacing):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, grid_spacing):
            pygame.draw.line(self.screen, WHITE, (0, y), (self.width, y), 1)
            
        # Center crosshairs with color separation
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Red horizontal
        pygame.draw.line(self.screen, RED, (center_x - 100, center_y - 1), 
                        (center_x + 100, center_y - 1), 1)
        # Green center
        pygame.draw.line(self.screen, GREEN, (center_x - 100, center_y), 
                        (center_x + 100, center_y), 1)
        # Blue horizontal
        pygame.draw.line(self.screen, BLUE, (center_x - 100, center_y + 1), 
                        (center_x + 100, center_y + 1), 1)
        
        # Vertical lines
        pygame.draw.line(self.screen, RED, (center_x - 1, center_y - 100), 
                        (center_x - 1, center_y + 100), 1)
        pygame.draw.line(self.screen, GREEN, (center_x, center_y - 100), 
                        (center_x, center_y + 100), 1)
        pygame.draw.line(self.screen, BLUE, (center_x + 1, center_y - 100), 
                        (center_x + 1, center_y + 100), 1)
        
        # Corner convergence patterns
        corners = [
            (50, 50), (self.width - 50, 50),
            (50, self.height - 50), (self.width - 50, self.height - 50)
        ]
        
        for cx, cy in corners:
            # Draw RGB separated circles
            pygame.draw.circle(self.screen, RED, (cx - 2, cy), 20, 1)
            pygame.draw.circle(self.screen, GREEN, (cx, cy), 20, 1)
            pygame.draw.circle(self.screen, BLUE, (cx + 2, cy), 20, 1)
            
        self.draw_logo()
        self.draw_info()
        
    def linearity_grid(self):
        """Linearity test - evenly spaced grid"""
        self.screen.fill(BLACK)
        
        # Adjustable grid
        spacing = self.grid_size
        
        # Draw grid
        for x in range(spacing, self.width, spacing):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, self.height), 1)
        for y in range(spacing, self.height, spacing):
            pygame.draw.line(self.screen, WHITE, (0, y), (self.width, y), 1)
            
        # Draw circles at intersections for better linearity check
        for x in range(spacing, self.width, spacing * 4):
            for y in range(spacing, self.height, spacing * 4):
                pygame.draw.circle(self.screen, WHITE, (x, y), 5, 1)
                
        # Draw diagonal lines for aspect ratio check
        pygame.draw.line(self.screen, NEON_GREEN, (0, 0), (self.width, self.height), 1)
        pygame.draw.line(self.screen, NEON_GREEN, (self.width, 0), (0, self.height), 1)
        
        self.draw_logo()
        self.draw_info()
        
    def focus_pattern(self):
        """Focus test pattern with fine details"""
        self.screen.fill(BLACK)
        
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Concentric circles
        for radius in range(20, min(self.width, self.height) // 2, 40):
            pygame.draw.circle(self.screen, WHITE, (center_x, center_y), radius, 1)
            
        # Fine line patterns
        # Horizontal lines
        for y in range(center_y - 100, center_y + 100, 2):
            pygame.draw.line(self.screen, WHITE, (center_x - 150, y), (center_x + 150, y), 1)
            
        # Vertical lines
        for x in range(center_x - 100, center_x + 100, 2):
            pygame.draw.line(self.screen, WHITE, (x, center_y - 150), (x, center_y + 150), 1)
            
        # Corner focus patterns
        pattern_size = 100
        corners = [
            (pattern_size, pattern_size),
            (self.width - pattern_size, pattern_size),
            (pattern_size, self.height - pattern_size),
            (self.width - pattern_size, self.height - pattern_size)
        ]
        
        for cx, cy in corners:
            # Draw fine radial lines
            for angle in range(0, 360, 10):
                rad = math.radians(angle)
                x1 = cx + int(20 * math.cos(rad))
                y1 = cy + int(20 * math.sin(rad))
                x2 = cx + int(60 * math.cos(rad))
                y2 = cy + int(60 * math.sin(rad))
                pygame.draw.line(self.screen, WHITE, (x1, y1), (x2, y2), 1)
                
        # Resolution test text
        test_text = "1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, size in enumerate([8, 10, 12, 14, 16, 18, 20]):
            font = pygame.font.Font(None, size)
            text = font.render(test_text, True, WHITE)
            self.screen.blit(text, (50, 300 + i * 25))
            
        self.draw_logo()
        self.draw_info()
        
    def purity_test(self):
        """Color purity test - full screen single colors"""
        color = self.purity_colors[self.purity_color_index]
        self.screen.fill(color)
        
        # Add subtle grid for geometry reference
        if color != BLACK:
            for x in range(0, self.width, 100):
                pygame.draw.line(self.screen, BLACK, (x, 0), (x, self.height), 1)
            for y in range(0, self.height, 100):
                pygame.draw.line(self.screen, BLACK, (0, y), (self.width, y), 1)
                
        # Color name
        color_names = ["WHITE", "RED", "GREEN", "BLUE", "CYAN", "MAGENTA", "YELLOW"]
        name_text = self.font.render(color_names[self.purity_color_index], True, BLACK if color == WHITE else WHITE)
        name_rect = name_text.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(name_text, name_rect)
        
        self.draw_info()
        
    def contrast_brightness(self):
        """Contrast and brightness calibration pattern"""
        self.screen.fill(GRAY)
        
        # PLUGE pattern for black level
        pluge_height = 100
        pluge_y = self.height // 2 - 200
        
        # Draw PLUGE bars
        bar_width = self.width // 5
        pluge_values = [0, 5, 10, 15, 20]  # Black levels
        
        for i, value in enumerate(pluge_values):
            color = (value, value, value)
            pygame.draw.rect(self.screen, color, 
                           (i * bar_width, pluge_y, bar_width, pluge_height))
            
        # Label
        label = self.small_font.render("PLUGE - Adjust brightness until leftmost bars merge", True, WHITE)
        self.screen.blit(label, (50, pluge_y - 30))
        
        # White level bars
        white_y = self.height // 2 + 50
        white_values = [235, 240, 245, 250, 255]  # Near white levels
        
        for i, value in enumerate(white_values):
            color = (value, value, value)
            pygame.draw.rect(self.screen, color,
                           (i * bar_width, white_y, bar_width, pluge_height))
            
        # Label
        label = self.small_font.render("Adjust contrast until rightmost bars are distinguishable", True, BLACK)
        self.screen.blit(label, (50, white_y + pluge_height + 10))
        
        self.draw_logo()
        self.draw_info()
        
    def geometry_test(self):
        """Geometry test pattern"""
        self.screen.fill(BLACK)
        
        # Outer border
        pygame.draw.rect(self.screen, WHITE, (5, 5, self.width - 10, self.height - 10), 2)
        
        # Center cross
        pygame.draw.line(self.screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height), 1)
        pygame.draw.line(self.screen, WHITE, (0, self.height // 2), (self.width, self.height // 2), 1)
        
        # Circle for pincushion/barrel check
        radius = min(self.width, self.height) // 2 - 20
        pygame.draw.circle(self.screen, WHITE, (self.width // 2, self.height // 2), radius, 2)
        
        # Corner markers
        marker_size = 50
        corners = [
            (0, 0), (self.width - marker_size, 0),
            (0, self.height - marker_size), (self.width - marker_size, self.height - marker_size)
        ]
        
        for x, y in corners:
            # L-shaped markers
            if x == 0:
                pygame.draw.line(self.screen, NEON_GREEN, (x, y), (x + marker_size, y), 2)
                pygame.draw.line(self.screen, NEON_GREEN, (x, y), (x, y + marker_size if y == 0 else y), 2)
            else:
                pygame.draw.line(self.screen, NEON_GREEN, (x, y), (x + marker_size, y), 2)
                pygame.draw.line(self.screen, NEON_GREEN, (x + marker_size, y), 
                               (x + marker_size, y + marker_size if y == 0 else y), 2)
                
        self.draw_logo()
        self.draw_info()
        
    def moire_test(self):
        """Moiré pattern test"""
        self.screen.fill(BLACK)
        
        # Fine vertical lines
        for x in range(0, self.width, 2):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, self.height // 2), 1)
            
        # Fine horizontal lines
        for y in range(self.height // 2, self.height, 2):
            pygame.draw.line(self.screen, WHITE, (0, y), (self.width, y), 1)
            
        # Instructions
        text = self.small_font.render("Adjust monitor settings to minimize moiré patterns", True, NEON_GREEN)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        
        # Black background for text
        pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 10))
        self.screen.blit(text, text_rect)
        
        self.draw_info()
        
    def dot_pitch_test(self):
        """Dot pitch visualization test"""
        self.screen.fill(BLACK)
        
        # Draw RGB dot pattern
        dot_size = 2
        spacing = 6
        
        for y in range(0, self.height, spacing):
            for x in range(0, self.width, spacing * 3):
                # RGB triplet
                pygame.draw.circle(self.screen, RED, (x, y), dot_size)
                pygame.draw.circle(self.screen, GREEN, (x + spacing, y), dot_size)
                pygame.draw.circle(self.screen, BLUE, (x + spacing * 2, y), dot_size)
                
        self.draw_logo()
        self.draw_info()
        
    def refresh_rate_test(self):
        """Refresh rate test with motion"""
        self.screen.fill(BLACK)
        
        # Moving vertical bar
        time = pygame.time.get_ticks() / 1000.0
        bar_x = int((math.sin(time) + 1) * self.width / 2)
        
        pygame.draw.rect(self.screen, WHITE, (bar_x - 10, 0, 20, self.height))
        
        # Info text
        info_text = [
            "Refresh Rate Test",
            "Watch for tearing or stuttering",
            "Smooth motion indicates proper refresh rate"
        ]
        
        y = self.height // 2 - 50
        for line in info_text:
            text = self.small_font.render(line, True, NEON_GREEN)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 30
            
        self.draw_info()
        
    def burn_in_prevention(self):
        """Anti burn-in pattern with moving elements"""
        self.screen.fill(BLACK)
        
        time = pygame.time.get_ticks() / 1000.0
        
        # Moving circles
        for i in range(5):
            phase = i * math.pi / 2.5
            x = int((math.sin(time + phase) + 1) * self.width / 2)
            y = int((math.cos(time * 0.7 + phase) + 1) * self.height / 2)
            color = self.purity_colors[i % len(self.purity_colors)]
            pygame.draw.circle(self.screen, color, (x, y), 50, 2)
            
        # Moving logo
        logo_x = int((math.sin(time * 0.5) + 1) * (self.width - 200) / 2 + 100)
        logo_y = int((math.cos(time * 0.3) + 1) * (self.height - 100) / 2 + 50)
        self.draw_logo(logo_x, logo_y)
        
        # Info
        text = self.small_font.render("Burn-in Prevention Pattern", True, WHITE)
        self.screen.blit(text, (10, 10))
        
    def color_gradient(self):
        """Color gradient test"""
        self.screen.fill(BLACK)
        
        # RGB gradients
        gradient_height = self.height // 4
        
        # Red gradient
        for x in range(self.width):
            red_value = int(255 * x / self.width)
            pygame.draw.line(self.screen, (red_value, 0, 0), (x, 0), (x, gradient_height))
            
        # Green gradient
        for x in range(self.width):
            green_value = int(255 * x / self.width)
            pygame.draw.line(self.screen, (0, green_value, 0), (x, gradient_height), (x, gradient_height * 2))
            
        # Blue gradient
        for x in range(self.width):
            blue_value = int(255 * x / self.width)
            pygame.draw.line(self.screen, (0, 0, blue_value), (x, gradient_height * 2), (x, gradient_height * 3))
            
        # Gray gradient
        for x in range(self.width):
            gray_value = int(255 * x / self.width)
            pygame.draw.line(self.screen, (gray_value, gray_value, gray_value), 
                           (x, gradient_height * 3), (x, self.height))
            
        self.draw_logo()
        self.draw_info()
        
    def gray_scale_bars(self):
        """16-step grayscale bars"""
        self.screen.fill(BLACK)
        
        steps = 16
        bar_width = self.width // steps
        
        for i in range(steps):
            gray_value = int(255 * i / (steps - 1))
            color = (gray_value, gray_value, gray_value)
            pygame.draw.rect(self.screen, color, (i * bar_width, 0, bar_width, self.height))
            
            # Label each bar
            label = self.small_font.render(str(gray_value), True, 
                                         BLACK if gray_value > 127 else WHITE)
            label_rect = label.get_rect(center=(i * bar_width + bar_width // 2, self.height - 30))
            self.screen.blit(label, label_rect)
            
        self.draw_logo()
        self.draw_info()
        
    def resolution_test(self):
        """Resolution and sharpness test"""
        self.screen.fill(BLACK)
        
        # One pixel lines
        for y in range(100, 200, 2):
            pygame.draw.line(self.screen, WHITE, (50, y), (self.width - 50, y), 1)
            
        # One pixel checkerboard
        checker_size = 100
        checker_x = self.width // 2 - checker_size // 2
        checker_y = 250
        
        for y in range(checker_size):
            for x in range(checker_size):
                if (x + y) % 2 == 0:
                    self.screen.set_at((checker_x + x, checker_y + y), WHITE)
                    
        # Resolution info
        res_text = self.font.render(f"{self.width} × {self.height}", True, NEON_GREEN)
        res_rect = res_text.get_rect(center=(self.width // 2, 400))
        self.screen.blit(res_text, res_rect)
        
        # Pixel perfect text samples
        sizes = [8, 9, 10, 11, 12]
        y = 450
        for size in sizes:
            font = pygame.font.Font(None, size)
            text = font.render(f"{size}pt: The quick brown fox jumps over the lazy dog", True, WHITE)
            self.screen.blit(text, (50, y))
            y += size + 5
            
        self.draw_logo()
        self.draw_info()
        
    def phosphor_persistence_test(self):
        """Phosphor persistence / ghosting test"""
        self.screen.fill(BLACK)
        
        time = pygame.time.get_ticks() / 1000.0
        
        # Moving white box on black
        box_size = 100
        x = int((math.sin(time * 2) + 1) * (self.width - box_size) / 2)
        y = self.height // 3
        
        pygame.draw.rect(self.screen, WHITE, (x, y, box_size, box_size))
        
        # Moving black box on white
        y2 = self.height * 2 // 3 - box_size
        pygame.draw.rect(self.screen, WHITE, (0, y2, self.width, box_size + 20))
        x2 = int((math.sin(time * 2 + math.pi) + 1) * (self.width - box_size) / 2)
        pygame.draw.rect(self.screen, BLACK, (x2, y2 + 10, box_size, box_size))
        
        # Instructions
        text = self.small_font.render("Watch for ghosting or phosphor trails", True, NEON_GREEN)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        
        self.draw_info()
        
    def handle_events(self):
        """Handle keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RIGHT:
                    self.current_pattern = (self.current_pattern + 1) % len(self.patterns)
                elif event.key == pygame.K_LEFT:
                    self.current_pattern = (self.current_pattern - 1) % len(self.patterns)
                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info
                elif event.key == pygame.K_g:
                    # Adjust grid size
                    self.grid_size = 25 if self.grid_size >= 100 else self.grid_size + 25
                elif event.key == pygame.K_c:
                    # Cycle purity colors
                    self.purity_color_index = (self.purity_color_index + 1) % len(self.purity_colors)
                    
    def run(self):
        """Main loop"""
        while self.running:
            self.handle_events()
            self.patterns[self.current_pattern]()
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

def select_resolution():
    """Display resolution selection menu"""
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Select Resolution")
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    tiny_font = pygame.font.Font(None, 18)
    clock = pygame.time.Clock()
    
    running = True
    selected = None
    
    # Resolution categories
    categories = {
        "Legacy CRT": ['1', '2', '3', '4', '5'],
        "Modern Displays": ['6', '7', '8', '9']
    }
    
    while running and selected is None:
        screen.fill(BLACK)
        
        # Title
        title = font.render("NEONpulseTechshop Monitor Test Suite", True, NEON_MAGENTA)
        title_rect = title.get_rect(center=(400, 40))
        screen.blit(title, title_rect)
        
        subtitle = small_font.render("Select Resolution:", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(400, 80))
        screen.blit(subtitle, subtitle_rect)
        
        # Resolution options by category
        y = 120
        for category, keys in categories.items():
            # Category header
            cat_text = small_font.render(category, True, NEON_GREEN)
            screen.blit(cat_text, (200, y))
            y += 30
            
            # Resolution options in category
            for key in keys:
                res = RESOLUTIONS[key]
                text = f"{key}. {res[0]}×{res[1]}"
                
                # Add labels for common names
                if res == (1920, 1080):
                    text += " (Full HD)"
                elif res == (2560, 1440):
                    text += " (2K/QHD)"
                elif res == (3840, 2160):
                    text += " (4K/UHD)"
                elif res == (7680, 4320):
                    text += " (8K)"
                    
                # Highlight common resolutions
                if res in [(1024, 768), (1920, 1080), (3840, 2160)]:
                    color = WHITE
                    text += " ★"
                else:
                    color = (200, 200, 200)
                    
                option = small_font.render(text, True, color)
                screen.blit(option, (250, y))
                y += 25
            
            y += 15  # Space between categories
            
        # Instructions
        inst = small_font.render("Press number key (1-9) or ESC to exit", True, WHITE)
        inst_rect = inst.get_rect(center=(400, 500))
        screen.blit(inst, inst_rect)
        
        # Warning for high resolutions
        warning = tiny_font.render("Note: 4K/8K may require significant system resources", True, YELLOW)
        warning_rect = warning.get_rect(center=(400, 530))
        screen.blit(warning, warning_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    key = str(event.key - pygame.K_0)
                    if key in RESOLUTIONS:
                        selected = RESOLUTIONS[key]
                        
        pygame.display.flip()
        clock.tick(30)
        
    if selected:
        return selected
    else:
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    resolution = select_resolution()
    test_suite = CRTTestSuite(resolution)
    test_suite.run()

if __name__ == "__main__":
    main()