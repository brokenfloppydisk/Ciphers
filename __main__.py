from random import randint
from typing import Tuple
from string import ascii_lowercase
from time import sleep
from math import floor

import aristocrat as aristo
import alphabet as alpha
import quotes
from alphabet import Alphabet

def section_header(banner_text: str) -> None:
    """ Print a section header:
    """
    # Calculate the whitespace before the word to center it
    whitespace_length = floor((80 - len(banner_text)) / 2)
    # Print a row of dashes, the word, and a row of dashes
    print(
        "-" * 80 + "\n" + 
        " " * whitespace_length + banner_text + "\n" + 
        "-" * 80
    )

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

    # Create string for list of options
    options = "\nOptions: \n" + ", ".join([option for option in function_dict]) + "\n"
    
    # Set function output to false by default to return if function fails to run
    function_output = False

    # Only print initial text if it has something in it
    if initial_text != "":
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

def choose_alphabet(prompt="Choose an encryption alphabet type. "):
    """ Prompt user to select an alphabet generator, and returns it as a function
    """
    # User has to type k1, k2, k3, or k4
    return get_menu_input("", prompt, 
        False,
        ("k1", lambda : alpha.k_1_alphabet),
        ("k2", lambda : alpha.k_2_alphabet),
        ("k3", lambda : alpha.k_3_alphabet),
        ("k4", lambda : alpha.k_4_alphabet)
    )

def choose_patristo() -> bool:
    """ Get if the user wants to format the cipher as an aristocrat (original spaces are preserved)
    or patristocrat cipher (spaces are removed, and letters are shown in capitalized groups of 5)
    and return the result.
    """
    return get_menu_input(
        "Would you like your cipher to be formatted as a patristocrat?", 
        "Please enter True or False. ", 
        False,
        ("true", lambda : True),
        ("false", lambda : False)
    )

def practice_cipher() -> None:
    """ Generate a random cipher and have the user solve it.
    """
    # Prompt the user to choose an alphabet, and save the output of 
    # the corresponding alphabet generator to alphabet.
    alphabet = choose_alphabet()()

    # Get if the user wants to format the cipher as an aristocrat (original spaces are preserved)
    # or patristocrat cipher (spaces are removed, and letters are shown in capitalized groups of 5)
    use_patristo = choose_patristo()

    # Get a random quote from the list of quotes
    quote = quotes.get_quote()

    # Pass the quote to solve_cipher to display the encrypted quote to the user
    # and have the user attempt to reconstruct the original quote
    solve_cipher(quote=quote, alphabet=alphabet, use_patristo=use_patristo)

def generate_user_cipher() -> None:
    """ Generate a user-created cipher with the alphabet generator provided.
    """
    # Have the user choose the alphabet type
    alphabet = choose_alphabet()()

    # Have the user enter the quote to encrypt
    quote = input("Please enter a quote to encrypt. ")

    # Encrypt the cipher
    encrypted_cipher = aristo.encrypt(quote, alphabet)

    # Get if the user wants to format the cipher as an aristocrat (original spaces are preserved)
    # or patristocrat cipher (spaces are removed, and letters are shown in capitalized groups of 5)
    use_patristo = choose_patristo()

    # Format the cipher as a patristocrat if needed
    if choose_patristo():
        encrypted_cipher = aristo.patristocrat(encrypted_cipher)
    
    # Ask if the user wants to print or practice solving the cipher
    get_menu_input("Would you like to print your cipher or practice solving it? ",
        "",
        False,
        ("print cipher", lambda : 
            print("The encrypted cipher is: " + encrypted_cipher)
        ),
        ("solve cipher", lambda : 
            solve_cipher(quote, alphabet, use_patristo)
        )
    )
    
    # Wait for half a second after printing the cipher
    sleep(0.5)
    
    # Return to main menu
    main_menu(returning=True)

def solve_unknown_cipher() -> None:
    """ Have the user attempt to solve a cipher that they input
    """
    encrypted_text = input("Please enter the encrypted cipher to solve. ")

    # Display and have the user solve the cipher
    solve_cipher(quote=encrypted_text, alphabet=None)

def solve_cipher(quote: str, alphabet: Alphabet=None, use_patristo:bool=False) -> None:
    """ Prompt the user to solve a cipher by typing in letters to swap.
    """
    alphabet_known = True

    # Set alphabet known to false if the alphabet is not provided.
    if alphabet == None:
        alphabet_known = False
    else:
        decryption_key = aristo.flip(alphabet)

        solved = False

    # Don't show the letter distribution by default
    show_distribution = False

    # Encrypt the quote as a cipher using the provided alphabet.
    # If the alphabet is not known, show the quote directly.
    if alphabet_known:
        encrypted_cipher = aristo.encrypt(quote, alphabet)
    else:
        encrypted_cipher = quote
    if use_patristo:
        encrypted_cipher = aristo.patristocrat(encrypted_cipher)
    
    # Create a default Alphabet where each letter maps to itself
    # Equivalent to a k1 alphabet with a shift of 0
    user_alphabet = alpha.k_1_alphabet(0)

    # Loop until the cipher is solved (or the user exits)
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
            + "Enter 'exit' or 'done' to exit."
            )
        
        # Get user input
        user_input: str = input("Input: ").lower()

        # Do different things based on user input

        # Exit if user input is 'exit'
        if user_input.lower() == "exit" or user_input.lower() == "done":
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

        if alphabet_known:    
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
    
    main_menu(returning=True)

def decrypt_known_cipher() -> None:
    """ Decrypt and print a cipher that the user enters, using a user-provided key.
    """
    encrypted_cipher = input("Please enter the encrypted monoalphabetic cipher. ")
    alphabet = choose_alphabet("What type of alphabet does the cipher use for its key? ")()
    
    decrypted_cipher = aristo.decrypt(encrypted_cipher, alphabet)
    
    print("Using this key, the decrypted cipher is: "
        + decrypted_cipher
    )

    # Return to the main menu
    main_menu(returning=True)

def main_menu(returning: bool=False) -> None:
    # Print banner if launching the program, otherwise print returning to main menu
    if not returning: 
        section_header("Cipher toolkit")
    else:
        section_header("Returning to the main menu...")
        sleep(0.5)
    
    # Get user input and either go to cipher generation or solving.
    exit_status = get_menu_input("Welcome to cipher toolkit! This program allows you to " +
        "generate monoalphabetic ciphers, \npractice solving a cipher, " +
        "attempt to solve a cipher, and decrypt a cipher with the key.\n" +
        "made to practice codebusters for Science Olympiad.", 
        "Please enter a command. ", 
        False,
        ("generate cipher" , generate_user_cipher),
        ("practice cipher" , practice_cipher),
        ("solve unknown cipher", solve_unknown_cipher),
        ("decrypt known cipher", decrypt_known_cipher),
        ("exit", lambda : section_header("Exiting program..."))
    )
    
    # Exit the program if the user typed exit
    if exit_status == False:
        exit(0)

def __main__():
    main_menu()

if __name__ == "__main__":
    __main__()