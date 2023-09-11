from bottle import Bottle, move_water_segment, copy_bottles
from helpers.shuffle import shuffle_bottles
from helpers.bottle_setup import init_bottles, top_off_bottles, WaterColorMap

class WaterSortPuzzle:
  """
  A class that maintains the state of the water sort puzzle
  """

  def __init__(self) -> None:
    self.bottles: list[Bottle] = []
    self.init_bottles: list[Bottle] = []

    self.history: list[list[Bottle]] = []

    self.selected_bottle_index = -1

  def create_bottles(self, empty_bottle_count: int, colored_bottle_count: int, bottle_capacity: int, water_color_map: WaterColorMap, shuffle_moves: int) -> None:
    """
    Set up the state to start the water sort puzzle.

    Args:
        empty_bottle_count (int): Number of empty bottles on the stage.
        colored_bottle_count (int): Number of bottles with colored water segments in them on the stage.
        bottle_capacity (int): The maximum amount of water a bottle can hold.
        water_color_map (WaterColorMap): The colors different of the water.
        shuffle_moves (int): The number of times the water segments in the bottles are shuffled.
    """
    self.selected_bottle_index = -1
    self.history = []
    
    self.init_bottles = init_bottles(empty_bottle_count, colored_bottle_count, bottle_capacity, water_color_map)
    shuffle_bottles(self.init_bottles, shuffle_moves)
    top_off_bottles(self.init_bottles)

    self.bottles = copy_bottles(self.init_bottles)
  
  def select_bottle(self, bottle_index: int) -> None:
    """
    If a bottle is already selected moves the top water segment into the bottle at `bottle_index` (if possible).
    If a bottle is not already selected sets the selected bottle to `bottle_index`.
    Else deselects selected bottle.

    Args:
        bottle_index (int): bottle to be selected.
    """
    if bottle_index < 0 or self.selected_bottle_index == bottle_index:
      self.selected_bottle_index = -1

    elif self.selected_bottle_index < 0:
      self.selected_bottle_index = bottle_index
    
    elif self.selected_bottle_index >= 0 and bottle_index >= 0:
      tmp_bottles = copy_bottles(self.bottles)
      suc = move_water_segment(self.bottles[self.selected_bottle_index], self.bottles[bottle_index])
      if suc:
        self.history.append(tmp_bottles)
      
      self.selected_bottle_index = -1
  
  def is_puzzle_solved(self) -> bool:
    """
    Checks if each bottle is full and contains the same water segment.

    Returns:
        bool: Returns True if puzzle was solved else returns False.
    """
    for bottle in self.bottles:
      if not (bottle.is_empty() or (len(bottle.get_contents()) == 1 and bottle.get_remaining_capacity() == 0)):
        return False
    return True

  def go_back(self) -> None:
    """Sets the bottles state to the previous valid move made."""
    if len(self.history) == 0:
      return

    self.bottles = self.history.pop()
    self.selected_bottle_index = -1
  
  def restart_puzzle(self) -> None:
    """Reset the bottles to there initial state."""
    self.bottles = copy_bottles(self.init_bottles)
    self.selected_bottle_index = -1
    self.history = []
    


    


