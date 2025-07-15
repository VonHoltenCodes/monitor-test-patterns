#!/usr/bin/env python3
"""
NEONpulseTechshop HDR Test Pattern Suite
High Dynamic Range display testing patterns
"""

import pygame
import numpy as np
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

# HDR Standards
HDR_MODES = {
    'HDR10': {
        'max_nits': 10000,
        'bit_depth': 10,
        'color_space': 'rec2020',
        'eotf': 'PQ'
    },
    'HDR10+': {
        'max_nits': 10000,
        'bit_depth': 10,
        'color_space': 'rec2020',
        'eotf': 'PQ',
        'dynamic_metadata': True
    },
    'Dolby Vision': {
        'max_nits': 10000,
        'bit_depth': 12,
        'color_space': 'rec2020',
        'eotf': 'PQ',
        'dynamic_metadata': True
    },
    'HLG': {
        'max_nits': 1000,
        'bit_depth': 10,
        'color_space': 'rec2020',
        'eotf': 'HLG'
    }
}

class HDRTestSuite:
    def __init__(self, resolution=(3840, 2160), hdr_mode='HDR10'):
        self.width, self.height = resolution
        self.hdr_mode = hdr_mode
        self.hdr_config = HDR_MODES[hdr_mode]
        
        # Try to create HDR surface
        try:
            # Set up for HDR display
            os.environ['SDL_VIDEO_ALLOW_SCREENSAVER'] = '1'
            self.screen = pygame.display.set_mode(
                (self.width, self.height), 
                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
            pygame.display.set_caption(f"NEONpulseTechshop HDR Test Suite - {hdr_mode}")
        except:
            print("Warning: HDR display mode not available, falling back to SDR")
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.current_pattern = 0
        self.peak_nits = 1000
        self.show_info = True
        
        self.patterns = [
            self.peak_brightness_test,
            self.gradient_ramp_test,
            self.color_volume_test,
            self.black_level_test,
            self.highlight_detail_test,
            self.color_gamut_test,
            self.tone_mapping_test,
            self.clipping_test,
            self.pq_curve_visualization,
            self.hdr_color_checker
        ]
        
        self.pattern_names = [
            "Peak Brightness Windows",
            "10-bit Gradient Ramp",
            "Color Volume Test",
            "Black Level Detail",
            "Highlight Roll-off",
            "Rec.2020 Color Gamut",
            "SDR to HDR Tone Mapping",
            "Clipping Detection",
            "PQ Curve Visualization",
            "HDR Color Checker"
        ]
        
        self.running = True
        
    def nits_to_pq(self, nits):
        """Convert nits to PQ (Perceptual Quantizer) value"""
        m1 = 0.1593017578125
        m2 = 78.84375
        c1 = 0.8359375
        c2 = 18.8515625
        c3 = 18.6875
        
        y = nits / 10000.0
        pq = np.power((c1 + c2 * np.power(y, m1)) / (1 + c3 * np.power(y, m1)), m2)
        return np.clip(pq, 0, 1)
        
    def pq_to_linear(self, pq):
        """Convert PQ value to linear light"""
        m1 = 0.1593017578125
        m2 = 78.84375
        c1 = 0.8359375
        c2 = 18.8515625
        c3 = 18.6875
        
        pq_pow = np.power(pq, 1.0 / m2)
        y = np.power((pq_pow - c1) / (c2 - c3 * pq_pow), 1.0 / m1)
        return y * 10000.0
        
    def get_hdr_color(self, nits, color=(1, 1, 1)):
        """Convert nits value to displayable color"""
        pq = self.nits_to_pq(nits)
        # Convert to 8-bit for display (will be tone-mapped by display)
        value = int(pq * 255)
        return (
            int(value * color[0]),
            int(value * color[1]),
            int(value * color[2])
        )
        
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
        
        # HDR indicator
        hdr_text = self.small_font.render(f"HDR {self.hdr_mode}", True, WHITE)
        hdr_rect = hdr_text.get_rect()
        
        # Position elements
        neon_rect.midright = (x - 2, y)
        pulse_rect.midleft = (x + 2, y)
        hdr_rect.midtop = (x, y + 25)
        
        self.screen.blit(neon_text, neon_rect)
        self.screen.blit(pulse_text, pulse_rect)
        self.screen.blit(hdr_text, hdr_rect)
        
    def draw_info(self):
        """Draw pattern info and controls"""
        if not self.show_info:
            return
            
        info_surface = pygame.Surface((500, 250))
        info_surface.set_alpha(200)
        info_surface.fill(BLACK)
        
        # Pattern name
        name_text = self.small_font.render(self.pattern_names[self.current_pattern], True, WHITE)
        info_surface.blit(name_text, (10, 10))
        
        # HDR info
        hdr_info = [
            f"Mode: {self.hdr_mode}",
            f"Peak: {self.peak_nits} nits",
            f"Bit Depth: {self.hdr_config['bit_depth']}-bit",
            f"Color Space: {self.hdr_config['color_space'].upper()}"
        ]
        
        y = 40
        for info in hdr_info:
            info_text = self.small_font.render(info, True, NEON_GREEN)
            info_surface.blit(info_text, (10, y))
            y += 25
            
        # Controls
        controls = [
            "← → : Change Pattern",
            "↑ ↓ : Adjust Peak Brightness",
            "I : Toggle Info",
            "ESC : Exit"
        ]
        
        y = 140
        for control in controls:
            control_text = self.small_font.render(control, True, WHITE)
            info_surface.blit(control_text, (10, y))
            y += 25
            
        self.screen.blit(info_surface, (10, 10))
        
    def peak_brightness_test(self):
        """Test display's peak brightness capabilities"""
        self.screen.fill(BLACK)
        
        # Different window sizes for peak brightness testing
        windows = [
            (1, self.peak_nits),      # 1% window
            (2, self.peak_nits * 0.9), # 2% window
            (5, self.peak_nits * 0.8), # 5% window
            (10, self.peak_nits * 0.7), # 10% window
            (25, self.peak_nits * 0.6), # 25% window
            (50, self.peak_nits * 0.5), # 50% window
            (100, self.peak_nits * 0.4) # 100% window
        ]
        
        spacing = self.width // (len(windows) + 1)
        
        for i, (percent, nits) in enumerate(windows):
            x = spacing * (i + 1)
            size = int((self.height * 0.6) * (percent / 100))
            
            # Draw window
            color = self.get_hdr_color(nits)
            rect = pygame.Rect(x - size // 2, self.height // 2 - size // 2, size, size)
            pygame.draw.rect(self.screen, color, rect)
            
            # Label
            label = f"{percent}%"
            nits_label = f"{int(nits)} nits"
            
            label_text = self.small_font.render(label, True, WHITE)
            nits_text = self.small_font.render(nits_label, True, WHITE)
            
            label_rect = label_text.get_rect(centerx=x, y=self.height // 2 + size // 2 + 20)
            nits_rect = nits_text.get_rect(centerx=x, y=self.height // 2 + size // 2 + 45)
            
            self.screen.blit(label_text, label_rect)
            self.screen.blit(nits_text, nits_rect)
            
        self.draw_logo()
        self.draw_info()
        
    def gradient_ramp_test(self):
        """10-bit gradient test for smooth transitions"""
        self.screen.fill(BLACK)
        
        # Create gradient surface
        gradient_height = self.height // 2
        
        # Horizontal gradient
        for x in range(self.width):
            nits = (x / self.width) * self.peak_nits
            color = self.get_hdr_color(nits)
            pygame.draw.line(self.screen, color, (x, 0), (x, gradient_height))
            
        # Step wedge for banding detection
        steps = 64
        step_height = self.height // 4
        step_width = self.width // steps
        
        for i in range(steps):
            nits = (i / (steps - 1)) * self.peak_nits
            color = self.get_hdr_color(nits)
            rect = pygame.Rect(i * step_width, gradient_height + 50, step_width, step_height)
            pygame.draw.rect(self.screen, color, rect)
            
        # Labels
        label_text = self.small_font.render("Smooth Gradient (10-bit)", True, WHITE)
        self.screen.blit(label_text, (10, gradient_height + 10))
        
        step_text = self.small_font.render("Step Wedge (Banding Test)", True, WHITE)
        self.screen.blit(step_text, (10, gradient_height + step_height + 60))
        
        self.draw_logo()
        self.draw_info()
        
    def color_volume_test(self):
        """Test color reproduction at different brightness levels"""
        self.screen.fill(BLACK)
        
        # Rec.2020 primaries
        colors = [
            ("Red", (1, 0, 0)),
            ("Green", (0, 1, 0)),
            ("Blue", (0, 0, 1)),
            ("Cyan", (0, 1, 1)),
            ("Magenta", (1, 0, 1)),
            ("Yellow", (1, 1, 0))
        ]
        
        # Brightness levels
        brightness_levels = [0.1, 0.25, 0.5, 0.75, 1.0]
        
        cell_width = self.width // len(colors)
        cell_height = self.height // (len(brightness_levels) + 1)
        
        for row, brightness in enumerate(brightness_levels):
            nits = brightness * self.peak_nits
            
            for col, (name, base_color) in enumerate(colors):
                color = self.get_hdr_color(nits, base_color)
                rect = pygame.Rect(
                    col * cell_width + 2,
                    row * cell_height + 2,
                    cell_width - 4,
                    cell_height - 4
                )
                pygame.draw.rect(self.screen, color, rect)
                
                # Add color name in middle row
                if row == 2:
                    text_color = BLACK if brightness > 0.5 else WHITE
                    name_text = self.small_font.render(name, True, text_color)
                    name_rect = name_text.get_rect(center=rect.center)
                    self.screen.blit(name_text, name_rect)
                    
            # Row label
            nits_text = self.small_font.render(f"{int(nits)} nits", True, WHITE)
            self.screen.blit(nits_text, (self.width - 100, row * cell_height + cell_height // 2))
            
        self.draw_logo()
        self.draw_info()
        
    def black_level_test(self):
        """Test near-black detail visibility"""
        self.screen.fill(BLACK)
        
        # Near-black squares
        squares = 15
        square_size = min(self.width, self.height) // (squares + 2)
        start_x = (self.width - squares * square_size) // 2
        start_y = self.height // 3
        
        for i in range(squares):
            # Range from 0 to 50 nits
            nits = (i / (squares - 1)) * 50
            color = self.get_hdr_color(nits)
            
            rect = pygame.Rect(
                start_x + i * square_size,
                start_y,
                square_size - 2,
                square_size
            )
            pygame.draw.rect(self.screen, color, rect)
            
            # Label
            if i % 3 == 0:
                label_color = WHITE if nits < 25 else BLACK
                label = f"{int(nits)}"
                label_text = self.small_font.render(label, True, label_color)
                label_rect = label_text.get_rect(center=(rect.centerx, rect.centery))
                self.screen.blit(label_text, label_rect)
                
        # PLUGE pattern
        pluge_y = start_y + square_size + 50
        pluge_height = self.height // 4
        pluge_values = [0, 0.1, 0.5, 1, 2, 5, 10]
        pluge_width = self.width // len(pluge_values)
        
        for i, nits in enumerate(pluge_values):
            color = self.get_hdr_color(nits)
            rect = pygame.Rect(i * pluge_width, pluge_y, pluge_width - 2, pluge_height)
            pygame.draw.rect(self.screen, color, rect)
            
            # Label
            label_text = self.small_font.render(f"{nits} nit", True, WHITE)
            label_rect = label_text.get_rect(centerx=rect.centerx, y=pluge_y - 25)
            self.screen.blit(label_text, label_rect)
            
        self.draw_logo()
        self.draw_info()
        
    def highlight_detail_test(self):
        """Test highlight detail preservation"""
        self.screen.fill(BLACK)
        
        # Concentric circles with subtle brightness differences
        center_x = self.width // 2
        center_y = self.height // 2
        max_radius = min(self.width, self.height) // 3
        circles = 20
        
        for i in range(circles):
            radius = max_radius * (1 - i / circles)
            # Brightness from 70% to 100% of peak
            brightness_ratio = 0.7 + (0.3 * i / circles)
            nits = self.peak_nits * brightness_ratio
            color = self.get_hdr_color(nits)
            
            pygame.draw.circle(self.screen, color, (center_x, center_y), int(radius))
            
        # Fine detail checkerboard in center
        checker_size = 100
        pixel_size = 2
        
        for y in range(0, checker_size, pixel_size):
            for x in range(0, checker_size, pixel_size):
                if (x // pixel_size + y // pixel_size) % 2 == 0:
                    nits = self.peak_nits * 0.9
                else:
                    nits = self.peak_nits * 0.95
                    
                color = self.get_hdr_color(nits)
                rect = pygame.Rect(
                    center_x - checker_size // 2 + x,
                    center_y - checker_size // 2 + y,
                    pixel_size,
                    pixel_size
                )
                pygame.draw.rect(self.screen, color, rect)
                
        self.draw_logo()
        self.draw_info()
        
    def color_gamut_test(self):
        """Test Rec.2020 color space coverage"""
        self.screen.fill(BLACK)
        
        # Color wheel
        center_x = self.width // 2
        center_y = self.height // 2
        radius = min(self.width, self.height) // 3
        
        # Draw color wheel using Rec.2020 primaries
        for angle in range(360):
            for r in range(0, radius, 2):
                saturation = r / radius
                hue = angle
                
                # Convert HSV to RGB (simplified)
                rgb = self.hsv_to_rgb(hue, saturation, 1.0)
                nits = self.peak_nits * 0.5  # Mid-brightness
                color = self.get_hdr_color(nits, rgb)
                
                x = int(center_x + r * math.cos(math.radians(angle)))
                y = int(center_y + r * math.sin(math.radians(angle)))
                
                self.screen.set_at((x, y), color)
                
        # Draw gamut boundaries
        # Rec.709 boundary (approximate)
        pygame.draw.circle(self.screen, WHITE, (center_x, center_y), int(radius * 0.6), 2)
        
        # Labels
        rec709_text = self.small_font.render("Rec.709", True, WHITE)
        rec709_rect = rec709_text.get_rect(centerx=center_x, y=center_y + int(radius * 0.6) + 10)
        self.screen.blit(rec709_text, rec709_rect)
        
        rec2020_text = self.small_font.render("Rec.2020", True, WHITE)
        rec2020_rect = rec2020_text.get_rect(centerx=center_x, y=center_y + radius + 10)
        self.screen.blit(rec2020_text, rec2020_rect)
        
        self.draw_logo()
        self.draw_info()
        
    def tone_mapping_test(self):
        """Test SDR to HDR tone mapping"""
        self.screen.fill(BLACK)
        
        # Show same content at different brightness levels
        sections = 4
        section_width = self.width // sections
        
        brightness_levels = [
            ("SDR (100 nits)", 100),
            ("HDR (400 nits)", 400),
            ("HDR (1000 nits)", 1000),
            ("HDR (Peak)", self.peak_nits)
        ]
        
        for i, (label, max_nits) in enumerate(brightness_levels):
            x_start = i * section_width
            
            # Gradient in each section
            for y in range(self.height - 40):
                brightness = y / (self.height - 40)
                nits = brightness * max_nits
                color = self.get_hdr_color(nits)
                
                pygame.draw.line(
                    self.screen,
                    color,
                    (x_start, y),
                    (x_start + section_width - 2, y)
                )
                
            # Label
            label_bg = pygame.Rect(x_start, 0, section_width - 2, 30)
            pygame.draw.rect(self.screen, BLACK, label_bg)
            
            label_text = self.small_font.render(label, True, WHITE)
            label_rect = label_text.get_rect(centerx=x_start + section_width // 2, y=10)
            self.screen.blit(label_text, label_rect)
            
        self.draw_logo()
        self.draw_info()
        
    def clipping_test(self):
        """Test for highlight and shadow clipping"""
        self.screen.fill(BLACK)
        
        # Draw bars from 0 to beyond peak brightness
        bars = 20
        bar_width = self.width // bars
        bar_height = int(self.height * 0.7)
        start_y = (self.height - bar_height) // 2
        
        for i in range(bars):
            # Go up to 120% of peak to test clipping
            nits = (i / (bars - 1)) * self.peak_nits * 1.2
            
            # Clamp to display maximum
            display_nits = min(nits, self.hdr_config['max_nits'])
            color = self.get_hdr_color(display_nits)
            
            rect = pygame.Rect(
                i * bar_width + 2,
                start_y,
                bar_width - 4,
                bar_height
            )
            pygame.draw.rect(self.screen, color, rect)
            
            # Clipping indicator
            if nits > self.peak_nits:
                # Flash red border for clipped values
                if pygame.time.get_ticks() % 1000 < 500:
                    pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
                    
            # Label
            label_color = BLACK if display_nits > self.peak_nits * 0.5 else WHITE
            label = f"{int(nits)}"
            label_text = self.small_font.render(label, True, label_color)
            label_rect = label_text.get_rect(
                centerx=rect.centerx,
                bottom=rect.bottom - 10
            )
            
            # Rotate label
            label_surface = pygame.Surface((label_text.get_width(), label_text.get_height()))
            label_surface.fill(color)
            label_surface.blit(label_text, (0, 0))
            label_rotated = pygame.transform.rotate(label_surface, 90)
            
            self.screen.blit(label_rotated, (rect.centerx - 10, rect.bottom - 80))
            
        self.draw_logo()
        self.draw_info()
        
    def pq_curve_visualization(self):
        """Visualize the PQ transfer function"""
        self.screen.fill(BLACK)
        
        # Graph area
        margin = 80
        graph_width = self.width - 2 * margin
        graph_height = self.height - 2 * margin
        
        # Draw axes
        pygame.draw.line(self.screen, WHITE, 
                        (margin, self.height - margin),
                        (self.width - margin, self.height - margin), 2)
        pygame.draw.line(self.screen, WHITE,
                        (margin, margin),
                        (margin, self.height - margin), 2)
                        
        # Draw PQ curve
        points = []
        for x in range(graph_width):
            nits = (x / graph_width) * 10000
            pq = self.nits_to_pq(nits)
            y = graph_height - (pq * graph_height)
            points.append((margin + x, margin + y))
            
        if len(points) > 1:
            pygame.draw.lines(self.screen, NEON_GREEN, False, points, 3)
            
        # Reference points
        references = [100, 400, 1000, 4000, 10000]
        for nits in references:
            x = (nits / 10000) * graph_width
            pq = self.nits_to_pq(nits)
            y = graph_height - (pq * graph_height)
            
            # Vertical line
            pygame.draw.line(self.screen, (100, 100, 100),
                           (margin + x, margin),
                           (margin + x, self.height - margin), 1)
                           
            # Point
            pygame.draw.circle(self.screen, NEON_MAGENTA,
                             (int(margin + x), int(margin + y)), 5)
                             
            # Label
            label_text = self.small_font.render(f"{nits}", True, WHITE)
            label_rect = label_text.get_rect(
                centerx=margin + x,
                y=self.height - margin + 10
            )
            self.screen.blit(label_text, label_rect)
            
        # Axis labels
        x_label = self.font.render("Nits", True, WHITE)
        x_rect = x_label.get_rect(centerx=self.width // 2, y=self.height - 40)
        self.screen.blit(x_label, x_rect)
        
        y_label = self.font.render("PQ Value", True, WHITE)
        y_surface = pygame.transform.rotate(y_label, 90)
        self.screen.blit(y_surface, (20, self.height // 2 - 50))
        
        self.draw_logo()
        self.draw_info()
        
    def hdr_color_checker(self):
        """HDR version of color checker pattern"""
        self.screen.fill(BLACK)
        
        # Extended color patches for HDR
        colors = [
            # Row 1: Skin tones at different exposures
            [(0.94, 0.73, 0.61), (0.76, 0.58, 0.48), (0.58, 0.44, 0.36), (0.40, 0.30, 0.24)],
            # Row 2: Primary colors at peak brightness
            [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0)],
            # Row 3: Secondary colors
            [(1.0, 0.0, 1.0), (0.0, 1.0, 1.0), (1.0, 0.5, 0.0), (0.5, 0.0, 1.0)],
            # Row 4: Grayscale at different nits levels
            [(1.0, 1.0, 1.0), (0.75, 0.75, 0.75), (0.5, 0.5, 0.5), (0.25, 0.25, 0.25)],
            # Row 5: HDR specular highlights
            [(1.0, 0.95, 0.8), (0.9, 0.9, 1.0), (1.0, 0.9, 0.9), (0.95, 1.0, 0.95)]
        ]
        
        # Brightness levels for each row
        row_nits = [200, 1000, 800, 400, self.peak_nits]
        
        rows = len(colors)
        cols = len(colors[0])
        patch_size = min(self.width // (cols + 1), self.height // (rows + 1))
        
        start_x = (self.width - cols * patch_size) // 2
        start_y = (self.height - rows * patch_size) // 2
        
        for row, (row_colors, nits) in enumerate(zip(colors, row_nits)):
            for col, base_color in enumerate(row_colors):
                color = self.get_hdr_color(nits, base_color)
                
                rect = pygame.Rect(
                    start_x + col * patch_size + 2,
                    start_y + row * patch_size + 2,
                    patch_size - 4,
                    patch_size - 4
                )
                pygame.draw.rect(self.screen, color, rect)
                
        # Row labels
        row_labels = ["Skin Tones", "Primaries", "Secondaries", "Grayscale", "Highlights"]
        for i, (label, nits) in enumerate(zip(row_labels, row_nits)):
            label_text = self.small_font.render(f"{label} ({int(nits)} nits)", True, WHITE)
            label_rect = label_text.get_rect(
                right=start_x - 10,
                centery=start_y + i * patch_size + patch_size // 2
            )
            self.screen.blit(label_text, label_rect)
            
        self.draw_logo()
        self.draw_info()
        
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB color space"""
        h = h / 360.0
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        i = i % 6
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q
            
        return (r, g, b)
        
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
                elif event.key == pygame.K_UP:
                    self.peak_nits = min(self.hdr_config['max_nits'], self.peak_nits + 100)
                elif event.key == pygame.K_DOWN:
                    self.peak_nits = max(100, self.peak_nits - 100)
                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info
                    
    def run(self):
        """Main loop"""
        while self.running:
            self.handle_events()
            self.patterns[self.current_pattern]()
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

def select_hdr_mode():
    """Display HDR mode selection menu"""
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Select HDR Mode")
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    
    running = True
    selected = None
    
    while running and selected is None:
        screen.fill(BLACK)
        
        # Title
        title = font.render("NEONpulseTechshop HDR Test Suite", True, NEON_MAGENTA)
        title_rect = title.get_rect(center=(400, 50))
        screen.blit(title, title_rect)
        
        subtitle = small_font.render("Select HDR Mode:", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(400, 100))
        screen.blit(subtitle, subtitle_rect)
        
        # HDR mode options
        y = 150
        modes = list(HDR_MODES.keys())
        
        for i, mode in enumerate(modes, 1):
            config = HDR_MODES[mode]
            text = f"{i}. {mode}"
            detail = f"   Max: {config['max_nits']} nits, {config['bit_depth']}-bit, {config['color_space'].upper()}"
            
            mode_text = small_font.render(text, True, NEON_GREEN)
            detail_text = small_font.render(detail, True, WHITE)
            
            screen.blit(mode_text, (200, y))
            screen.blit(detail_text, (200, y + 25))
            y += 60
            
        # Warning
        warning = small_font.render("⚠️  HDR display and OS HDR support required", True, NEON_MAGENTA)
        warning_rect = warning.get_rect(center=(400, 450))
        screen.blit(warning, warning_rect)
        
        # Instructions
        inst = small_font.render("Press number key or ESC to exit", True, WHITE)
        inst_rect = inst.get_rect(center=(400, 500))
        screen.blit(inst, inst_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key >= pygame.K_1 and event.key <= pygame.K_4:
                    index = event.key - pygame.K_1
                    if index < len(modes):
                        selected = modes[index]
                        
        pygame.display.flip()
        clock.tick(30)
        
    if selected:
        return selected
    else:
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    hdr_mode = select_hdr_mode()
    
    # Default to 4K for HDR testing
    resolution = (3840, 2160)
    
    test_suite = HDRTestSuite(resolution, hdr_mode)
    test_suite.run()

if __name__ == "__main__":
    main()