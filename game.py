
from bottle import Bottle
from water_sort_puzzle import WaterSortPuzzle
from game_menu import GameMenu
import constants.colors as colors
import math
import pygame

def print_bottles(bottles: list[Bottle]) -> None:
  """
  Print the current state of the game to the console

  Args:
      bottles (list[Bottle]): The list of bottles in the game.
  """
  for bottle in bottles:
    print(bottle)
  print("")

def draw_bottle(surface: pygame.Surface, bottle: Bottle, x: int, y: int, water_hight=50, water_width=75, radius=20, selected=False) -> pygame.Rect:
  """
  Draw a bottle to the surface

  Args:
      surface (pygame.Surface): The surface (game window) to draw the bottle on.
      bottle (Bottle): The bottle object to be drawn.
      x (int): The initial x axis coordinate on the surface to draw the bottle on.
      y (int): The initial y axis coordinate on the surface to draw the bottle on.
      water_hight (int, optional): The hight of each water segment. Defaults to 50.
      water_width (int, optional): The width of each water segment. Defaults to 75.
      radius (int, optional): The radius of the bottle most water segment. Defaults to 20.
      selected (bool, optional): True if the user selected the bottle object. Defaults to False.

  Returns:
      pygame.Rect: The pygame Rect of the bottle that is drawn onto the surface.
  """
  water_seg_count = 0
  for water_index, water in enumerate(bottle.contents):
    for i in range(water.amount):
      rect_vals = (
        x - water_hight, # left
        y - water_hight*water_seg_count, # top
        water_width, # width 
        water_hight # hight
      )

      if i + water_index == 0:
        pygame.draw.rect(surface, water.color, rect_vals, border_bottom_left_radius=radius, border_bottom_right_radius=radius)
      else:
        pygame.draw.rect(surface, water.color, rect_vals)
      
      if bottle.get_remaining_capacity() != 0 and i + 1 == water.amount:
        draw_sin_wave(surface, x+25, water.color, y - water_hight*water_seg_count, start=x+25-water_width,  shift=water.wave.shift, amplitude=water.wave.amplitude, spread=7)
        water.wave.increment_amplitude()
        water.wave.increment_shift()

      
      water_seg_count += 1

  outline_rect_vals = (
    x - water_hight,
    y - water_hight*(bottle.capacity-1),
    water_width,
    water_hight*bottle.capacity
  )
  
  return pygame.draw.rect(surface, colors.LIGHT_GRAY if selected else colors.GRAY, outline_rect_vals, width=5, border_bottom_left_radius=radius, border_bottom_right_radius=radius)

def draw_bottles(surface: pygame.Surface, bottles: list[Bottle], init_x: int, init_y: int, right_spacing=25, water_hight=50, water_width=75, radius=20, selected_bottle_index=-1) -> list[pygame.Rect]:
  """
  Draw a list of bottle objects onto a surface

  Args:
      surface (pygame.Surface): The surface (game window) to draw the bottles on 
      bottles (list[Bottle]): The list of bottle objects to draw
      init_x (int): The initial x axis coordinate on the surface to start drawing the bottles
      init_y (int): The initial y axis coordinate on the surface to start drawing the bottles
      right_spacing (int, optional): The amount of space between each bottle when drawn onto the surface. Defaults to 25.
      water_hight (int, optional): The hight of each water segment in each bottle. Defaults to 50.
      water_width (int, optional): The width of each water segment in each bottle. Defaults to 75.
      radius (int, optional): The radius of bottom most water segment in each bottle. Defaults to 20.
      selected_bottle_index (int, optional): The index of the bottle that is selected or -1 if not bottles are selected. Defaults to -1.

  Returns:
      list[pygame.Rect]: The list of pygame rects that were drawn onto the surface
  """
  
  x, y = init_x, init_y

  rects: list[pygame.Rect] = []
  for index, bottle in enumerate(bottles):
    selected = index == selected_bottle_index 
    rect = draw_bottle(surface, bottle, x, y, water_hight=water_hight, water_width=water_width, radius=radius, selected=selected)
    rects.append(rect)

    x += right_spacing + water_width

    if surface.get_width() <= x + water_width:
      x = init_x
      y += 250 + right_spacing*3

  return rects

def get_mouse_colliding_rect(mouse_pos: tuple[int, int], rects: list[pygame.Rect]) -> int:
  """
  Gets the index of the first rect in the list of rects that is colliding with the mouse coordinate

  Args:
      mouse_pos (tuple[int, int]): The x, y coordinates of the mouse
      rects (list[pygame.Rect]): The list of rects to check

  Returns:
      int: The index of rect that is colliding with the mouse coordinate
  """
  mouse_x, mouse_y = mouse_pos
  colliding_rect_index = -1

  for index, rect in enumerate(rects):
    if rect.collidepoint(mouse_x, mouse_y):
      colliding_rect_index = index
      break

  return colliding_rect_index

def draw_sin_wave(surface: pygame.Surface, width: int, color: tuple[int, int, int], offset: int, start=0, shift=0, amplitude=100, frequency=0.02, spread = 1) -> pygame.Rect:
    points = []
    
    for x in range(start, width):
        y = int(amplitude * math.sin((frequency * x + shift)/spread) + offset)
        points.append((x, y))

    points[0] = (start, offset)
    points[-1] = (width - 1, offset)

    return pygame.draw.polygon(surface, color, points)
    

def get_difficulty_params(difficulty: int, max_colored_bottle: int, max_shuffle_moves: int) -> tuple[int, int]:
  """
  Get the number of bottles with water in them and the number of shuffles to make based on the value of `difficulty`

  Args:
      difficulty (int): An int repersetaion of the difficulty (0 = easy, 1 = medium, 2 = hard)
      max_colored_bottle (int): The max number of bottles with colored water to select from
      max_shuffle_moves (int): The max number of shuffle moves that can be made

  Returns:
      tuple[int, int]: The number of bottles with water in them and the number of shuffles to make.
  """
  if difficulty == 0:
    return max_colored_bottle//3, max_shuffle_moves//3

  if difficulty == 1:
    return max_colored_bottle//2, max_shuffle_moves//2

  return max_colored_bottle, max_shuffle_moves


def game_loop(screen: pygame.Surface, clock: pygame.time.Clock, difficulty: int) -> None:
  water_id_map = {
    0: colors.RED,
    1: colors.GREEN,
    2: colors.BLUE,
    3: colors.YELLOW,
    4: colors.PINK,
    5: colors.ORANGE,
    6: colors.PURPLE,
    7: colors.CYAN,
  }

  bottle_capacity = 4
  empty_bottle_count = 2
  max_colored_bottle = len(water_id_map)
  max_shuffle_moves = 1000

  colored_bottle_count, shuffle_moves = get_difficulty_params(difficulty, max_colored_bottle, max_shuffle_moves)

  puzzle = WaterSortPuzzle()
  puzzle.create_bottles(empty_bottle_count, colored_bottle_count, bottle_capacity, water_id_map, shuffle_moves)

  running = True

  while running:
    is_left_mouse_pressed = False

    # poll for events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        is_left_mouse_pressed, _, _ =  pygame.mouse.get_pressed()
      if event.type == pygame.KEYDOWN:
        if pygame.key.get_pressed()[pygame.K_r]:
          puzzle.restart_puzzle()

        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
          puzzle.create_bottles(empty_bottle_count, colored_bottle_count, bottle_capacity, water_id_map, shuffle_moves)

        elif pygame.key.get_pressed()[pygame.K_LEFT]:
          puzzle.go_back()
        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
          selected_difficulty = main_menu(screen, clock)
          if selected_difficulty != difficulty:
            colored_bottle_count, shuffle_moves = get_difficulty_params(selected_difficulty, max_colored_bottle, max_shuffle_moves)
            puzzle.create_bottles(empty_bottle_count, colored_bottle_count, bottle_capacity, water_id_map, shuffle_moves)
            difficulty = selected_difficulty
        
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(colors.BLACK)

    # render bottles
    bottle_rects = draw_bottles(screen, puzzle.bottles, 100, 275, selected_bottle_index=puzzle.selected_bottle_index)

    if puzzle.is_puzzle_solved():
      puzzle.create_bottles(empty_bottle_count, colored_bottle_count, bottle_capacity, water_id_map, shuffle_moves)

    if is_left_mouse_pressed:
      mouse_pos = pygame.mouse.get_pos()
      pressed_rect_index = get_mouse_colliding_rect(mouse_pos, bottle_rects)

      puzzle.select_bottle(pressed_rect_index)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

def main_menu(screen: pygame.Surface, clock: pygame.time.Clock) -> int:
  menu_start_pos = (screen.get_width()//20, screen.get_height()//20)
  game_menu = GameMenu()
  difficulty = -1

  offset = 1
  amplitude = 5
  amp_increment = 1/5

  running = True
  while running:
    is_left_mouse_pressed = False
    pressed_menu_item_index = -1

    # poll for events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        is_left_mouse_pressed, _, _ =  pygame.mouse.get_pressed()
    
    if game_menu.is_difficulty_selected():
      difficulty = game_menu.get_difficulty()
      running = False


    screen.fill(colors.BLACK)
    mouse_pos = pygame.mouse.get_pos()
    menu_item_rects = game_menu.draw(screen, menu_start_pos, mouse_pos=mouse_pos)

    # TODO: Move to a class/function
    pygame.draw.rect(screen, colors.BLUE, (0, screen.get_height()//2, screen.get_width(), screen.get_height()//2 ))
    draw_sin_wave(screen, screen.get_width(), colors.LIGHT_BLUE, screen.get_height()//2, shift=offset, amplitude=amplitude, spread=7, frequency=0.02)
    draw_sin_wave(screen, screen.get_width(), colors.LIGHT_BLUE, screen.get_height()//2, shift=1, amplitude=amplitude, spread=7, frequency=0.02)

    if amplitude <= -10:
      amp_increment = 1/5
    if amplitude >= 10:
      amp_increment = -1/5
    amplitude += amp_increment

    offset += 1/30
    
    
    if is_left_mouse_pressed:
      pressed_menu_item_index = get_mouse_colliding_rect(mouse_pos, menu_item_rects)
      game_menu.press(pressed_menu_item_index)


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

  return difficulty


def main() -> None:
  pygame.init()
  screen = pygame.display.set_mode((1280, 720))
  clock = pygame.time.Clock()

  difficulty = main_menu(screen, clock)
  if difficulty == -1:
    return
  
  game_loop(screen, clock, difficulty)

if __name__ == "__main__":
  main()