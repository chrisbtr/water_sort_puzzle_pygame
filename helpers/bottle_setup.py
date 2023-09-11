from bottle import Bottle, Water, copy_bottles

ColorValue = tuple[int, int, int]
WaterColorMap = dict[int, ColorValue]

def init_bottles(empty_count: int, color_count: int, bottle_capacity: int, water_id_map: dict[int, ColorValue]) -> list[Bottle]:
  water_segments: list[Water] = []
  for water_id in list(water_id_map.keys())[:color_count]:
    color = water_id_map[water_id]
    water_segments.append(Water(water_id, bottle_capacity, color))

  bottles: list[Bottle] = []
  for i in range(color_count): 
    bottles.append(Bottle(bottle_capacity, [water_segments[i]]))
  
  for i in range(empty_count):
    bottles.append(Bottle(bottle_capacity, []))

  return bottles

def find_largest_bottle_cap(bottles: list[Bottle]) -> int:
  largest_bottle_cap_index = -1
  largest_bottle_cap = float('-inf')
  for index, bottle in enumerate(bottles):
    bottle_cap =  bottle.get_remaining_capacity()

    if not bottle.is_empty() and bottle_cap != 0 and largest_bottle_cap < bottle_cap:
      largest_bottle_cap_index = index
      largest_bottle_cap = bottle_cap

  
  return largest_bottle_cap_index

def find_smallest_bottle_cap(bottles: list[Bottle]) -> int:
  smallest_bottle_cap_index = -1
  smallest_bottle_cap = float('inf')
  for index, bottle in enumerate(bottles):
    bottle_cap =  bottle.get_remaining_capacity()

    if not bottle.is_empty() and bottle_cap != 0 and smallest_bottle_cap >= bottle_cap:
      smallest_bottle_cap_index = index
      smallest_bottle_cap = bottle_cap

  return smallest_bottle_cap_index

def top_off_bottles(bottles: list[Bottle], history: list[list[Bottle]] = []) -> None:
  largest_bottle_cap_index = find_largest_bottle_cap(bottles)
  smallest_bottle_cap_index = find_smallest_bottle_cap(bottles)

  while largest_bottle_cap_index != -1 and smallest_bottle_cap_index != -1 and smallest_bottle_cap_index != largest_bottle_cap_index:
    from_bottle = bottles[largest_bottle_cap_index]
    to_bottle = bottles[smallest_bottle_cap_index]

    water = from_bottle.pop_water(1)
    if not to_bottle.push_water(water):
      from_bottle.push_water(water)
      return
    
    history.append(copy_bottles(bottles))
    
    largest_bottle_cap_index = find_largest_bottle_cap(bottles)
    smallest_bottle_cap_index = find_smallest_bottle_cap(bottles)

    

