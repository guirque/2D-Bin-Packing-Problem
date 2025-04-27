import matplotlib.pyplot as plt
import numpy as np

def draw_bin(bin_size, items=[], filename='Bin.png'):

    plt.figure(figsize=bin_size)
    plt.title(label='Bin')

    # Set the scaling to a fixed interval (don't let it zoom in or out on the bin)
    plt.xlim(0, bin_size[0])
    plt.ylim(0, bin_size[1])
    
    for item in items:
        width = item[0]
        height = item[1]
        position = (item[2], item[3]) # bottom left corner position
    
        # fills in the area between two horizontal curves
        # plt.fill_between(x, y0, y1)
        # Curves are in a position defined by y. x is the interval (x0, x1)

        plt.fill_between([position[0], position[0] + width], position[1], position[1]+height,  where=None, alpha=0.8) # opacity is lower to make interpolations explicit
    plt.savefig('bins/' + filename)

# Example
# x, y and startingPosition (bottom left corner coordinates)
#draw_bin(10, np.array([[5, 3, 0, 0], [3, 3, 0, 3]]))