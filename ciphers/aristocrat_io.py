from string import ascii_lowercase
from cipher_io import CipherIO
from ciphers.alphabet import Alphabet
import ciphers.quotes as quotes
import ciphers.aristocrat as aristo
import ciphers.alphabet as alpha

class AristocratIO():
    @classmethod
    def choose_alphabet(cls, prompt="Choose an encryption alphabet type. "):
        """ Prompt user to select an alphabet generator, and returns it as a function
        """
        # User has to type k1, k2, k3, or k4
        return CipherIO.get_menu_input("", prompt, 
            False,
            ("k1", lambda : alpha.k_1_alphabet),
            ("k2", lambda : alpha.k_2_alphabet),
            ("k3", lambda : alpha.k_3_alphabet),
            ("k4", lambda : alpha.k_4_alphabet)
        )

    @classmethod
    def choose_patristo(cls) -> bool:
        """ Get if the user wants to format the cipher as an aristocrat (original spaces are preserved)
        or patristocrat cipher (spaces are removed, and letters are shown in capitalized groups of 5)
        and return the result.
        """
        return CipherIO.get_menu_input(
            "Would you like your cipher to be formatted as a patristocrat?", 
            "Please enter True or False. ", 
            False,
            ("true", lambda : True),
            ("false", lambda : False)
        )

    @classmethod
    def practice_cipher(cls) -> None:
        """ Generate a random cipher and have the user solve it.
        """
        # Prompt the user to choose an alphabet, and save the output of 
        # the corresponding alphabet generator to alphabet.
        alphabet = cls.choose_alphabet()()

        # Get if the user wants to format the cipher as an aristocrat (original spaces are preserved)
        # or patristocrat cipher (spaces are removed, and letters are shown in capitalized groups of 5)
        use_patristo = cls.choose_patristo()

        # Get a random quote from the list of quotes
        quote = quotes.get_quote()

        # Pass the quote to solve_cipher to display the encrypted quote to the user
        # and have the user attempt to reconstruct the original quote
        cls.solve_cipher(quote=quote, alphabet=alphabet, use_patristo=use_patristo)
    
    @classmethod
    def generate_user_cipher(cls) -> None:
        """ Generate a user-created cipher with the alphabet generator provided.
        """
        # Have the user choose the alphabet type
        alphabet = cls.choose_alphabet()()

        # Have the user enter the quote to encrypt
        quote = CipherIO.fetch_input("Please enter a quote to encrypt. ")

        # Encrypt the cipher
        encrypted_cipher = aristo.encrypt(quote, alphabet)

        # Get if the user wants to format the cipher as an aristocrat (original spaces are preserved)
        # or patristocrat cipher (spaces are removed, and letters are shown in capitalized groups of 5)
        use_patristo = cls.choose_patristo()

        # Format the cipher as a patristocrat if needed
        if use_patristo:
            encrypted_cipher = aristo.patristocrat(encrypted_cipher)
        
        # Ask if the user wants to print or practice solving the cipher
        CipherIO.get_menu_input("Would you like to print your cipher or practice solving it? ",
            "",
            False,
            ("print cipher", lambda : 
                CipherIO.print_function("The encrypted cipher is: " + encrypted_cipher)
            ),
            ("solve cipher", lambda : 
                cls.solve_cipher(quote, alphabet, use_patristo)
            )
        )
    
    @classmethod
    def solve_unknown_cipher(cls) -> None:
        """ Have the user attempt to solve a cipher that they input
        """
        encrypted_text = CipherIO.fetch_input("Please enter the encrypted cipher to solve. ")

        # Display and have the user solve the cipher
        cls.solve_cipher(quote=encrypted_text, alphabet=None)

    @classmethod
    def solve_cipher(cls, quote: str, alphabet: Alphabet=None, use_patristo:bool=False) -> None:
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
        
        # Create a default Alphabet where each letter maps to itcls
        # Equivalent to a k1 alphabet with a shift of 0
        user_alphabet = alpha.k_1_alphabet(0)

        # Loop until the cipher is solved (or the user exits)
        while not solved:
            user_decryption = aristo.encrypt(encrypted_cipher, user_alphabet)

            # Print question text
            CipherIO.print_function("Original Cipher:\n" + 
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
                CipherIO.print_function(aristo.distribution_table(encrypted_cipher))
            
            # Print user options
            CipherIO.print_function("Enter letters to switch below: (for example, ab to decrypt a to b in your key)\n"
                + "Enter '.' to toggle the letter distribution.\n"
                + "Enter 'reset' to reset your letter mappings.\n"
                + "Enter 'exit' or 'done' to exit."
                )
            
            # Get user input
            user_input: str = CipherIO.fetch_input("Input: ").lower()

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
                CipherIO.print_function(
                    "-" * 80
                    + "\n\nInvalid input!\n\n")
                continue
            
            # Print 80 of '-' to act as a section divider.
            CipherIO.print_function("-" * 80)

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
            CipherIO.print_function("Cipher decrypted!")

    @classmethod
    def decrypt_known_cipher(cls) -> None:
        """ Decrypt and print a cipher that the user enters, using a user-provided key.
        """
        encrypted_cipher = CipherIO.fetch_input("Please enter the encrypted monoalphabetic cipher. ")
        alphabet = cls.choose_alphabet("What type of alphabet does the cipher use for its key? ")()
        
        decrypted_cipher = aristo.decrypt(encrypted_cipher, alphabet)
        
        CipherIO.print_function("Using this key, the decrypted cipher is: "
            + decrypted_cipher
        )