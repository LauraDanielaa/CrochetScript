"""This module represents the behavior of a lexical analyzer.

Authors: Daniela Cubillos <ldcubillose@udistrital.edu.co>
"""

import re

class Token:
    """
    Represents a token with its type and associated value (lexeme).

    Attributes:
        type_ (str): The type of token (e.g., FIGURE, COLOR, KEYWORDS, SIZE, SPECIALCHAR).
        value (str): The lexeme extracted from the input code.
    """

    def __init__(self, type_: str, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type_}, {self.value})"


class LexicalAnalyzer:
    """
    Represents the behavior of a lexical analyzer that tokenizes the input code.

    Methods:
        lex(code): Tokenizes the provided code string and returns a list of tokens.
    """

    @staticmethod
    def lex(code):
        """
        Receives a code string and returns a list of tokens.

        Args:
            code (str): The input code string to tokenize.

        Returns:
            list: A list of Token instances representing the tokenized input.
        """

        tokens = []

        # Define token specifications as tuples of (TOKEN_TYPE, REGEX_PATTERN)
        token_specification = [
            ("FIGURE", r"addCircle|addSquare|addTriangle|addHeart"),    # Figure commands
            ("COLOR", r"RED|PINK|BLUE|BLACK"),                          # Figure colors
            ("KEYWORDS", r"START|END"),                                 # Start and end keywords
            ("SIZE", r"[1-5]"),                                         # Figure size (digits 1-5)
            ("SPECIALCHAR", r"\(|\)"),                                  # Parentheses: ( and )
            ("SKIP", r"[ \t]+"),                                        # Skip spaces and tabs
            ("MISMATCH", r"."),                                         # Any other character (error)
        ]

        # Combine all token patterns into a single regex using named groups
        tok_regex = "|".join(
            f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification
        )

        # Iterate over all matches in the input code
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup # Get the name of the matched group (token type)
            value = mo.group()  # Get the actual substring that matched

            # If an unexpected character is encountered, raise an error.
            if kind == "MISMATCH":
                raise RuntimeError(f"{value} unexpected")
            
            # Skip over spaces and tabs.
            if kind == "SKIP":
                continue
            
            # Create a new Token and add it to the tokens list.
            tokens.append(Token(kind, value))

        return tokens