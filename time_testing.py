import time
from string import ascii_lowercase
from alphabet import shift_text

def dictionary_comprehension(list_a: list, list_b: list):
    start_time = time.time()
    comprehension = {list_a[i] : list_b[i] for i in range(26)}
    print(f"Execution time: {time.time() - start_time}")
    start_time = time.time()
    constructor = dict(zip(list_a, list_b))
    print(f"Execution time: {time.time() - start_time}")

dictionary_comprehension(ascii_lowercase, shift_text(list(ascii_lowercase), 3))