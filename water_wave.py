import math
import pygame

def draw_sin_wave(surface: pygame.Surface, width: int, color: tuple[int, int, int], offset: int, shift=0, amplitude=100, frequency=0.02, spread = 1) -> pygame.Rect:
  points = []
  
  for x in range(width):
    y = int(amplitude * math.sin((frequency * x + shift)/spread) + offset)
    points.append((x, y))

  points[0] = (0, offset)
  points[-1] = (width - 1, offset)

  return pygame.draw.polygon(surface, color, points)

class WaterWave:
  def __init__(self, shift: float, amplitude: float, amp_increment = 1/5, shift_increment = 1/30) -> None:
    self.max_amplitude = 10
    
    self.shift = shift 
    self.amplitude = amplitude
    self.shift_increment = shift_increment
    self.amp_increment = amp_increment

  
  def increment_amplitude(self):
    if self.amplitude <= -self.max_amplitude or self.amplitude >= self.max_amplitude:
      self.amp_increment = -self.amp_increment

    self.amplitude += self.amp_increment
  
  def increment_shift(self):
    self.shift += self.shift_increment
