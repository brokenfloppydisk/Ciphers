class alphabet():
    # Generate the default alphabet from A to Z using list comprehension
    default_alphabet = [chr(i) for i in range(97, 123)]

    def __init__(self, alphabets: "tuple[list[str], list[str]]"):
        """
        Create a new alphabet.
        """
        # Use tuple unpacking to get plaintext and ciphertext
        plaintext, ciphertext = alphabets

        # Initialize Plaintext and Ciphertext Alphabets
        self.pta = [char.lower() for char in plaintext]
        self.cta = [char.lower() for char in ciphertext]

        # Create the conversion dictionaries
        self.construct_dictionaries()

    def construct_dictionaries(self) -> None:
        """
        Creates the conversion dictionaries from ciphertext to plaintext
        and vice versa using the plaintext and ciphertext alphabets.
        """
        self.ct_to_pt = { self.cta[i] : self.pta[i] for i in range(len(self.pta)) }
        self.pt_to_ct = { self.pta[i] : self.cta[i] for i in range(len(self.pta)) }

    def order_alphabet(self, plaintext=True) -> None:
        """
        Re-orders the alphabets so that the ciphertext or plaintext
        is in alphabetical order.
        """
        if (plaintext):
            self.cta = [self.pt_to_ct[char] for char in self.default_alphabet]
            self.pta = self.default_alphabet
        else:
            self.pta = [self.ct_to_pt[char] for char in self.default_alphabet]
            self.cta = self.default_alphabet


