# Import a random number generator from the standard python random module
from random import randint
# Import the tuple type hint from the standard python typing module
from typing import Tuple
# Import a list of the lowercase ascii letters from the standard python string module
from string import ascii_lowercase

# Import other python files
import aristocrat as aristo
import alphabet as alpha
from quotes import quotes
from alphabet import Alphabet

def get_menu_input(initial_text: str, prompt: str, can_exit: bool=False, *functions: Tuple, **function_dict) -> bool:
    """ Asks the user a question and performs a function depending on the answer.
    
    Returns True if a function was run, otherwise returns False

    *functions should be tuples of (str, function)

    **function_dict should be kwargs of function_name=function
    """
    # Add functions to function dictionary
    for item in functions:
        name, function = item
        function_dict[name] = function

    options = "\nOptions: \n" + ", ".join([option for option in function_dict]) + "\n"
    
    function_output = False

    print(initial_text)

    # Loop if a function has not been executed
    while not function_output:
        # Print the question and get the lowercase form of the answer
        user_input: str = input(prompt + "Type 'help' for more help. " + 
            ("Type 'exit' to exit. " if can_exit else "")).lower()

        # Exit from the loop and return False, as a function was not executed
        if user_input == "exit" and can_exit:
            break
        elif user_input == "help":
            print(options)
            continue
        # Check the keyword arguments to see if the input is assigned to a function
        elif user_input in function_dict:
            # Run the corresponding function
            return function_dict[user_input]()
        
        print("\nInvalid input!\n")
    
    return function_output

def choose_alphabet():
    """ Prompt user to select an alphabet generator, and returns it as a function
    """
    return get_menu_input("", "Choose an encryption alphabet type. ", 
        False,
        ("k1", lambda : alpha.k_1_alphabet),
        ("k2", lambda : alpha.k_2_alphabet),
        ("k3", lambda : alpha.k_3_alphabet),
        ("k4", lambda : alpha.k_4_alphabet)
    )

def generate_random_cipher() -> None:
    """ Generate a random cipher and have the user solve it.
    """
    # Have the user choose the alphabet generator to use and then run it to get the alphabet.
    alphabet = choose_alphabet()()

    # Get a random quote from the list of quotes
    quote = quotes[randint(0, len(quotes)-1)]

    # Lambda (anonymous) function to solve the cipher using patristocrat formatting (all capitalized)
    patristocrat = lambda : solve_cipher(quote=quote, alphabet=alphabet, use_patristo=True)
    # Lambda (anonymous) function to solve the cipher with aristocrat formatting (no caps)
    aristocrat = lambda : solve_cipher(quote=quote, alphabet=alphabet)

    # Run the corresponding solve cipher based on whether or not the user wants to format it as a patristocrat
    get_menu_input("Would you like your cipher to be formatted as a patristocrat (all caps with letters in group of 5)? ", 
        "Please enter True or False.", 
        False,
        ("true", patristocrat),
        ("false", aristocrat)
    )

def generate_user_cipher() -> None:
    """ Generate a user-created cipher with the alphabet generator provided.
    """
    alphabet = choose_alphabet()()

    quote = input("Please enter a quote to encrypt. ")

    patristocrat = lambda : solve_cipher(quote=quote, alphabet=alphabet, use_patristo=True)
    aristocrat = lambda : solve_cipher(quote=quote, alphabet=alphabet)

    get_menu_input("Would you like to print your cipher or solve it? ",
        "",
        False,
        ("print cipher", lambda : print(aristo.encrypt(quote, alphabet))),
        ("solve cipher", lambda : 
            get_menu_input("Would you like your cipher to be formatted as a patristocrat?", 
            "Please enter True or False.", 
            False,
            ("true", patristocrat),
            ("false", aristocrat)
            )
        )
    )

    # Return to main menu
    __main__(True)

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
        user_decryption = aristo.encrypt(encrypted_cipher, user_alphabet)

        # Print question text
        print("Original Cipher:\n" + 
            encrypted_cipher + 
            "\nYour decryption:\n" + 
            (aristo.patristocrat(user_decryption) if use_patristo else user_decryption) + "\n\n" + 
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
    
    __main__(True)

def __main__(returning: bool=False):
    # Print banner if launching the program, otherwise print returning to main menu
    if not returning: 
        print("-"*80 + "\n" + " "*33 + "Cipher toolkit\n" + "-"*80)
    else:
        print("\n\nReturning to the main menu...\n\n")
    
    exit_status = get_menu_input("Welcome to cipher toolkit! ", 
        "Please enter a command.", 
        True,
        ("generate cipher" , generate_user_cipher),
        ("solve cipher" , generate_random_cipher),
    )
    
    if exit_status == False:
        exit(0)

if __name__ == "__main__":
    __main__()