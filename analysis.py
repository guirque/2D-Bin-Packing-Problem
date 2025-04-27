import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import time
from main import construct_solution, generate_random_items

df = pd.DataFrame([], columns=['time taken', 'Num of Items', 'Bin Size X', 'Bin Size Y', 'Result (Num of Bins)'])

def run(bin_size, num_of_items, df):
    items = generate_random_items(num_of_items, bin_size)
    time_taken = time()
    solution = construct_solution(items, bin_size, save_img=False)
    time_taken = time() - time_taken

    df.loc[len(df)] = [time_taken, num_of_items, bin_size[0], bin_size[1], solution[1]]
    print(f"--> Finished step with {num_of_items} items in bin of size {bin_size[0]}x{bin_size[1]}: {time_taken}s")
    return time_taken
    

num_of_items = range(0, 5100, 100)
bin_size = [(pow(10, x), pow(10, x)) for x in range(1, 3)] # 10x10 and 100x100

plt.xlabel('Num Of Items')
plt.ylabel('Time Taken (s)')
plt.title('Num of Items x Time Taken')

for bin_size_value in bin_size:
    y = []
    for num_of_items_value in num_of_items:
        time_taken = run(bin_size_value, num_of_items_value, df)
        y.append(time_taken)
    plt.plot(num_of_items, y, label=f"{bin_size_value[0]}x{bin_size_value[1]} Bin")
        
plt.legend()
plt.savefig('analysis/results.png')

print(df)
df.to_csv('analysis/results.csv')