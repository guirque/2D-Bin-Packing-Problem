import matplotlib.pyplot as plt
import numpy as np
from utils.draw_bin import draw_bin

NUM_OF_ITEMS = 10
BIN_SIZE = 10 # BIN_SIZExBIN_SIZE

items = np.ceil(np.random.rand(NUM_OF_ITEMS, 2) * (BIN_SIZE))

getAreas = lambda items : [item[0]*item[1] for item in items]
items_areas = getAreas(items) # areas of items
sorted_indices = np.argsort(items_areas) # indices that would sort the array (from lowest to biggest)

# Sorted items (from biggest to lowest)
items = items[list(reversed(sorted_indices))]


def putItem(available_spaces, item_to_place):
    """
    Returns coordinates (bottom left) if placed. (-1, -1) if no space if available.
    Modifies available_spaces after item is placed.
    - available_spaces: array of available spaces. Each space is in the shape of (width, height, bottom_left_x, bottom_left_y)
    - item_to_place: [width, height] of item (rectangle) to place.
    """

    print(f"Available spaces:\n", available_spaces)
    print('\n')

    # Verify if there's space available
    # Bottom-left: look for the first available space that's more to the bottom-left. available_space should be ordered so this is true.
    item_width = item_to_place[0]
    item_height = item_to_place[1]

    for i in range(len(available_spaces)):
        space = available_spaces[i]

        space_dimensions = (space[0], space[1])
        space_position = (space[2], space[3])

        # Can you insert it?
        if space_dimensions[0] >= item_width and space_dimensions[1] >= item_height:
            
            # Update available spaces (split the available space into two more)

            # new positions to generate available spaces
            new_position_1 = (space_position[0], space_position[1] + item_height) # on top of item
            new_position_2 = (space_position[0] + item_width, space_position[1]) # next to item (to the right)

            # new available space dimensions
            new_dimensions_1 = (item_width, space_dimensions[1] - item_height) # available space on top of item
            new_dimensions_2 = (space_dimensions[0] - item_width, space_dimensions[1]) # available space to the right of item

            available_spaces = np.append(available_spaces, [np.array([new_dimensions_1[0], new_dimensions_1[1], new_position_1[0], new_position_1[1]])], axis=0)
            available_spaces = np.append(available_spaces, [np.array([new_dimensions_2[0], new_dimensions_2[1], new_position_2[0], new_position_2[1]])], axis=0)
            available_spaces = np.delete(available_spaces, i, axis=0) # delete the space that used to be available

            # Insert item (return the available spaces and its position)
            return (available_spaces, (space[2], space[3]))

    return None


#print(f'Generated items: \n', items)

# Executing algorithm -------------------------------------------------------------

available_spaces = np.array([[BIN_SIZE, BIN_SIZE, 0, 0]]) # initial available space is a whole bin
answers = np.array([np.array([0, 0, 0, 0])])




for i in range(len(items)):
    item = items[i]

    print('\n\n----- Analyzing new item -----')
    
    insert_result = putItem(available_spaces, item)
    if insert_result is not None:
        available_spaces = insert_result[0]
        coordinates = insert_result[1]

        print("Inserting: ", np.array([item[0], item[1], coordinates[0], coordinates[1]]))

        answers = np.append(answers, [np.array([item[0], item[1], coordinates[0], coordinates[1]])], axis=0)
        print(f'Successfully placed item on position ({coordinates[0]}, {coordinates[1]}).')
    else:
        print(f'Failed to insert item in bin. No more space available.')

answers = np.delete(answers, 0, axis=0)
print("\n\n----- Answers ------\n", answers)


# Drawing bin
draw_bin(BIN_SIZE, answers)