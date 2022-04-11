from string import ascii_lowercase
from typing import NewType

Alphabet = NewType("Alphabet", dict)
Text = NewType("Text", str)

def shift_text(input_list: list, shift: int, left: bool = True) -> list:
    """Shifts a list by the shift amount and returns it
    """
    # Make a copy of the input list
    shifted_list = list(input_list).copy()

    # Convert a left shift to a right shift (equivalent left shift + right shift = 26)
    if left:
        shift = 26 - shift

    # Perform a modulus on the shift to keep it in the range of 0 to 25.
    shift = shift % 26

    # Repeat by the number of shifts
    for _ in range(shift):
        # Move an from the end of the list to the front
        # shifts the list to the right by 1 space
        shifted_list.insert(0, shifted_list.pop(25))
    
    # Return the shifted list
    return shifted_list

def keyword_text(keyword: str) -> str:
    """Generates the alphabet starting with the keyword 
    and continuing in alphabetical order.
    """
    # Create an empty keyword to use as the normalized keyword
    normalized_keyword = ""
    
    # Iterate through every item in the keyword, as a lowercase letter
    for i in keyword.lower():
        # Add unique lowercase letters to the normalized keyword
        if i not in normalized_keyword and i in ascii_lowercase:
            normalized_keyword += i
    
    # Set the keyword to the normalized keyword
    keyword = normalized_keyword

    # Create a list of the letters in the alphabet not in the keyword
    # using a list comprehension
    text = [i for i in ascii_lowercase if i not in keyword]

    # Add keyword to the start of text using list slicing
    text[:0] = list(keyword)
    
    # Concatenate all of the items in the text list to form a string
    text = "".join(text)

    # Return the final string
    return text

def k_1_alphabet(shift: int = None) -> Alphabet:
    """Returns a K1 alphabet with the shift.
    """
    # If shift is not set, prompt user to enter it.
    shift = (_set_shift() if shift is None else shift)

    # Set the ciphertext alphabet to a list of lowercase ascii letters shifted by the shift
    ct_alphabet = shift_text(list(ascii_lowercase), shift)

    # Return a dictionary of lowercase ascii letters mapped to ciphertext
    return dict(zip(ascii_lowercase, ct_alphabet))

def k_2_alphabet(shift: int = None, keyword: str = None) -> Alphabet:
    """Returns a K2 alphabet with the shift and keyword.
    """
    # If shift or keyword are not set, prompt user to enter them.
    shift = (_set_shift() if shift is None else shift)
    keyword = (input("Please enter a keyword") if keyword is None else keyword)

    # Set the ciphertext alphabet to a list of lowercase ascii letters with
    # the keyword at the front and shifted by the shift
    ct_alphabet = shift_text(keyword_text(keyword), shift)

    # Return a dictionary of lowercase ascii letters mapped to the ciphertext
    return dict(zip(ascii_lowercase, ct_alphabet))

def k_3_alphabet(shift_1: int = None, shift_2: int = None, keyword: str = None) -> Alphabet:
    """Returns a K3 alphabet with the shifts and keyword.
    """
    # If shift or keyword are not set, prompt user to enter them.
    shift_1 = (_set_shift() if shift_1 is None else shift_1)
    shift_2 = (_set_shift() if shift_2 is None else shift_2)
    keyword = (input("Please enter a keyword") if keyword is None else keyword)

    # Set the plaintext alphabet to an alphabet with the keyword at the front
    pt_alphabet = keyword_text(keyword)

    # Create the ciphertext alphabet by shifting the plaintext alphabet
    ct_alphabet = shift_text(pt_alphabet, shift_2)

    # Shift the plaintext alphabet
    pt_alphabet = shift_text(pt_alphabet, shift_1)

    # Return a dictionary mapping the plaintext to the ciphertext.
    return dict(zip(pt_alphabet, ct_alphabet))

def k_4_alphabet(shift_1: int = None, shift_2: int = None, 
                 keyword_1: str = None, keyword_2: str = None) -> Alphabet:
    """Returns a K4 alphabet with the shifts and keywords.
    """
    # If shift or keyword are not set, prompt user to enter them.
    shift_1 = (_set_shift() if shift_1 is None else shift_1)
    shift_2 = (_set_shift() if shift_2 is None else shift_2)
    keyword_1 = (input("Please enter a keyword. ") if keyword_1 is None else keyword_1)
    keyword_2 = (input("Please enter a keyword. ") if keyword_2 is None else keyword_2)

    # Create the plaintext alphabet by creating an alphabet with the 
    # first keyword at the front, and shifting it by the first shift.
    pt_alphabet = shift_text(keyword_text(keyword_1), shift_1)

    # Create the ciphertext alphabet in the same way, 
    # but using the second keyword and shift.
    ct_alphabet = shift_text(keyword_text(keyword_2), shift_2)

    # Return a dictionary mapping the plaintext to the ciphertext.
    return dict(zip(pt_alphabet, ct_alphabet))

def _set_shift() -> int:
    # Have the user set a shift and return it
    shift = input("Please enter a shift. ")
    while not shift.isdigit():
        shift = input("Invalid input. Please enter a number. ")
    return int(shift)