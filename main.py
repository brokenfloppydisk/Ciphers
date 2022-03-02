# Import modules (other files of code)
import aristocrat as aristo
import alphabet as alpha
from string import ascii_lowercase
from alphabet import Alphabet

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
    
    # Create a new Alphabet where each letter maps to itself
    user_alphabet = Alphabet({ ascii_lowercase[i] : ascii_lowercase[i] for i in range(26) })

    while not solved:
        print("Original Cipher:\n" + encrypted_cipher + 
            "\nYour decryption:\n" + aristo.encrypt(encrypted_cipher, user_alphabet) + "\n\n" + 
            "Your key:\n" +
            "Ciphertext (encrypted) letters: \n" + 
            " ".join(list(ascii_lowercase)) + "\n" + 
            "Plaintext (actual) letters: \n" + 
            " ".join([user_alphabet[letter] for letter in ascii_lowercase]) + "\n"
        )

        if (show_distribution):
            aristo.print_distribution_table(encrypted_cipher)
        
        print("Enter letters to switch below: (for example, ab to decrypt a to b in your key)\n"
            + "Enter '.' to toggle the letter distribution.\n"
            + "Enter 'reset' to reset your letter mappings.\n"
            + "Enter 'exit' to exit."
            )
        
        user_input: str = input("Input: ").lower()

        # Parse user input
        if user_input.lower() == "exit":
            break
        elif user_input == ".":
            show_distribution = not show_distribution
        elif user_input == "reset":
            user_alphabet = Alphabet({ ascii_lowercase[i] : ascii_lowercase[i] for i in range(26) })
        elif len(user_input) == 2:
            if any(letter in user_input for letter in ascii_lowercase):
                user_alphabet[user_input[0]] = user_input[1]
        else:
            print("-" * 80)
            print("\n\nInvalid input!\n\n")
            continue
        
        print("-" * 80)

        distributions = aristo.distributions(encrypted_cipher)
        
        # Check if user has solved the cipher
        solved = True
        for letter in user_alphabet:
            if distributions[letter] == 0:
                continue
            if user_alphabet[letter] != decryption_key[letter]:
                solved = False
    
    if solved:
        print("Cipher decrypted!")
    else:
        print("Try again next time...")

solve_cipher("Hello there", alpha.k_1_alphabet(1))