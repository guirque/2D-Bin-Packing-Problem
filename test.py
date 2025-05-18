from main import generate_random_items, construct_solution
import numpy as np
from time import time
import math
import matplotlib.pyplot as plt


# Generating Random Items -----------------------------------------------------------------------------------

random_items = generate_random_items(200, (10, 10))
num_items = len(random_items)
BIN_SIZE = (10,10)
TIME_LIMIT = 120 # in seconds

# Solution: a list of items. Submit it to the construct solution algorithm to obtain its cost and filled bins.

# List of costs (to plot later on)
costs_obtained = []
# List of best costs (to plot later on)
best_costs_obtained = []
# List of quality obtained (to plot later on)
quality_obtained = []



def cost_function(solution):
    """
        Evaluates overall solution quality.
        Quality is calculated by:
        number_of_bins*bin_area - occupied_space_ratio_mean 
        
        This way, number_of_bins is prioritized.

        # Args
            solution: (item placement, number of bins)
    """
    item_placement = np.array(solution[0])
    num_of_bins = solution[1]
    BIN_AREA = float(BIN_SIZE[0]*BIN_SIZE[1])

    areas_occupied_ratio = np.multiply(item_placement[:, 0], item_placement[:, 1]) / BIN_AREA
    mean_area_occupied = np.mean(areas_occupied_ratio)
    
    quality = num_of_bins*BIN_AREA - mean_area_occupied

    return quality



# First Solution (using First Fit Decreasing) --------------------------------------------------------------

initial_time = time()

getAreas = lambda items : [item[0]*item[1] for item in items]
items_areas = getAreas(random_items) # areas of items
sorted_indices = np.argsort(items_areas) # indices that would sort the array (from lowest to biggest)

# Sorted items (from biggest to lowest)
random_items = random_items[list(reversed(sorted_indices))]


# First Solution
first_solution_results = construct_solution(random_items, bin_size=BIN_SIZE)
best_solution = current_solution = random_items
best_solution_cost = first_solution_results[1]
best_costs_obtained.append(best_solution_cost)
costs_obtained.append(best_solution_cost)

quality_obtained.append(cost_function(first_solution_results))


# ILS ------------------------------------------------------------------------------------------------------

log_date = lambda i, j: f'[{i}-{j} {math.trunc(time() - initial_time)}s]'

continue_local_search = True
while time() - initial_time < TIME_LIMIT:

    continue_local_search = True

    for i in range(num_items-1, -1, -1):
        if continue_local_search:
            for j in range(0, num_items):

                # Changing solution
                temp = np.copy(current_solution[j])
                current_solution[j] = np.copy(current_solution[i])
                current_solution[i] = temp

                # Execution
                new_solution_results = construct_solution(items=current_solution, bin_size=(10,10), save_img=False)
                
                if new_solution_results[1] < best_solution_cost:
                    #print(f'{log_date(i, j)} New best solution: {best_solution_cost} -> {new_solution_results[1]}')
                    best_solution = current_solution
                    best_solution_cost = new_solution_results[1]

                    continue_local_search = False
                    break

                #else:
                    #print(f'{log_date(i, j)} Solution obtained: {new_solution_results[1]}')
                
                costs_obtained.append(new_solution_results[1])
                quality_obtained.append(cost_function(new_solution_results))
                best_costs_obtained.append(best_solution_cost)
                
                if time() - initial_time >= TIME_LIMIT:
                    continue_local_search = False
                    break


# Results
print("---------------- FINAL RESULTS ----------------")
#print(f"Costs obtained: ", costs_obtained)
#print(f"Best Costs obtained: ", best_costs_obtained)
print(f"First solution (number of bins): {best_costs_obtained[0]}")
print(f"Best solution found (number of bins): {best_costs_obtained[-1]}")
print(f"Time taken: {time() - initial_time}s")

plt.title('Costs Obtained')
plt.plot(costs_obtained, label='Costs Obtained', marker='.')
plt.plot(best_costs_obtained, label='Best Costs Obtained')

plt.legend()
plt.savefig('ILS_results.png')

#construct_solution(best_solution, bin_size=BIN_SIZE, save_img=True)


plt.title('Changes in Quality')
plt.figure()
plt.plot(quality_obtained, label='Quality Obtained')
plt.savefig('Quality_Changes.png')