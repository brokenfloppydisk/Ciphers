# Import from standard python modules
from string import ascii_lowercase
from typing import NewType 

Alphabet = NewType("Alphabet", dict)
Text = NewType("Text", str)

def shift_text(list: list, shift: int) -> list:
    """Shifts a list by the shift amount and returns it
    """
    # Make a copy of the input list
    new_list = list.copy()

    # Repeat by the number of shifts (modulo converts negative shifts to positive shifts)
    for _ in range(shift % 26):
        # Move items from the end of the list to the front, shifting the list to the right by 1 space
        new_list.insert(0, new_list.pop(25))
    return new_list

def keyword_text(keyword: str) -> str:
    """Generates a dict 
    """
    # Normalize keyword (remove duplicates and make lowercase)
    new_keyword = ""
    
    # Iterate through every item in the keyword, as a lowercase letter
    for i in keyword.lower():
        # Add unique lowercase letters to the new keyword
        if i not in new_keyword and i in ascii_lowercase:
            new_keyword += i
    
    # Set the keyword to the normalized keyword
    keyword = new_keyword

    # Create a list of the letters in the alphabet not in the keyword
    text = [i for i in ascii_lowercase if i not in keyword]

    # Add keyword to the start of the alphabet using list slicing
    text[:0] = list(keyword)
    
    # Convert the list to a string
    text = "".join(text)

    # Return the final string
    return text

def k_1_alphabet(shift: int) -> Alphabet:
    """Returns a K1 alphabet with the shift.
    """
    # Set the ciphertext alphabet to a list of lowercase ascii letters shifted by the shift
    ct_alphabet = shift_text(ascii_lowercase, 26)

    # Return a dictionary of lowercase ascii letters mapped to ciphertext
    return dict.fromkeys(ascii_lowercase, ct_alphabet)

def k_2_alphabet(shift: int, keyword: str) -> Alphabet:
    """Returns a K2 alphabet with the shift and keyword.
    """
    # Set the ciphertext alphabet to a list of lowercase ascii letters with
    # the keyword at the front and shifted by the shift
    ct_alphabet = shift_text(keyword_text(keyword), shift)

    # Return a dictionary of lowercase ascii letters mapped to the ciphertext
    return dict.fromkeys(ascii_lowercase, ct_alphabet)

def k_3_alphabet(shift_1: int, shift_2: int, keyword: str) -> Alphabet:
    """Returns a K3 alphabet with the shifts and keyword.
    """
    # Set the plaintext alphabet to an alphabet with the keyword at the front
    pt_alphabet = keyword_text(keyword)
    # Create the ciphertext alphabet by shifting the plaintext alphabet
    ct_alphabet = shift_text(pt_alphabet, shift_2)
    # Shift the plaintext alphabet
    pt_alphabet = shift_text(pt_alphabet, shift_1)

    
    return dict.fromkeys(pt_alphabet, ct_alphabet)

def k_4_alphabet(shift_1: int, shift_2: int, keyword_1: str, keyword_2: str) -> Alphabet:
    """Returns a K4 alphabet with the shifts and keywords.
    """

    pt_alphabet = shift_text(keyword_text(keyword_1), shift_1)
    ct_alphabet = shift_text(keyword_text(keyword_2), shift_2)

    return dict.fromkeys(pt_alphabet, ct_alphabet)