import constants.colors as colors
import pygame

FONT_SIZE = 30

def draw_text(surface: pygame.Surface, text: str, font: pygame.font.Font, color: tuple[int, int, int], pos: tuple[int, int]) -> pygame.Rect:
  text_surface = font.render(text, True, color)
  return surface.blit(text_surface, pos)


class GameMenuItem:

  def __init__(self, name: str, on_press) -> None:
    self.name = name
    self.on_press = on_press

  def press(self) -> None:
    self.on_press()

  def draw(self, surface: pygame.Surface, pos: tuple[int, int], font: pygame.font.Font, mouse_pos: tuple[int, int] = (-1, -1)) -> pygame.Rect:
    rect =  draw_text(surface, self.name, font, colors.GRAY, pos)
    if rect.collidepoint(mouse_pos):
      rect.move(-999, -999)
      return draw_text(surface, self.name, font, colors.LIGHT_GRAY, pos)
    
    return rect

class GameMenu:
   
  def __init__(self, font_name: str | None = None) -> None:
    self._difficulty = -1
    self.font_name = font_name
    
    self.menu_items: list[GameMenuItem] = []
    names = ['Easy', "Medium", "Hard"]
    on_press_helper = lambda d: (lambda: self.set_difficulty(d))
    for i in range(len(names)):
      on_press = on_press_helper(i)
      name = names[i]
      self.menu_items.append(GameMenuItem(name, on_press))

  def is_difficulty_selected(self) -> bool:
    return self._difficulty != -1

  def set_difficulty(self, difficulty: int) -> None:
    self._difficulty = difficulty
  
  def get_difficulty(self) -> int:
    return self._difficulty

  def press(self, menu_item_index: int) -> bool:
    if not menu_item_index in range(len(self.menu_items)):
      return False
    
    self.menu_items[menu_item_index].press()
    return True
    
  def draw(self, surface: pygame.Surface, pos: tuple[int, int], mouse_pos: tuple[int, int] = (-1, -1)) -> list[pygame.Rect]:
    rects: list[pygame.Rect] = []
    
    menu_item_font = pygame.font.SysFont(None, FONT_SIZE)
    title_font = pygame.font.SysFont(None, FONT_SIZE*2)

    title_text = "Water Sort Puzzle"
    x, y = pos

    draw_text(surface, title_text, title_font, colors.GRAY, (x, y))
    y += FONT_SIZE*2
    x += 10
    for menu_item in self.menu_items:
      rect = menu_item.draw(surface, (x, y), menu_item_font, mouse_pos=mouse_pos)
      rects.append(rect)
      y += FONT_SIZE
    
    return rects
