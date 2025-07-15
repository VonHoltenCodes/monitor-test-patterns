#!/usr/bin/env python3
"""
NEONpulseTechshop Automated Calibration Sequences
Guided calibration workflow with step-by-step instructions
"""

import pygame
import sys
import time
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Initialize Pygame
pygame.init()

class CalibrationStep(Enum):
    """Calibration workflow steps"""
    WELCOME = "welcome"
    BRIGHTNESS = "brightness"
    CONTRAST = "contrast"
    GAMMA = "gamma"
    WHITE_POINT = "white_point"
    COLOR_ACCURACY = "color_accuracy"
    UNIFORMITY = "uniformity"
    COMPLETE = "complete"

@dataclass
class CalibrationSettings:
    """User's calibration preferences"""
    target_gamma: float = 2.2
    target_white_point: str = "6500K"
    target_brightness: int = 120  # cd/m²
    ambient_light: str = "medium"
    use_case: str = "general"  # general, photo, video, gaming

@dataclass
class TestResult:
    """Result from a calibration test"""
    test_name: str
    passed: bool
    measured_value: Optional[float] = None
    target_value: Optional[float] = None
    notes: str = ""

class AutoCalibrationSuite:
    """Automated calibration workflow"""
    
    def __init__(self, resolution=(1920, 1080)):
        self.width, self.height = resolution
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("NEONpulseTechshop Auto Calibration")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Colors
        self.NEON_GREEN = (0, 255, 65)
        self.NEON_MAGENTA = (255, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        
        # Calibration state
        self.current_step = CalibrationStep.WELCOME
        self.settings = CalibrationSettings()
        self.results = []
        self.step_start_time = time.time()
        self.running = True
        self.waiting_for_user = False
        
        # Step definitions
        self.steps = {
            CalibrationStep.WELCOME: self.welcome_screen,
            CalibrationStep.BRIGHTNESS: self.brightness_calibration,
            CalibrationStep.CONTRAST: self.contrast_calibration,
            CalibrationStep.GAMMA: self.gamma_calibration,
            CalibrationStep.WHITE_POINT: self.white_point_calibration,
            CalibrationStep.COLOR_ACCURACY: self.color_accuracy_test,
            CalibrationStep.UNIFORMITY: self.uniformity_test,
            CalibrationStep.COMPLETE: self.completion_screen
        }
        
        self.step_order = [
            CalibrationStep.WELCOME,
            CalibrationStep.BRIGHTNESS,
            CalibrationStep.CONTRAST,
            CalibrationStep.GAMMA,
            CalibrationStep.WHITE_POINT,
            CalibrationStep.COLOR_ACCURACY,
            CalibrationStep.UNIFORMITY,
            CalibrationStep.COMPLETE
        ]
        
    def draw_header(self, title: str, subtitle: str = ""):
        """Draw common header"""
        # Background
        header_rect = pygame.Rect(0, 0, self.width, 120)
        pygame.draw.rect(self.screen, self.BLACK, header_rect)
        
        # Gradient line
        for i in range(5):
            color_factor = (5 - i) / 5
            color = tuple(int(c * color_factor) for c in self.NEON_MAGENTA)
            pygame.draw.line(self.screen, color, 
                           (0, 115 + i), (self.width, 115 + i), 1)
        
        # Title
        title_text = self.font.render(title, True, self.NEON_MAGENTA)
        title_rect = title_text.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        if subtitle:
            subtitle_text = self.medium_font.render(subtitle, True, self.WHITE)
            subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 80))
            self.screen.blit(subtitle_text, subtitle_rect)
            
    def draw_progress_bar(self):
        """Draw calibration progress"""
        current_index = self.step_order.index(self.current_step)
        total_steps = len(self.step_order) - 1  # Don't count welcome
        progress = current_index / total_steps
        
        # Progress bar background
        bar_width = self.width - 200
        bar_height = 20
        bar_x = 100
        bar_y = self.height - 60
        
        pygame.draw.rect(self.screen, self.GRAY, 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Progress fill
        fill_width = int(bar_width * progress)
        pygame.draw.rect(self.screen, self.NEON_GREEN,
                        (bar_x, bar_y, fill_width, bar_height))
        
        # Progress text
        progress_text = f"Step {current_index + 1} of {total_steps + 1}"
        text = self.small_font.render(progress_text, True, self.WHITE)
        text_rect = text.get_rect(center=(self.width // 2, bar_y + bar_height + 20))
        self.screen.blit(text, text_rect)
        
    def draw_instructions(self, instructions: List[str], y_start: int = 200):
        """Draw instruction text"""
        y = y_start
        for instruction in instructions:
            # Word wrap for long instructions
            words = instruction.split(' ')
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                text_width = self.medium_font.size(test_line)[0]
                
                if text_width > self.width - 200:
                    if current_line:
                        lines.append(current_line.strip())
                        current_line = word + " "
                    else:
                        lines.append(word)
                        current_line = ""
                else:
                    current_line = test_line
                    
            if current_line:
                lines.append(current_line.strip())
                
            # Draw lines
            for line in lines:
                text = self.medium_font.render(line, True, self.WHITE)
                text_rect = text.get_rect(center=(self.width // 2, y))
                self.screen.blit(text, text_rect)
                y += 40
                
            y += 20  # Extra space between instructions
            
    def draw_controls(self, controls: List[str]):
        """Draw control instructions at bottom"""
        y = self.height - 150
        
        for control in controls:
            text = self.small_font.render(control, True, self.NEON_GREEN)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 25
            
    def welcome_screen(self):
        """Welcome and setup screen"""
        self.screen.fill(self.BLACK)
        
        # Logo
        neon_text = self.font.render("NEON", True, self.NEON_MAGENTA)
        pulse_text = self.font.render("pulse", True, self.NEON_GREEN)
        tech_text = self.medium_font.render("TECHSHOP", True, self.NEON_GREEN)
        
        logo_y = 50
        neon_rect = neon_text.get_rect(center=(self.width // 2 - 50, logo_y))
        pulse_rect = pulse_text.get_rect(center=(self.width // 2 + 50, logo_y))
        tech_rect = tech_text.get_rect(center=(self.width // 2, logo_y + 50))
        
        self.screen.blit(neon_text, neon_rect)
        self.screen.blit(pulse_text, pulse_rect)
        self.screen.blit(tech_text, tech_rect)
        
        # Title
        title = "Automated Monitor Calibration"
        title_text = self.font.render(title, True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "This wizard will guide you through calibrating your monitor",
            "for optimal color accuracy and consistency.",
            "",
            "You will need:",
            "• 30-45 minutes of uninterrupted time",
            "• Stable ambient lighting",
            "• Access to monitor controls",
            "",
            "For best results, let your monitor warm up for 30 minutes",
            "before starting calibration."
        ]
        
        y = 220
        for instruction in instructions:
            if instruction == "":
                y += 20
                continue
                
            color = self.NEON_GREEN if instruction.startswith("•") else self.WHITE
            text = self.medium_font.render(instruction, True, color)
            
            if instruction.startswith("•"):
                text_rect = text.get_rect(left=self.width // 2 - 200, centery=y)
            else:
                text_rect = text.get_rect(center=(self.width // 2, y))
                
            self.screen.blit(text, text_rect)
            y += 35
            
        # Controls
        controls = [
            "Press SPACE to begin calibration",
            "Press ESC to exit"
        ]
        self.draw_controls(controls)
        
    def brightness_calibration(self):
        """Brightness calibration step"""
        self.screen.fill(self.BLACK)
        
        self.draw_header("Step 1: Brightness Calibration", 
                        "Adjust display brightness for optimal black levels")
        
        # PLUGE pattern for brightness adjustment
        pluge_height = 200
        pluge_y = 200
        bar_width = self.width // 5
        
        # PLUGE bars (Picture Line-Up Generation Equipment)
        pluge_values = [0, 5, 10, 16, 20]  # Below black, black, above black
        
        for i, value in enumerate(pluge_values):
            color = (value, value, value)
            rect = pygame.Rect(i * bar_width, pluge_y, bar_width - 2, pluge_height)
            pygame.draw.rect(self.screen, color, rect)
            
            # Labels
            if i == 0:
                label = "Below Black"
            elif i == 2:
                label = "True Black"
            elif i == 4:
                label = "Above Black"
            else:
                label = f"{value}"
                
            label_text = self.small_font.render(label, True, self.WHITE)
            label_rect = label_text.get_rect(center=(i * bar_width + bar_width // 2, pluge_y - 20))
            self.screen.blit(label_text, label_rect)
            
        # Instructions
        instructions = [
            "Adjust your monitor's BRIGHTNESS control until:",
            "• The leftmost bar (Below Black) is invisible",
            "• The middle bar (True Black) is just barely visible",
            "• The rightmost bar (Above Black) is clearly visible",
            "",
            "Do NOT adjust contrast - only brightness!"
        ]
        
        self.draw_instructions(instructions, pluge_y + pluge_height + 50)
        
        # Progress and controls
        self.draw_progress_bar()
        controls = [
            "Adjust monitor BRIGHTNESS control",
            "Press SPACE when adjustment is complete",
            "Press B to go back"
        ]
        self.draw_controls(controls)
        
    def contrast_calibration(self):
        """Contrast calibration step"""
        self.screen.fill(self.BLACK)
        
        self.draw_header("Step 2: Contrast Calibration",
                        "Adjust display contrast for optimal white levels")
        
        # White level test pattern
        white_height = 200
        white_y = 200
        bar_width = self.width // 5
        
        # Near-white bars
        white_values = [235, 240, 245, 250, 255]
        
        for i, value in enumerate(white_values):
            color = (value, value, value)
            rect = pygame.Rect(i * bar_width, white_y, bar_width - 2, white_height)
            pygame.draw.rect(self.screen, color, rect)
            
            # Labels
            label = f"{value}"
            label_color = self.BLACK if value > 240 else self.WHITE
            label_text = self.small_font.render(label, True, label_color)
            label_rect = label_text.get_rect(center=(i * bar_width + bar_width // 2, white_y + white_height // 2))
            self.screen.blit(label_text, label_rect)
            
        # Instructions
        instructions = [
            "Adjust your monitor's CONTRAST control until:",
            "• All bars are distinguishable from each other",
            "• The rightmost bar (255) is bright white but not glowing",
            "• No detail is lost in the bright areas",
            "",
            "If bars merge together, reduce contrast!"
        ]
        
        self.draw_instructions(instructions, white_y + white_height + 50)
        
        self.draw_progress_bar()
        controls = [
            "Adjust monitor CONTRAST control",
            "Press SPACE when adjustment is complete",
            "Press B to go back"
        ]
        self.draw_controls(controls)
        
    def gamma_calibration(self):
        """Gamma calibration step"""
        self.screen.fill(self.BLACK)
        
        self.draw_header("Step 3: Gamma Calibration",
                        f"Target: {self.settings.target_gamma}")
        
        # Gamma test pattern
        gamma_y = 180
        gamma_height = 300
        
        # Create gamma test squares
        square_size = 150
        squares_per_row = 3
        start_x = (self.width - squares_per_row * square_size * 1.2) // 2
        
        gamma_values = [1.8, 2.2, 2.8]
        
        for i, gamma in enumerate(gamma_values):
            x = start_x + i * square_size * 1.2
            
            # Create checkerboard pattern at 50% gray
            for row in range(square_size // 4):
                for col in range(square_size // 4):
                    # Alternate between gamma-corrected values
                    if (row + col) % 2 == 0:
                        # 50% input through gamma curve
                        value = int(pow(0.5, gamma) * 255)
                    else:
                        # Dithered pattern to match 50% gray
                        value = 127
                        
                    color = (value, value, value)
                    rect = pygame.Rect(x + col * 4, gamma_y + row * 4, 4, 4)
                    pygame.draw.rect(self.screen, color, rect)
                    
            # Solid 50% gray comparison square
            gray_rect = pygame.Rect(x, gamma_y + square_size + 20, square_size, 50)
            pygame.draw.rect(self.screen, (127, 127, 127), gray_rect)
            
            # Label
            label = f"γ {gamma}"
            color = self.NEON_GREEN if gamma == self.settings.target_gamma else self.WHITE
            label_text = self.medium_font.render(label, True, color)
            label_rect = label_text.get_rect(center=(x + square_size // 2, gamma_y + square_size + 100))
            self.screen.blit(label_text, label_rect)
            
        # Instructions
        instructions = [
            "Look at the checkerboard patterns above.",
            f"The γ {self.settings.target_gamma} pattern should blend smoothly",
            "with the solid gray bar below it.",
            "",
            "Adjust monitor settings or graphics card gamma",
            "until the pattern matches the gray bar."
        ]
        
        self.draw_instructions(instructions, gamma_y + square_size + 150)
        
        self.draw_progress_bar()
        controls = [
            "Adjust gamma until pattern matches gray bar",
            "Press SPACE when adjustment is complete",
            "Press B to go back"
        ]
        self.draw_controls(controls)
        
    def white_point_calibration(self):
        """White point calibration step"""
        self.screen.fill(self.BLACK)
        
        self.draw_header("Step 4: White Point Calibration",
                        f"Target: {self.settings.target_white_point}")
        
        # White point comparison
        comparison_height = 200
        comparison_y = 200
        
        # Current white point (left)
        left_rect = pygame.Rect(100, comparison_y, self.width // 2 - 150, comparison_height)
        pygame.draw.rect(self.screen, self.WHITE, left_rect)
        
        # Target white point (right) - simulated D65
        # This is approximate since we can't actually show true D65 without calibration
        d65_color = (255, 255, 248)  # Slightly warm white
        right_rect = pygame.Rect(self.width // 2 + 50, comparison_y, self.width // 2 - 150, comparison_height)
        pygame.draw.rect(self.screen, d65_color, right_rect)
        
        # Labels
        current_label = self.medium_font.render("Current White Point", True, self.BLACK)
        current_rect = current_label.get_rect(center=(left_rect.centerx, left_rect.centery))
        self.screen.blit(current_label, current_rect)
        
        target_label = self.medium_font.render(f"Target: {self.settings.target_white_point}", True, self.BLACK)
        target_rect = target_label.get_rect(center=(right_rect.centerx, right_rect.centery))
        self.screen.blit(target_label, target_rect)
        
        # Instructions
        instructions = [
            "Adjust your monitor's color temperature control",
            f"to match the target {self.settings.target_white_point} standard.",
            "",
            "The two white rectangles should appear identical.",
            "Common settings: 6500K (D65), 5000K (D50), 9300K (cool)"
        ]
        
        self.draw_instructions(instructions, comparison_y + comparison_height + 50)
        
        self.draw_progress_bar()
        controls = [
            "Adjust monitor COLOR TEMPERATURE",
            "Press SPACE when whites match",
            "Press B to go back"
        ]
        self.draw_controls(controls)
        
    def color_accuracy_test(self):
        """Color accuracy verification"""
        self.screen.fill(self.BLACK)
        
        self.draw_header("Step 5: Color Accuracy Test",
                        "Verify color reproduction")
        
        # Color checker pattern
        colors = [
            ((139, 69, 19), "Brown"),
            ((255, 105, 180), "Pink"),
            ((255, 165, 0), "Orange"),
            ((255, 255, 0), "Yellow"),
            ((0, 128, 0), "Green"),
            ((0, 191, 255), "Sky Blue"),
            ((75, 0, 130), "Indigo"),
            ((238, 130, 238), "Violet"),
            ((255, 0, 0), "Red"),
            ((0, 0, 255), "Blue"),
            ((255, 255, 255), "White"),
            ((128, 128, 128), "Gray")
        ]
        
        patch_size = 120
        cols = 4
        rows = 3
        start_x = (self.width - cols * patch_size * 1.1) // 2
        start_y = 180
        
        for i, (color, name) in enumerate(colors):
            row = i // cols
            col = i % cols
            
            x = start_x + col * patch_size * 1.1
            y = start_y + row * patch_size * 1.1
            
            # Color patch
            rect = pygame.Rect(x, y, patch_size, patch_size)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.WHITE, rect, 2)
            
            # Label
            label_color = self.BLACK if sum(color) > 400 else self.WHITE
            label_text = self.small_font.render(name, True, label_color)
            label_rect = label_text.get_rect(center=(x + patch_size // 2, y + patch_size // 2))
            self.screen.blit(label_text, label_rect)
            
        # Instructions
        instructions = [
            "Examine the color patches above.",
            "Colors should appear natural and well-saturated.",
            "If colors appear too vivid or dull, check monitor settings."
        ]
        
        self.draw_instructions(instructions, start_y + rows * patch_size * 1.1 + 30)
        
        self.draw_progress_bar()
        controls = [
            "Verify colors appear natural",
            "Press SPACE if colors look good",
            "Press B to go back"
        ]
        self.draw_controls(controls)
        
    def uniformity_test(self):
        """Display uniformity test"""
        self.screen.fill(self.GRAY)
        
        self.draw_header("Step 6: Uniformity Test",
                        "Check for brightness and color uniformity")
        
        # Grid overlay for reference
        grid_spacing = 100
        for x in range(0, self.width, grid_spacing):
            pygame.draw.line(self.screen, self.WHITE, (x, 120), (x, self.height - 100), 1)
        for y in range(120, self.height - 100, grid_spacing):
            pygame.draw.line(self.screen, self.WHITE, (0, y), (self.width, y), 1)
            
        # Instructions overlay
        instruction_bg = pygame.Rect(50, self.height - 150, self.width - 100, 100)
        pygame.draw.rect(self.screen, self.BLACK, instruction_bg)
        pygame.draw.rect(self.screen, self.WHITE, instruction_bg, 2)
        
        instructions = [
            "Look for variations in brightness or color across the screen.",
            "The gray background should appear uniform throughout.",
            "Some variation is normal, especially near edges."
        ]
        
        y = self.height - 140
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 25
            
        self.draw_progress_bar()
        
    def completion_screen(self):
        """Calibration completion screen"""
        self.screen.fill(self.BLACK)
        
        # Success header
        success_text = self.font.render("Calibration Complete!", True, self.NEON_GREEN)
        success_rect = success_text.get_rect(center=(self.width // 2, 100))
        self.screen.blit(success_text, success_rect)
        
        # Summary
        summary_y = 180
        summary_items = [
            "✓ Brightness optimized for ambient lighting",
            "✓ Contrast adjusted for full tonal range",
            f"✓ Gamma corrected to {self.settings.target_gamma}",
            f"✓ White point calibrated to {self.settings.target_white_point}",
            "✓ Color accuracy verified",
            "✓ Uniformity checked"
        ]
        
        for item in summary_items:
            text = self.medium_font.render(item, True, self.NEON_GREEN)
            text_rect = text.get_rect(center=(self.width // 2, summary_y))
            self.screen.blit(text, text_rect)
            summary_y += 40
            
        # Recommendations
        recommendations = [
            "",
            "Recommendations:",
            "• Save these settings in your monitor's memory",
            "• Re-calibrate monthly or when lighting changes",
            "• Use color-managed applications for best results"
        ]
        
        y = summary_y + 40
        for rec in recommendations:
            if rec == "":
                y += 20
                continue
                
            color = self.WHITE if rec.startswith("•") else self.NEON_MAGENTA
            text = self.medium_font.render(rec, True, color)
            
            if rec.startswith("•"):
                text_rect = text.get_rect(left=self.width // 2 - 250, centery=y)
            else:
                text_rect = text.get_rect(center=(self.width // 2, y))
                
            self.screen.blit(text, text_rect)
            y += 35
            
        # Controls
        controls = [
            "Press SPACE to save calibration report",
            "Press ESC to exit"
        ]
        self.draw_controls(controls)
        
    def next_step(self):
        """Advance to next calibration step"""
        current_index = self.step_order.index(self.current_step)
        if current_index < len(self.step_order) - 1:
            self.current_step = self.step_order[current_index + 1]
            self.step_start_time = time.time()
            
    def previous_step(self):
        """Go back to previous step"""
        current_index = self.step_order.index(self.current_step)
        if current_index > 0:
            self.current_step = self.step_order[current_index - 1]
            self.step_start_time = time.time()
            
    def save_calibration_report(self):
        """Save calibration results"""
        report = {
            "calibration_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "settings": {
                "target_gamma": self.settings.target_gamma,
                "target_white_point": self.settings.target_white_point,
                "target_brightness": self.settings.target_brightness
            },
            "results": [result.__dict__ for result in self.results],
            "total_time": time.time() - self.step_start_time
        }
        
        filename = f"calibration_report_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"Calibration report saved as: {filename}")
        
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.current_step == CalibrationStep.COMPLETE:
                        self.save_calibration_report()
                    else:
                        self.next_step()
                elif event.key == pygame.K_b:
                    self.previous_step()
                    
    def run(self):
        """Main calibration loop"""
        while self.running:
            self.handle_events()
            
            # Draw current step
            self.steps[self.current_step]()
            
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()


def main():
    """Main entry point"""
    calibration = AutoCalibrationSuite()
    calibration.run()


if __name__ == "__main__":
    main()