# Import a list of the lowercase ascii characters from the default python string module
from string import ascii_lowercase
# Import the Alphabet type from alphabet
from alphabet import Alphabet

def flip(alphabet: Alphabet) -> Alphabet:
    """Returns the alphabet with the plaintext and ciphertext swapped.
    """
    # Return a dictionary with value : key for key : value in the original dictionary
    return {alphabet[item] : item for item in alphabet}

def encrypt(text: str, alphabet: Alphabet) -> str:
    """Returns the plaintext encrypted using the alphabet.
    """

    output = ""

    # Output the ciphertext letter corresponding to each plaintext letter
    for character in text:
        # Check if the character is a letter
        if (character.isalpha()):
            # Add the corresponding ciphertext letter
            output += alphabet[character.lower()]
        else:
            # Output the original character if it is not a letter
            output += character

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

    # Make a dictionary of distributions with 0 assigned to each letter
    letter_count = {i : 0 for i in ascii_lowercase}

    # Add 1 to the letter count for each character that is a letter
    for character in text:
        if (character.isalpha()):
            letter_count[character.lower()] += 1
    
    return letter_count

def distribution_table(text: str, percentages: bool=False) -> str:
    """Prints the letter distribution table for a piece of text.
    """
    # Get the distributions of the letters
    distribution = distributions(text)

    # Top and bottom rows of the table
    letters = ""
    numbers = ""

    for letter in ascii_lowercase:
        value = str(distribution[letter])
        # Add the letter, and then add whitespace to match the number of digits
        letters += letter + ( " " * len(value)) + " "
        # Add the number of times the letter appears
        numbers += value + " "
    
    # Return the table as a single string
    return "Letter distribution:\n" + letters + "\n" + numbers + "\n"


def patristocrat(text: str) -> str:
    """Returns the text formatted as a patristocrat
    """
    formatted_text = ""

    # Remove non-ascii characters
    for character in text:
        # Check if the lowercase version of the character is a lowercase letter
        if character.lower() in ascii_lowercase:
            # Add it to the formatted text if it is a letter
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
