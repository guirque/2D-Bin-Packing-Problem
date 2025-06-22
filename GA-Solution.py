from main import generate_random_items, construct_solution
import numpy as np
from time import time
import math
import matplotlib.pyplot as plt
from random import random, choices

# CROSSING OVER METHODS ########################################################################################

class crossover_class:
    def crossover(self, individual1, cost_individual1, individual2, cost_individual2):
        raise Exception("Function not implemented error")

class half(crossover_class):

    def crossover(self, individual1, cost_individual1, individual2, cost_individual2):
        """
            Returns a resulting individual.
            Each individual is a list of lists.  
            Each sublist has the following format: [id, width, height].
            
            Respects the order of items of the first half of the fittest individual.  
            The other half respects the order of items from the other individual.
        """

        # Declaring individuals
        fittest_individual = individual1 if cost_individual1 < cost_individual2 else individual2
        other_individual = individual2

        # Splitting
        fittest_half = np.array([item for item in fittest_individual][:math.floor(len(fittest_individual)/2)]) # half the items in fittest_individual
        other_half = np.array([item for item in other_individual if item[0] not in fittest_half[:, 0]]) # all items in other_individual that are not in the fittest_half (the result preserves the order of other_half).

        #print(f'FITTEST HALF -------------------------------------\n{fittest_half}')
        #print(f'OTHER HALF -------------------------------------\n{other_half}')

        # Creating New Individual
        new_individual = np.concat([fittest_half.copy(), other_half.copy()], axis=0)

        # For testing:
        #print(f'Original size: {len(fittest_individual)}.\nResulting size: {len(new_individual)}.\nSorted unique elements: {np.unique(new_individual, axis=0)};\nSorted unique elements size: {len(np.unique(new_individual, axis=0))}')

        return new_individual

# HELPERS ######################################################################################################

def log(msg, initial_time):
    print(f'[{math.trunc(time() - initial_time)}s] {msg}')

def get_greedy_solution(items, bin_size):
    """
    # Returns
    (list of items and their positions, num_bins, sorted_items). Each item is of format:
    [width, height, pos_x, pos_y].

    You can recreate the solution by trying to fit each item in new bins, respecting the order and position of each item.
    """
    
    getAreas = lambda items : [item[0]*item[1] for item in items]
    items_areas = getAreas(items) # areas of items
    sorted_indices = np.argsort(items_areas) # indices that would sort the array (from lowest to biggest)

    # Sorted items (from biggest to lowest)
    items = items[list(reversed(sorted_indices))]

    solution = construct_solution(items, bin_size)

    return (solution[0], solution[1], items)

def random_swap_k_percent(items, k=0.2):
    num_items = len(items)
    num_of_pairs = math.floor(k*num_items)

    for i in range(0, num_of_pairs):

        # Choose a random pair
        rand_i = math.floor(random()*num_items)
        rand_j = math.floor(random()*num_items)

        # Swap
        #print(f"{items[rand_i]} <-> {items[rand_j]}")
        temp = np.copy(items[rand_i])
        items[rand_i] = np.copy(items[rand_j])
        items[rand_j] = temp
        
def get_individual_without_indices(items_with_indices):
    copy = []
    for item in items_with_indices:
        copy.append([item[1], item[2]])
    return np.array(copy)

def binary_tournament(population, population_costs):
    """
        Returns two indices of individuals from a population, in a tuple of format (i, j).
    """
    
    def choose_random_index_except(population, except_list):
        size = len(population)
        random_i = math.floor(random()*size)
        while random_i in except_list:
            random_i = math.floor(random()*size)
        return random_i

    # Choosing Individuals
    i = choose_random_index_except(population, [])
    j = choose_random_index_except(population, [i])

    # Choose fittest

    chosen_index = i if min(population_costs[i], population_costs[j]) == population_costs[i] else j


    # Choose 2 more and select fittest
    i = choose_random_index_except(population, [chosen_index])
    j = choose_random_index_except(population, [chosen_index, i])

    # Choose fittest

    chosen_index_2 = i if min(population_costs[i], population_costs[j]) == population_costs[i] else j

    return (chosen_index, chosen_index_2)

# GA ###########################################################################################################

# Genetic Algorithms ->
# PS: might be a good idea to tag items, so they will be properly crossed over (without repetitions)
# - Crossover: 
#       "ALTERNATE": get alternate snippets (sequences of items), of size K, and merge them into a solution. If num_items % K != 0, a final snippet of lower size will be used.
#       "HALF": get half from each parent.
#       "FITTEST_K": get K% from the fittest parent and (100-K)% from the other parent.
# - Mutation:
#       "RANDOM_SWAP_K": swap K random pairs of items. 
# - Stop criteria: time
# - How to choose parent: binary tournament

def ga_2D_bin_packing(items:list[list[2]], bin_size:tuple, time_limit:float, population_size:int = 5, crossover_mode:str="ALTERNATE", mutation_mode:str="RANDOM_SWAP_K", mutation_prob:float=0.02):
    """
    Genetic algorithm to solve the 2D bin packing problem.
    - Stop criteria: time.
    - How parent is chosen: binary tournament.

    Important aspect: an individual is treated as a list of items. That is because the list of items can be used to recreate the solution with `construct_solution`.
    To check a solution, `construct_solution(individual, bin_size)`.

    # Arguments
        - items: list of items. Items are lists of format (width, height).
        - bin_size: tuple (width, height). Bin size.
        - time_limit: approximate execution time limit, in seconds.
        - population_size: number of individuals.
        - crossover_mode: 
            - "ALTERNATE": get alternate snippets (sequences of items), of size K, and merge them into a solution. If num_items % K != 0, a final snippet of lower size will be used.
            - "HALF": get half from each parent.
            - "FITTEST_K": get K% from the fittest parent and (100-K)% from the other parent.
        - mutation_mode:
            - "RANDOM_SWAP_K": swap K random pairs of items.
            - "RANDOM_SWAP_K_PERCENT": swap K% random pairs of items.

    # Returns

    (best_solution_found, num_bins).

    best_solution_found is a list of items.
    """

    # Step by step
    # 1. Index items. IDs must be associated in order to ease differentiating items. They must be removed in the end.
    # 2. Generate solutions (populations).
    # 3. Evaluate solution qualities.
    # 4. Choose a pair of individuals. 
    # 5. Cross them over.
    # 6. Choose whether or not to mutate resulting solution.
    # 7. Choose individuals who will live (survive).
    # 8. Check stop condition.
    # 9. Repeat if stop condition is not met.
    # 10. Prepare final solution if stop condition is met.
    
    # PS.: It is important to keep a dictionary to hold the value of each individual (solution). Update it accordingly.

    # Declaring variables and constants
    initial_time = time()
    NUM_ITEMS = len(items)
    BIN_SIZE = bin_size
    indexed_items = []     # indexed_items: Numpy array of arrays of format [item_id, width, height]
    population_generations = []
    population_costs = []
    population = []
    best_cost = 0
    best_individual = None
    crossover_method = crossover_class()
    if crossover_mode == "HALF":
        crossover_method = half()
    

    # 0. Generate Individual with Greedy Method (which is our first individual)
    log(f"Crafting greedy individual", initial_time)
    greedy_solution_res = get_greedy_solution(items, BIN_SIZE)
    greedy_individual = greedy_solution_res[2]                      # individuals are lists of items, not the solutions themselves, for this algorithm

    # ----------------------------------------------
    # 1. Index items. IDs must be associated in order to ease differentiating items. They must be removed in the end.

    for i in range(0, len(greedy_individual)):
        indexed_items.append([i, greedy_individual[i][0], greedy_individual[i][1]])
    indexed_items = np.array(indexed_items)

    # adding greedy individual to population
    population_costs.append(greedy_solution_res[1])
    GREEDY_COST = greedy_solution_res[1]
    population.append(indexed_items)
    population_generations.append(0)

    #print("----------------- Items \n", indexed_items)

    # ----------------------------------------------
    # 2. Generate remaining individuals (population).
    # Do so by randomizing positions of the indexed items and making individuals.
    # Items were already indexed according to the greedy individual.

    for i in range(1, population_size):
        indexed_items_copy = np.copy(indexed_items)
        
        log(f"Crafting individual {i}", initial_time)

        # Generating individual (perform a RANDOM_SWAP_20%)
        random_swap_k_percent(indexed_items_copy, k=0.2)
        population.append(indexed_items_copy)
        population_generations.append(0)

        # Calculating cost
        individual_without_indices = get_individual_without_indices(population[i])
        population_costs.append(construct_solution(individual_without_indices, BIN_SIZE)[1])

    log(f"Populations created successfully.\n      Lowest cost (number of bins): {min(population_costs)}\n      Costs: {population_costs}", initial_time)
    
    # ----------------------------------------------
    # 3. Evaluate solution qualities.

    best_individual_cost_index = population_costs.index(min(population_costs))
    best_individual = np.copy(population[best_individual_cost_index])
    best_cost = min(population_costs)

    while(time() - initial_time < time_limit):
        
        # ----------------------------------------------
        # 4. Choose a pair of individuals.

        pair = binary_tournament(population, population_costs)

        log(f'Pair of individuals of indices {pair[0]} and {pair[1]} (costs {population_costs[pair[0]]} and {population_costs[pair[1]]}) were chosen for a crossover.', initial_time)

        #(f'Pair chosen: {population[pair[0]]}, {population[pair[1]]}. \n Costs: {population_costs[pair[0]]}, {population_costs[pair[1]]}')

        # ----------------------------------------------
        # 5. Cross them over.

        new_individual = crossover_method.crossover(population[pair[0]], population_costs[pair[0]], population[pair[1]], population_costs[pair[1]])
        new_individual_cost = construct_solution(get_individual_without_indices(new_individual), BIN_SIZE)[1]
        new_individual_generation = max(population_generations[pair[0]], population_generations[pair[1]]) + 1

        log(f'New individual created, of cost {new_individual_cost} and generation {new_individual_generation}.', initial_time)

        if new_individual_cost < best_cost:
            best_individual = np.copy(new_individual)
            best_cost = new_individual_cost
            log(f'-----> NEW BEST COST OBTAINED (after mutation): {new_individual_cost}.', initial_time)

        # ----------------------------------------------
        # 6. Choose whether or not to mutate resulting solution.

        mutate_new_individual = choices([True, False], [mutation_prob, 1-mutation_prob])[0]
        #mutate_new_individual = True

        if mutate_new_individual:

            # RANDOM SWAP 40%
            random_swap_k_percent(new_individual, k=0.4)

            new_individual_cost = construct_solution(get_individual_without_indices(new_individual), BIN_SIZE)[1]

            log(f'New individual went over a mutation... New cost: {new_individual_cost}', initial_time)

            # Check if the new individual has the best cost found
            if new_individual_cost < best_cost:
                best_individual = np.copy(new_individual)
                best_cost = new_individual_cost
                log(f'-----> NEW BEST COST OBTAINED (after mutation): {new_individual_cost}.', initial_time)

        # ----------------------------------------------
        # 7. Choose individuals who will live (survive).
        # The one to die is replaced by the new individual.
        # Strategy: choose the individual of oldest generation to die.

        # Calculating individual of oldest generation.
        index_oldest_generation_individual = population_generations.index(min(population_generations))
        log(f'Individual {index_oldest_generation_individual}, of generation {population_generations[index_oldest_generation_individual]}, has died.', initial_time)

        # Replacing individual with new one.

        population[index_oldest_generation_individual] = new_individual
        population_costs[index_oldest_generation_individual] = new_individual_cost
        population_generations[index_oldest_generation_individual] = new_individual_generation

        # ----------------------------------------------
        # 8. Check stop condition (done with while loop).
        # ----------------------------------------------
        # 9. Repeat if stop condition is not met (done with while loop).
        
    # ----------------------------------------------
    # 10. Prepare final solution if stop condition is met.

    log(f'Population costs: {population_costs}', initial_time)
    log(f'\nGreedy cost: {GREEDY_COST}\nBest cost obtained: {best_cost}', initial_time)
    return (best_individual, best_cost)


# MAIN #############################################################################

BIN_SIZE = (10,10)

random_items = generate_random_items(500, BIN_SIZE, seed=1000)

results = ga_2D_bin_packing(random_items, (10,10), 60, population_size=10, crossover_mode="HALF", mutation_prob=0.2)