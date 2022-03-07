# Import modules (other files of code)
from typing import Tuple
import aristocrat as aristo
import alphabet as alpha
from string import ascii_lowercase
from alphabet import Alphabet

def get_menu_input(prompt: str, show_options: bool=False, *functions: Tuple, **function_dict) -> bool:
    """ Asks the user a question and performs a function depending on the answer.
    
    Returns True if a function was run, otherwise returns False

    *functions should be tuples of (str, function)

    **function_dict should be kwargs of function_name=function

    Unless the name of the function cannot be pre-determined, **function_dict should be used over *functions.
    """
    # Add functions to function dictionary
    for item in functions:
        name, function = item
        function_dict[name] = function

    options = "\nOptions: \n" + "\n".join([f"'{option}' for {function_dict[option].__name__}" for option in function_dict]) + "\n"

    function_executed = False

    # Loop if a function has not been executed
    while not function_executed:
        # Print the question and get the lowercase form of the answer
        user_input: str = input(prompt + " Type 'help' for more help. ").lower()

        # Exit from the loop and return False, as a function was not executed
        if user_input == "exit":
            break
        elif user_input == "help":
            print(options)
            continue
        # Check the keyword arguments to see if the input is assigned to a function
        elif user_input in function_dict:
            # Run the corresponding function
            function_dict[user_input]()
            function_executed = True
            break

        print("\nInvalid input!\n")
    
    return function_executed

def solve_cipher(quote: str, alphabet: Alphabet, use_patristo:bool=False) -> None:
    """ Prompt the user to solve a cipher by typing in letters to swap.
    """
    decryption_key = aristo.flip(alphabet)

    solved = False
    show_distribution = False

    # Encrypt the quote as a cipher using the provided alphabet
    encrypted_cipher = aristo.encrypt(quote, alphabet)
    if use_patristo:
        encrypted_cipher = aristo.patristocrat(encrypted_cipher)
    
    # Create a default Alphabet where each letter maps to itself
    # Equivalent to a k1 alphabet with a shift of 0
    user_alphabet = alpha.k_1_alphabet(0)

    while not solved:
        # Print question text
        print("Original Cipher:\n" + encrypted_cipher + 
            "\nYour decryption:\n" + aristo.encrypt(encrypted_cipher, user_alphabet) + "\n\n" + 
            "Your key:\n" +
            "Ciphertext (encrypted) letters: \n" + 
            " ".join(list(ascii_lowercase)) + "\n" + 
            "Plaintext (actual) letters: \n" + 
            " ".join([user_alphabet[letter] for letter in ascii_lowercase]) + "\n"
        )

        # Show the letter distributions if needed
        if (show_distribution):
            print(aristo.distribution_table(encrypted_cipher))
        
        # Print user options
        print("Enter letters to switch below: (for example, ab to decrypt a to b in your key)\n"
            + "Enter '.' to toggle the letter distribution.\n"
            + "Enter 'reset' to reset your letter mappings.\n"
            + "Enter 'exit' to exit."
            )
        
        # Get user input
        user_input: str = input("Input: ").lower()

        # Do different things based on user input

        # Exit if user input is 'exit'
        if user_input.lower() == "exit":
            break
        # Toggle the letter distribution if the user input is '.'
        elif user_input == ".":
            show_distribution = not show_distribution
        # Reset the user alphabet if the user input is 'reset'
        elif user_input == "reset":
            user_alphabet = alpha.k_1_alphabet(0)
        # Assign a letter in the plaintext to one in the ciphertext if the user input is two letters.
        elif len(user_input) == 2:
            if any(letter in user_input for letter in ascii_lowercase):
                user_alphabet[user_input[0]] = user_input[1]
        # Print 'Invalid input!' if the user input does not match anything
        else:
            print("-" * 80)
            print("\n\nInvalid input!\n\n")
            continue
        
        # Print 80 of '-' to act as a section divider.
        print("-" * 80)

        distributions = aristo.distributions(encrypted_cipher)
        
        # Check if user has solved the cipher
        solved = True
        for letter in user_alphabet:
            # Ignore checking letters that are not in the cipher
            if distributions[letter] == 0:
                continue
            # If a letter is incorrect, set solved to False
            if user_alphabet[letter] != decryption_key[letter]:
                solved = False
    
    # Print the end result
    if solved:
        print("Cipher decrypted!")
    else:
        print("Try again next time...")

def generate_cipher():
    """ TODO Prompt the user to generate a cipher.
    """

def __main__():
    get_menu_input("Welcome to cipher practice! Please enter an option from the list of options.",
    True,
    ("solve ciphers", solve_cipher("Hello there", alpha.k_1_alphabet(1))),
    ("generate ciphers", generate_cipher)
    )

if __name__ == "__main__":
    __main__()