#!/usr/bin/env python3
"""
NEONpulseTechshop Multi-Monitor Test Suite
Synchronized patterns across multiple displays
"""

import pygame
import sys
import os
import threading
import json
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import time

# Initialize Pygame
pygame.init()

@dataclass
class MonitorInfo:
    """Information about a connected monitor"""
    index: int
    name: str
    resolution: Tuple[int, int]
    position: Tuple[int, int]
    is_primary: bool
    surface: Optional[pygame.Surface] = None


class MultiMonitorTestSuite:
    """Test suite for multiple monitors"""
    
    def __init__(self):
        self.monitors = []
        self.running = True
        self.current_pattern = 0
        self.sync_patterns = True
        self.master_surface = None
        self.show_info = True
        
        # Font setup
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Constants
        self.NEON_GREEN = (0, 255, 65)
        self.NEON_MAGENTA = (255, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Pattern functions
        self.patterns = [
            self.alignment_grid,
            self.bezel_compensation,
            self.color_matching,
            self.individual_patterns,
            self.span_test,
            self.refresh_sync_test,
            self.uniformity_test,
            self.multi_gamma_test
        ]
        
        self.pattern_names = [
            "Monitor Alignment Grid",
            "Bezel Compensation",
            "Color Matching",
            "Individual Patterns",
            "Span Across Monitors",
            "Refresh Rate Sync",
            "Brightness Uniformity",
            "Multi-Monitor Gamma"
        ]
        
    def detect_monitors(self) -> List[MonitorInfo]:
        """Detect connected monitors (simplified)"""
        monitors = []
        
        # For simplicity, we'll simulate multiple monitors
        # In a real implementation, you'd use platform-specific APIs
        
        # Get primary display info
        info = pygame.display.Info()
        primary_width = info.current_w
        primary_height = info.current_h
        
        # Simulate multiple monitors based on screen width
        if primary_width >= 3840:  # Assume dual 1920x1080 or single 4K
            monitors.append(MonitorInfo(
                index=0,
                name="Monitor 1",
                resolution=(1920, 1080),
                position=(0, 0),
                is_primary=True
            ))
            monitors.append(MonitorInfo(
                index=1,
                name="Monitor 2", 
                resolution=(1920, 1080),
                position=(1920, 0),
                is_primary=False
            ))
        else:
            # Single monitor
            monitors.append(MonitorInfo(
                index=0,
                name="Primary Monitor",
                resolution=(primary_width, primary_height),
                position=(0, 0),
                is_primary=True
            ))
            
        return monitors
        
    def initialize(self):
        """Initialize multi-monitor setup"""
        self.monitors = self.detect_monitors()
        
        if not self.monitors:
            print("No monitors detected!")
            return False
            
        print(f"Detected {len(self.monitors)} monitor(s):")
        for monitor in self.monitors:
            print(f"  {monitor.name}: {monitor.resolution[0]}x{monitor.resolution[1]} at {monitor.position}")
            
        # Create surfaces for each monitor
        self._create_monitor_surfaces()
        
        return True
        
    def _create_monitor_surfaces(self):
        """Create pygame surfaces for each monitor"""
        if len(self.monitors) == 1:
            # Single monitor
            monitor = self.monitors[0]
            self.master_surface = pygame.display.set_mode(
                monitor.resolution, 
                pygame.FULLSCREEN
            )
            monitor.surface = self.master_surface
        else:
            # Multiple monitors - create a spanning surface
            total_width = sum(m.resolution[0] for m in self.monitors)
            max_height = max(m.resolution[1] for m in self.monitors)
            
            try:
                self.master_surface = pygame.display.set_mode(
                    (total_width, max_height),
                    pygame.FULLSCREEN | pygame.NOFRAME
                )
                
                # Create subsurfaces for each monitor
                for monitor in self.monitors:
                    x_offset = monitor.position[0]
                    y_offset = monitor.position[1]
                    width, height = monitor.resolution
                    
                    monitor.surface = self.master_surface.subsurface(
                        (x_offset, y_offset, width, height)
                    )
                    
            except Exception as e:
                print(f"Could not create spanning surface: {e}")
                # Fallback to primary monitor only
                primary = self.monitors[0]
                self.master_surface = pygame.display.set_mode(
                    primary.resolution,
                    pygame.FULLSCREEN
                )
                primary.surface = self.master_surface
                self.monitors = [primary]
                
        pygame.display.set_caption("NEONpulseTechshop Multi-Monitor Test Suite")
        
    def alignment_grid(self):
        """Display alignment grids on all monitors"""
        for i, monitor in enumerate(self.monitors):
            if monitor.surface is None:
                continue
                
            surface = monitor.surface
            surface.fill(self.BLACK)
            
            # Draw grid
            grid_size = 50
            width, height = monitor.resolution
            
            # Vertical lines
            for x in range(0, width, grid_size):
                pygame.draw.line(surface, self.WHITE, (x, 0), (x, height), 1)
                
            # Horizontal lines
            for y in range(0, height, grid_size):
                pygame.draw.line(surface, self.WHITE, (0, y), (width, y), 1)
                
            # Center crosshairs
            center_x = width // 2
            center_y = height // 2
            pygame.draw.line(surface, self.NEON_GREEN, 
                           (center_x - 100, center_y), (center_x + 100, center_y), 3)
            pygame.draw.line(surface, self.NEON_GREEN,
                           (center_x, center_y - 100), (center_x, center_y + 100), 3)
                           
            # Corner markers
            marker_size = 50
            pygame.draw.line(surface, self.NEON_MAGENTA, (0, 0), (marker_size, 0), 3)
            pygame.draw.line(surface, self.NEON_MAGENTA, (0, 0), (0, marker_size), 3)
            
            pygame.draw.line(surface, self.NEON_MAGENTA, (width - marker_size, 0), (width, 0), 3)
            pygame.draw.line(surface, self.NEON_MAGENTA, (width, 0), (width, marker_size), 3)
            
            pygame.draw.line(surface, self.NEON_MAGENTA, (0, height - marker_size), (0, height), 3)
            pygame.draw.line(surface, self.NEON_MAGENTA, (0, height), (marker_size, height), 3)
            
            pygame.draw.line(surface, self.NEON_MAGENTA, (width - marker_size, height), (width, height), 3)
            pygame.draw.line(surface, self.NEON_MAGENTA, (width, height - marker_size), (width, height), 3)
            
            # Monitor label
            label = f"Monitor {i + 1}"
            label_text = self.font.render(label, True, self.NEON_GREEN)
            label_rect = label_text.get_rect(center=(center_x, 50))
            surface.blit(label_text, label_rect)
            
            # Resolution info
            res_text = f"{width} × {height}"
            res_label = self.small_font.render(res_text, True, self.WHITE)
            res_rect = res_label.get_rect(center=(center_x, 80))
            surface.blit(res_label, res_rect)
            
    def bezel_compensation(self):
        """Test bezel compensation across monitors"""
        for i, monitor in enumerate(self.monitors):
            if monitor.surface is None:
                continue
                
            surface = monitor.surface
            surface.fill(self.BLACK)
            width, height = monitor.resolution
            
            # Draw lines that should continue across bezels
            line_spacing = 100
            
            # Horizontal lines
            for y in range(line_spacing, height, line_spacing):
                pygame.draw.line(surface, self.WHITE, (0, y), (width, y), 2)
                
            # Vertical continuation lines at edges
            if i > 0:  # Not the leftmost monitor
                for y in range(0, height, 20):
                    pygame.draw.line(surface, self.NEON_GREEN, (0, y), (20, y), 1)
                    
            if i < len(self.monitors) - 1:  # Not the rightmost monitor
                for y in range(0, height, 20):
                    pygame.draw.line(surface, self.NEON_GREEN, (width - 20, y), (width, y), 1)
                    
            # Center pattern
            center_x = width // 2
            center_y = height // 2
            
            # Draw circles from center
            for radius in range(50, min(width, height) // 2, 50):
                pygame.draw.circle(surface, self.WHITE, (center_x, center_y), radius, 1)
                
    def color_matching(self):
        """Test color matching across monitors"""
        # Color patches that should match across monitors
        colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 255), # White
            (128, 128, 128), # Gray
            (255, 255, 0),   # Yellow
            (255, 0, 255),   # Magenta
            (0, 255, 255)    # Cyan
        ]
        
        for i, monitor in enumerate(self.monitors):
            if monitor.surface is None:
                continue
                
            surface = monitor.surface
            surface.fill(self.BLACK)
            width, height = monitor.resolution
            
            # Draw color patches
            patch_size = min(width, height) // 4
            start_x = (width - patch_size * 4) // 2
            start_y = (height - patch_size * 2) // 2
            
            for row in range(2):
                for col in range(4):
                    color_index = row * 4 + col
                    if color_index < len(colors):
                        color = colors[color_index]
                        rect = pygame.Rect(
                            start_x + col * patch_size,
                            start_y + row * patch_size,
                            patch_size - 4,
                            patch_size - 4
                        )
                        pygame.draw.rect(surface, color, rect)
                        
                        # Color label
                        color_names = ['Red', 'Green', 'Blue', 'White', 'Gray', 'Yellow', 'Magenta', 'Cyan']
                        if color_index < len(color_names):
                            label_color = self.BLACK if sum(color) > 400 else self.WHITE
                            label = self.small_font.render(color_names[color_index], True, label_color)
                            label_rect = label.get_rect(center=rect.center)
                            surface.blit(label, label_rect)
                            
            # Monitor info
            monitor_text = f"Monitor {i + 1} - Color Matching"
            text = self.small_font.render(monitor_text, True, self.NEON_GREEN)
            surface.blit(text, (10, 10))
            
    def individual_patterns(self):
        """Display different patterns on each monitor"""
        for i, monitor in enumerate(self.monitors):
            if monitor.surface is None:
                continue
                
            surface = monitor.surface
            surface.fill(self.BLACK)
            width, height = monitor.resolution
            
            # Draw different pattern on each monitor
            pattern_type = i % 4
            
            if pattern_type == 0:
                self._draw_grid_pattern(surface, width, height)
                pattern_name = "Grid"
            elif pattern_type == 1:
                self._draw_circle_pattern(surface, width, height)
                pattern_name = "Circles"
            elif pattern_type == 2:
                self._draw_diagonal_pattern(surface, width, height)
                pattern_name = "Diagonals"
            else:
                self._draw_checkerboard_pattern(surface, width, height)
                pattern_name = "Checkerboard"
            
            # Label
            label = f"Monitor {i + 1}: {pattern_name}"
            text = self.font.render(label, True, self.NEON_GREEN)
            text_rect = text.get_rect(center=(width // 2, 50))
            surface.blit(text, text_rect)
            
    def _draw_grid_pattern(self, surface, width, height):
        """Draw grid pattern"""
        for x in range(0, width, 30):
            pygame.draw.line(surface, self.WHITE, (x, 0), (x, height), 1)
        for y in range(0, height, 30):
            pygame.draw.line(surface, self.WHITE, (0, y), (width, y), 1)
            
    def _draw_circle_pattern(self, surface, width, height):
        """Draw concentric circles"""
        center_x = width // 2
        center_y = height // 2
        for radius in range(20, min(width, height) // 2, 30):
            pygame.draw.circle(surface, self.WHITE, (center_x, center_y), radius, 2)
            
    def _draw_diagonal_pattern(self, surface, width, height):
        """Draw diagonal lines"""
        for i in range(0, width + height, 40):
            pygame.draw.line(surface, self.WHITE, (0, i), (i, 0), 2)
            pygame.draw.line(surface, self.WHITE, (width - i, height), (width, height - i), 2)
            
    def _draw_checkerboard_pattern(self, surface, width, height):
        """Draw checkerboard pattern"""
        size = 60
        for row in range(0, height // size + 1):
            for col in range(0, width // size + 1):
                if (row + col) % 2 == 0:
                    rect = pygame.Rect(col * size, row * size, size, size)
                    pygame.draw.rect(surface, self.WHITE, rect)
                    
    def span_test(self):
        """Test pattern spanning across multiple monitors"""
        if len(self.monitors) < 2:
            # Single monitor fallback
            self.alignment_grid()
            return
            
        # Draw a continuous pattern across all monitors
        total_width = sum(m.resolution[0] for m in self.monitors)
        
        for i, monitor in enumerate(self.monitors):
            if monitor.surface is None:
                continue
                
            surface = monitor.surface
            surface.fill(self.BLACK)
            width, height = monitor.resolution
            
            # Calculate offset for this monitor
            x_offset = sum(self.monitors[j].resolution[0] for j in range(i))
            
            # Draw continuous sine wave across all monitors
            wave_height = height // 4
            wave_center = height // 2
            
            for x in range(width):
                global_x = x_offset + x
                y = wave_center + int(wave_height * math.sin(2 * math.pi * global_x / total_width * 3))
                if 0 <= y < height:
                    pygame.draw.circle(surface, self.NEON_GREEN, (x, y), 3)
                    
            # Draw vertical reference line at monitor boundary
            if i > 0:
                pygame.draw.line(surface, self.NEON_MAGENTA, (0, 0), (0, height), 3)
                
            # Monitor label
            label = f"Monitor {i + 1} - Span Test"
            text = self.small_font.render(label, True, self.WHITE)
            surface.blit(text, (10, 10))
            
    def refresh_sync_test(self):
        """Test refresh rate synchronization"""
        # Moving bars to test for tearing across monitors
        time_ms = pygame.time.get_ticks()
        
        for i, monitor in enumerate(self.monitors):
            if monitor.surface is None:
                continue
                
            surface = monitor.surface
            surface.fill(self.BLACK)
            width, height = monitor.resolution
            
            # Moving vertical bar
            bar_speed = 0.5  # pixels per ms
            bar_x = int((time_ms * bar_speed) % (width + 100)) - 50
            bar_width = 50
            
            if bar_x < width and bar_x + bar_width > 0:
                rect = pygame.Rect(max(0, bar_x), 0, min(bar_width, width - bar_x), height)
                pygame.draw.rect(surface, self.WHITE, rect)
                
            # Refresh rate info
            label = f"Monitor {i + 1} - Sync Test"
            text = self.small_font.render(label, True, self.NEON_GREEN)
            surface.blit(text, (10, 10))
            
    def uniformity_test(self):
        """Test brightness uniformity across monitors"""
        # Gray levels for uniformity testing
        gray_levels = [64, 128, 192]
        
        for i, monitor in enumerate(self.monitors):
            if monitor.surface is None:
                continue
                
            surface = monitor.surface
            width, height = monitor.resolution
            
            # Use different gray level for each monitor
            gray_value = gray_levels[i % len(gray_levels)]
            surface.fill((gray_value, gray_value, gray_value))
            
            # Grid for uniformity reference
            for x in range(0, width, 100):
                pygame.draw.line(surface, self.WHITE, (x, 0), (x, height), 1)
            for y in range(0, height, 100):
                pygame.draw.line(surface, self.WHITE, (0, y), (width, y), 1)
                
            # Label
            label = f"Monitor {i + 1} - Gray {gray_value}"
            text_color = self.BLACK if gray_value > 128 else self.WHITE
            text = self.font.render(label, True, text_color)
            text_rect = text.get_rect(center=(width // 2, height // 2))
            surface.blit(text, text_rect)
            
    def multi_gamma_test(self):
        """Test gamma across multiple monitors"""
        for i, monitor in enumerate(self.monitors):
            if monitor.surface is None:
                continue
                
            surface = monitor.surface
            surface.fill(self.BLACK)
            width, height = monitor.resolution
            
            # Gamma gradient
            for x in range(width):
                brightness = x / width
                gamma_corrected = pow(brightness, 2.2)
                gray_value = int(gamma_corrected * 255)
                color = (gray_value, gray_value, gray_value)
                pygame.draw.line(surface, color, (x, 0), (x, height), 1)
                
            # Gamma reference squares
            square_size = 100
            y_pos = height // 2 - square_size // 2
            
            for j, gamma_val in enumerate([1.0, 1.8, 2.2, 2.8]):
                x_pos = j * (width // 4) + (width // 8) - square_size // 2
                corrected = pow(0.5, gamma_val)  # 50% input
                gray = int(corrected * 255)
                
                rect = pygame.Rect(x_pos, y_pos, square_size, square_size)
                pygame.draw.rect(surface, (gray, gray, gray), rect)
                pygame.draw.rect(surface, self.WHITE, rect, 2)
                
                # Label
                label = f"γ{gamma_val}"
                text = self.small_font.render(label, True, self.NEON_GREEN)
                text_rect = text.get_rect(center=(x_pos + square_size // 2, y_pos - 20))
                surface.blit(text, text_rect)
                
            # Monitor label
            monitor_label = f"Monitor {i + 1} - Gamma Test"
            text = self.small_font.render(monitor_label, True, self.NEON_GREEN)
            surface.blit(text, (10, 10))
            
    def draw_info(self):
        """Draw info overlay on primary monitor"""
        primary = next((m for m in self.monitors if m.is_primary), self.monitors[0])
        if primary.surface is None:
            return
            
        # Info background
        info_width = 400
        info_height = 200
        info_surface = pygame.Surface((info_width, info_height))
        info_surface.set_alpha(200)
        info_surface.fill(self.BLACK)
        
        # Pattern name
        pattern_name = self.pattern_names[self.current_pattern]
        name_text = self.font.render(pattern_name, True, self.NEON_GREEN)
        info_surface.blit(name_text, (10, 10))
        
        # Monitor count
        count_text = f"Monitors: {len(self.monitors)}"
        count_label = self.small_font.render(count_text, True, self.WHITE)
        info_surface.blit(count_label, (10, 45))
        
        # Controls
        controls = [
            "← → : Change Pattern",
            "S : Toggle Sync",
            "I : Toggle Info",
            "ESC : Exit"
        ]
        
        y = 75
        for control in controls:
            control_text = self.small_font.render(control, True, self.WHITE)
            info_surface.blit(control_text, (10, y))
            y += 25
            
        primary.surface.blit(info_surface, (10, 10))
        
    def handle_events(self):
        """Handle keyboard events"""
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
                elif event.key == pygame.K_s:
                    self.sync_patterns = not self.sync_patterns
                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info
                    
    def run(self):
        """Main loop"""
        if not self.initialize():
            return
            
        clock = pygame.time.Clock()
        
        while self.running:
            self.handle_events()
            
            # Draw current pattern
            self.patterns[self.current_pattern]()
            
            # Draw info overlay
            if self.show_info:
                self.draw_info()
                
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()
        sys.exit()


def main():
    """Main entry point"""
    suite = MultiMonitorTestSuite()
    suite.run()


if __name__ == "__main__":
    main()