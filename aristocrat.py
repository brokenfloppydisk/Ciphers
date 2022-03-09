
from string import ascii_lowercase
from alphabet import Alphabet
from math import log10

def flip(alphabet: Alphabet) -> dict:
    """Returns the alphabet with the plaintext and ciphertext swapped.
    """

    return {alphabet[item] : item for item in alphabet}

def encrypt(text: str, alphabet: Alphabet) -> str:
    """Returns the plaintext encrypted using the alphabet.
    """

    output = ""

    # Add the corresponding letter from the ciphertext 
    # to the output for each plaintext letter
    for letter in text:
        if (letter.isalpha()):
            output += alphabet[letter.lower()]
        else:
            # Output the original character if it is not a letter
            output += letter

    return output

def decrypt(text: str, alphabet: Alphabet) -> str:
    """Returns the ciphertext decrypted using the alphabet.
    """

    # Switch the plaintext and ciphertext in the alphabet
    inverse_alphabet = flip(alphabet)

    # Encrypt with the inverse alphabet to decrypt
    return encrypt(text, inverse_alphabet)

def distributions(text: str) -> dict:
    """Returns a dictionary of letter distributions.
    """

    dist = {i : 0 for i in ascii_lowercase}

    for letter in text:
        if (letter.isalpha()):
            dist[letter.lower()] += 1
    
    return dist

def distribution_table(text: str, percentages: bool=False) -> str:
    """Prints the letter distribution table for a piece of text.
    """

    dist = distributions(text)

    letters = ""
    numbers = ""

    for letter in ascii_lowercase:
        # make sure the letters are spaced evenly according to the numbers
        num_digits = (1 if dist[letter] == 0 else int(log10(dist[letter])) + 1)
        letters += letter + ( " " * (num_digits - 1)) + " "
        numbers += str(dist[letter]) + " "
    
    return "Letter distribution:\n" + letters + "\n" + numbers + "\n"


def patristocrat(text: str) -> str:
    """Returns the text formatted as a patristocrat
    """
    formatted_text = ""

    for character in text:
        if character in ascii_lowercase:
            formatted_text += character

    text = formatted_text

    output = ""

    # Add each letter to the output
    for index, item in enumerate(text):
        output += item

        # Add a space after every fifth letter
        if (index + 1) % 5 == 0:
            output += " "
    
    # Return as all capitalized
    return output.upper()
