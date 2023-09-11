from bottle import Bottle

import random

def shuffle_move_water(bottles: list[Bottle], from_index: int, to_index: int, amount: int) -> bool:
  """
  Move an amount from the top water segment to another bottle.

  Args:
      bottles (list[Bottle]): The bottles
      from_index (int): The index of the bottle to remove water from
      to_index (int): The index of the bottle to add water to
      amount (int): The amount of water to move.

  Returns:
      bool: True if a move was successful else False
  """
  from_bottle = bottles[from_index]
  to_bottle = bottles[to_index]

  water = from_bottle.pop_water(amount)
  if water == None:
    return False
  
  suc = to_bottle.push_water(water)

  return suc

def shuffle_bottles(bottles: list[Bottle], move_count: int) -> None:
  """
  Randomly shuffle the water segments in  the bottles `move_count` amount of times.

  Args:
      bottles (list[Bottle]): The bottles to be shuffled.
      move_count (int): The amount of shuffles to make.
  """
  i = 0
  while i < move_count:
    from_index = random.randint(0, len(bottles) - 1)
    to_index = random.randint(0, len(bottles) - 1)

    if from_index == to_index:
      continue

    from_bottle_top = bottles[from_index].get_top_water()
    if from_bottle_top == None:
      continue

    max_amount = min(bottles[to_index].get_remaining_capacity(), from_bottle_top.amount)
    if max_amount <= 0:
      continue

    amount = random.randint(1, max_amount)
    
    suc = shuffle_move_water(bottles, from_index, to_index, amount)
    if not suc:
      continue

    i += 1
