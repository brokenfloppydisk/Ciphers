# Import from standard python modules
from string import ascii_lowercase
from typing import NewType 

Alphabet = NewType("Alphabet", dict)
Text = NewType("Text", str)

def shift_text(list: list, shift: int) -> list:
    """Shifts a list by the shift amount and returns it
    """
    new_list = list.copy()
    for _ in range(shift % 26):
        # Move items from the end of the list to the front
        new_list.insert(0, new_list.pop(25))
    return new_list

def keyword_text(keyword: str) -> str:
    """Generates a dict 
    """
    # Normalize keyword (remove duplicates and make lowercase)
    new_keyword = ""
    for i in keyword.lower():
        if i not in new_keyword:
            new_keyword += i
    keyword = new_keyword

    # Get letters not in keyword
    text = [i for i in ascii_lowercase if i not in keyword]
    # Add keyword to start of alphabet
    text[:0] = list(keyword)
    
    # Convert to string
    text = "".join(text)

    return text

def k_1_alphabet(shift: int) -> Alphabet:
    """Returns a K1 alphabet with the shift.
    """
    return {ascii_lowercase[i] : ascii_lowercase[(i + shift) % 26] for i in range(26)}

def k_2_alphabet(shift: int, keyword: str) -> Alphabet:
    """Returns a K2 alphabet with the shift and keyword.
    """
    ct_alphabet = shift_text(keyword_text(keyword), shift)
    return {ascii_lowercase[i] : ct_alphabet[i] for i in range(26)}

def k_3_alphabet(shift_1: int, shift_2: int, keyword: str) -> Alphabet:
    """Returns a K3 alphabet with the shifts and keyword.
    """
    pt_alphabet = keyword_text(keyword)
    ct_alphabet = shift_text(pt_alphabet, shift_2)
    pt_alphabet = shift_text(pt_alphabet, shift_1)

    return {pt_alphabet[i] : ct_alphabet[i] for i in range(26)}

def k_4_alphabet(shift_1: int, shift_2: int, keyword_1: str, keyword_2: str) -> Alphabet:
    """Returns a K4 alphabet with the shifts and keywords.
    """

    pt_alphabet = shift_text(keyword_text(keyword_1), shift_1)
    ct_alphabet = shift_text(keyword_text(keyword_2), shift_2)

    return {pt_alphabet[i] : ct_alphabet[i] for i in range(26)}