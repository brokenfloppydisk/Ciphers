import time
from string import ascii_lowercase
from alphabet import shift_text
from aristocrat import distributions
from math import log10

def compare_functions(*functions) -> None:
    for index, function in enumerate(functions):
        start_time = time.time()
        function()
        print(f"Function {index} execution time: {time.time() - start_time}")

# Compare dictionary comprehension vs. dict(zip())
compare_functions(
    lambda : {ascii_lowercase[i] : shift_text(ascii_lowercase, 1)[i] for i in range(26)},
    lambda : dict(zip(ascii_lowercase, shift_text(ascii_lowercase, 1)))
)



def digits_log10(string: str):
    distribution = distributions(string)

    for letter in ascii_lowercase:
        # make sure the letters are spaced evenly according to the numbers
        # If the letter's distribution is not 0, log10 gets the number of digits
        # If the letter's distribution is 0, make it have 1 digit by default
        num_digits = (1 if distribution[letter] == 0 else int(log10(distribution[letter])) + 1)
        letters = letter + ( " " * (num_digits - 1)) + " "
        numbers = str(distribution[letter]) + " "

def digits_convert_to_string(string: str):
    distribution = distributions(string)

    for letter in ascii_lowercase:
        value = str(distribution[letter])
        letters = value + ( " " * len(value)) + " "
        numbers = value + " "

# Compare text creation with log10 or with string conversion, string conversion is 2-3x faster
compare_functions(lambda : digits_log10("hi"), lambda : digits_convert_to_string("hi"))