from __future__ import annotations
from water_wave import WaterWave

class Water:
  """
  The water used as contents for a `Bottle`.
  """
  def __init__(self, water_id: int, amount: int, color: tuple[int, int, int], name = "") -> None:
    """
    Args:
        water_id (int): The ID of the water used the check equality of Water instances.
        amount (int): The amount to water in this segment.
        color (tuple[int, int, int]): The color of this water segment.
        name (str, optional): An optional name for this water segment (used when printing). Defaults to "".
    """
    self.water_id = water_id
    self.amount = amount
    self.color = color
    self.name = name if name != "" else str(water_id)

    self.wave = WaterWave(0, 5)
  
  def __eq__(self, __o: object) -> bool:
    if not isinstance(__o, Water):
      return False
    
    return self.water_id == __o.water_id

  def copy(self) -> Water:
    """
    Creates a deep copy of this water segment.

    Returns:
        Water: A deep copy of this water segment.
    """
    return Water(self.water_id, self.amount, self.color, self.name)

  def split(self, new_water_amount: int) ->  Water | None:
    """
    Split this water segment into two segment one with `new_water_amount` as the amount
    and the other with the rest of the amount.

    Args:
        new_water_amount (int): The amount to be taken from the water segment

    Returns:
        Water | None: The new water segment that was split or None if `new_water_amount` is not a valid amount. 
    """
    if self.amount - new_water_amount <= 0:
      return None
    
    self.amount -= new_water_amount

    return Water(self.water_id, new_water_amount, self.color, self.name)

  
  def add_amount(self, amount: int) -> None:
    """
    Adds more water to the water segment.

    Args:
        amount (int): The amount to add to the water segment.
    """
    self.amount += amount
 

class Bottle:
  """A bottle that holds water segments"""

  def __init__(self, capacity: int = 1, contents: list[Water] = []) -> None:
    """
    Args:
        capacity (int, optional): The maximum amount of water the bottle can hold. Defaults to 1.
        contents (list[Water], optional): The initial contents of the bottle. Defaults to [].
    """
    self.capacity = max(capacity, sum(list(map(lambda w: w.amount, contents))))
    self.contents = contents
  
  def is_empty(self) -> bool:
    """Checks if the bottle has no water segments in its contents

    Returns:
        bool: Returns True if length `contents` is zero else return False
    """
    return len(self.contents) == 0
  
  def copy(self) -> Bottle:
    """
    Creates a deep copy of a bottle

    Returns:
        Bottle: Returns a deep copy of a bottle
    """
    return Bottle(self.capacity, self.get_contents())

  def get_contents(self) -> list[Water]:
    """
    Gets a deep copy of the bottles `contents`

    Returns:
        list[Water]: Returns a deep copy of the bottles `contents`
    """
    return [water.copy() for water in self.contents]
  
  def get_top_water(self) -> Water | None:
    """
    Gets the water segment at the top of the bottle

    Returns:
        Water | None: None if the bottles `contents` is empty else the water segment at the top of the bottle
    """
    if self.is_empty():
      return None

    return self.contents[len(self.contents) - 1]
  
  def pop_water(self, amount: int | None = None) -> Water | None:
    """
    Removes and returns an amount of the top water segment from the bottle

    Args:
        amount (int | None, optional): The amount of the water segment to pop. Defaults to None.

    Returns:
        Water | None: The popped water segment (if it was possible to do so)
    """
    if self.is_empty() or amount == 0:
      return None
    
    # get the water segment at the top of the bottle
    water = self.contents.pop()

    # if the amount is not specified return the entire water segment
    if amount == None or water.amount <= amount:
      return water
    
    # split the water segment by amount and put the remaining water 
    # back into the bottle
    split_water = water.split(amount)
    self.push_water(water)

    # if the water segment couldn't be split return None 
    if split_water == None:
      return None

    return split_water

  def get_remaining_capacity(self) -> int:
    """
    Get the remaining space in the bottle

    Returns:
        int: The remaining space in the bottle
    """
    return self.capacity - sum(list(map(lambda w: w.amount, self.contents)))

  def push_water(self, water: Water) -> bool:
    curr_top_water = self.get_top_water()

    if water.amount > self.get_remaining_capacity():
      return False

    if curr_top_water == None or curr_top_water != water:
      self.contents.append(water)
    else:
      curr_top_water.add_amount(water.amount)
    
    return True

  def __str__(self) -> str:
    bottle_str = ""
    for water in self.contents:
      bottle_str += "|" + water.name * water.amount
    bottle_str += "_" * self.get_remaining_capacity()

    return bottle_str


def move_water_segment(from_bottle: Bottle, to_bottle: Bottle) -> bool:
  """
  Moves the maximum amount of water from the top water segment in `from_bottle` to `to_bottle` 

  Args:
      from_bottle (Bottle): The bottle to remove water from.
      to_bottle (Bottle): The bottle to add water to.

  Returns:
      bool: Returns True if a move was made else returns False.
  """
  if from_bottle.is_empty():
    return False

  water_amount = min(from_bottle.get_top_water().amount, to_bottle.get_remaining_capacity()) 
  if to_bottle.is_empty() or from_bottle.get_top_water() == to_bottle.get_top_water():
    water = from_bottle.pop_water(water_amount)
    if water == None:
      return False
    
    return to_bottle.push_water(water)
  
  return False

def copy_bottles(bottles: list[Bottle]) -> list[Bottle]:
  """
  Creates a deep copy of `bottles`.

  Args:
      bottles (list[Bottle]): The bottles to make a deep copy of.

  Returns:
      list[Bottle]: A deep copy of `bottles`
  """
  return [b.copy() for b in bottles]
    
