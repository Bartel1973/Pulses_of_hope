import pygame
import numpy as np
import math
import sys

class SinusScroller:
    def __init__(self, width=1200, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("3D Sinus Scroller")
        self.clock = pygame.time.Clock()
        
        # Load background image
        try:
            self.background = pygame.image.load("pulses-3d.png")
            self.background = pygame.transform.scale(self.background, (width, height))
        except pygame.error as e:
            print(f"Error loading background: {e}")
            self.background = pygame.Surface((width, height))
            self.background.fill((20, 20, 40))
        
        # Text settings
        self.text = "PULSES OF HOPE - Greetz 2 Cyberpriestand Cumulus Brain"
        self.font = pygame.font.Font(None, 48)
        self.text_color = (255, 255, 0)  # Yellow color
        
        # Scroller parameters
        self.scroll_speed = 2.0
        self.text_x = width
        self.wave_amplitude = 50
        self.wave_frequency = 0.02
        self.wave_speed = 0.05
        self.time = 0
        
        # 3D effect parameters
        self.depth_layers = 5
        self.layer_spacing = 20
        
    def draw_text_with_3d_effect(self):
        """Draw text with 3D sinus wave effect"""
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        
        # Create multiple layers for 3D effect
        for layer in range(self.depth_layers):
            layer_offset = layer * self.layer_spacing
            layer_alpha = 255 - (layer * 40)
            layer_color = (
                self.text_color[0] - (layer * 30),
                self.text_color[1] - (layer * 30), 
                self.text_color[2] - (layer * 20)
            )
            
            # Create surface for this layer with proper height
            layer_surface = pygame.Surface((text_rect.width, self.height), pygame.SRCALPHA)
            
            # Draw text with sinus wave distortion
            for x in range(text_rect.width):
                if self.text_x + x < 0 or self.text_x + x >= self.width:
                    continue
                    
                # Calculate sinus wave offset
                wave_offset = math.sin((x * self.wave_frequency) + self.time + (layer * 0.2)) * self.wave_amplitude
                
                # Get text column
                text_column = text_surface.subsurface((x, 0, 1, text_rect.height))
                
                # Draw column with wave offset - centered vertically
                y_pos = self.height // 2 - text_rect.height // 2 + wave_offset + layer_offset
                layer_surface.blit(text_column, (x, y_pos))
            
            # Apply alpha and draw to screen
            layer_surface.set_alpha(layer_alpha)
            self.screen.blit(layer_surface, (self.text_x, 0))
    
    def draw_particles(self):
        """Add floating particles for extra 3D effect"""
        num_particles = 50
        for i in range(num_particles):
            x = (i * 73 + self.time * 20) % self.width
            y = self.height // 2 + math.sin((i * 0.1) + self.time) * 200
            size = 2 + math.sin(self.time + i) * 1
            
            # Depth effect with varying opacity
            depth = (math.sin(self.time * 0.5 + i * 0.2) + 1) / 2
            alpha = int(100 + depth * 155)
            
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.text_color, alpha), (size, size), size)
            self.screen.blit(particle_surface, (x - size, y - size))
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_UP:
                        self.wave_amplitude = min(100, self.wave_amplitude + 5)
                    elif event.key == pygame.K_DOWN:
                        self.wave_amplitude = max(10, self.wave_amplitude - 5)
                    elif event.key == pygame.K_LEFT:
                        self.scroll_speed = max(0.5, self.scroll_speed - 0.5)
                    elif event.key == pygame.K_RIGHT:
                        self.scroll_speed = min(10, self.scroll_speed + 0.5)
            
            # Clear screen with background
            self.screen.blit(self.background, (0, 0))
            
            # Add semi-transparent overlay for better text visibility
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(100)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Draw particles
            self.draw_particles()
            
            # Draw main text with 3D effect
            self.draw_text_with_3d_effect()
            
            # Update scroll position
            self.text_x -= self.scroll_speed
            text_width = self.font.size(self.text)[0]
            
            # Reset position when text scrolls off screen
            if self.text_x < -text_width:
                self.text_x = self.width
            
            # Update time for animation
            self.time += self.wave_speed
            
            # Display controls
            controls_font = pygame.font.Font(None, 24)
            controls = [
                "Controls: ↑/↓ - Wave amplitude | ←/→ - Scroll speed | ESC - Exit",
                f"Wave: {self.wave_amplitude:.0f} | Speed: {self.scroll_speed:.1f}"
            ]
            
            for i, control_text in enumerate(controls):
                control_surface = controls_font.render(control_text, True, (200, 200, 200))
                self.screen.blit(control_surface, (10, 10 + i * 25))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    scroller = SinusScroller()
    scroller.run()
