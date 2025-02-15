"""This module represents the behavior of a syntactic analyzer.

Authors:Daniela Cubillos
        Laura Daniela Munoz Ipus


GRAMMAR DEFINITION:
<S>               -> "START" < FIGURE_SEQUENCE> "END" 
<FIGURE_SEQUENCE> -> <FIGURE> “(“<SIZE><COLOR>”)” <FIGURE_SEQUENCE> | <FIGURE> “(“<SIZE><COLOR>”)” 
<FIGURE>           -> “addCircle”| “addSquare”| “addTriangle”| “addHeart” 
<SIZE>             -> "1" | "2" | "3" | "4" | "5" 
<COLOR>            -> "RED" | "PINK" | "BLUE" | "BLACK" 
"""

class SintacticAnalyzer:
    """
    Represents the behavior of a syntactic analyzer.
    
    This analyzer checks if the token sequence conforms to the expected grammar.
    It verifies that the code starts with 'START', follows with a sequence of figures,
    and ends with 'END'. Each figure must be followed by a specific structure of tokens.
    """

    def __init__(self, tokens):
        """
        Initializes the syntactic analyzer with a list of tokens.
        
        Args:
            tokens (list): A list of tokens produced by the lexical analyzer.
        """

        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        """
        Advances the current token pointer to the next token in the list.
        
        If there are no more tokens, sets current_token to None.
        """

        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        """
        Starts the parsing process following the grammar structure.
        
        The process consists of checking:
            1. The start token ("START")
            2. A valid sequence of figures
            3. The end token ("END")
        """

        self.start()
        self.figure_sequence()
        self.end()

    def start(self):
        """
        Checks if the first token is 'START'.
        
        Advances to the next token if the check is successful, otherwise
        raises a syntax error.
        """

        if (
            self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "START"
        ):
            self.advance()
        else:
            self.error("START")

    def end(self):
        """
        Checks if the current token is 'END' at the end of the sequence.
        
        Advances to the next token after 'END'. If extra tokens remain or
        if 'END' is not found, raises a syntax error.
        """

        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "END"
        ):
            self.advance()
            if self.current_token is not None:
                self.error("No extra tokens expected after END")
        else:
            self.error("END")

    def figure_sequence(self):
        """
        Processes the sequence of figure tokens.
        
        Continues to parse figures as long as the current token is of type 'FIGURE'.
        """

        while self.current_token and self.current_token.type_ == "FIGURE":
            self.figure()

    def figure(self):
        """
        Processes a single figure structure.
        
        Expected structure:
            FIGURE "(" SIZE COLOR ")"
        
        Checks each token in the sequence:
            - A FIGURE token
            - An opening special character "("
            - A SIZE token
            - A COLOR token
            - A closing special character ")"
        
        If the structure is valid, prints a formatted representation of the figure.
        Otherwise, raises a syntax error indicating the expected token.
        """
        
        if self.current_token and self.current_token.type_ == "FIGURE":
            figure_value = self.current_token.value
            self.advance()
            
            # Check for "(" following the figure.
            if self.current_token and self.current_token.type_ == "SPECIALCHAR" and self.current_token.value == "(":
                sc_value1 = self.current_token.value
                self.advance()
            else:
                self.error("( after FIGURE")

            # Check for SIZE token.
            if self.current_token and self.current_token.type_ == "SIZE":
                size_value = self.current_token.value
                self.advance()
            else:
                self.error("SIZE")

            # Check for COLOR token.
            if self.current_token and self.current_token.type_ == "COLOR":
                color_value = self.current_token.value
                self.advance()
            else:
                self.error("COLOR")

            # Check for ")" following the size and color.
            if self.current_token and self.current_token.type_ == "SPECIALCHAR"  and self.current_token.value == ")":
                sc_value2 = self.current_token.value
                print(f"Figure: {figure_value}{sc_value1}{size_value} {color_value}{sc_value2}")
                self.advance()
            else:
                self.error(")")

        else:
            self.error("FIGURE")

    def error(self, expected):
        """
        Raises a SyntaxError when the current token does not match the expected token.
        
        Args:
            expected (str): The expected token or description of the expected input.
        
        Raises:
            SyntaxError: Indicates the mismatch between the expected token and the actual token.
        """
         
        raise SyntaxError(
            f"Syntax error: expected {expected}, found {self.current_token}"
        )