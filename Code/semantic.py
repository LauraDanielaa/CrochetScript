"""This module represents the behavior of a semantic analyzer.

Authors:Daniela Cubillos
        Laura Daniela Munoz Ipus
"""

class SemanticAnalyzer:
    """
    Represents a semantic analyzer that processes tokens to extract figure definitions.
    
    It parses the token list to produce a list of figure tuples in the form:
        (figure, size, color)
    """

    def __init__(self, tokens_input: list):
        """
        Initializes the SemanticAnalyzer with a list of tokens.
        
        Args:
            tokens_input (list): The list of tokens generated by the lexical analyzer.
        """

        self.tokens = tokens_input
        self.figures = []

    def analyze(self):
        """
        Analyzes the tokens and returns a list of figures as (figure, size, color) tuples.

        Expected input format:
            START
            addCircle(3, ROJO)
            addTriangle(1, ROSADO) ...
            END
        """

        # Iterate through tokens
        token_count = len(self.tokens)
        i = 0

        while i < token_count:
            token = self.tokens[i]
            if token.type_ == "FIGURE":
                # Append the figure with None placeholders for size and color.
                self.figures.append((token.value, None, None))
                i += 1
            elif token.type_ == "SIZE":
                # Associate SIZE to the most recent figure if not already set.
                if self.figures and self.figures[-1][1] is None:
                    self.figures[-1] = (self.figures[-1][0], token.value, None)
                i += 1
            elif token.type_ == "COLOR":
                # Associate COLOR to the most recent figure if not already set.
                if self.figures and self.figures[-1][2] is None:
                    self.figures[-1] = (self.figures[-1][0], self.figures[-1][1] ,token.value)
                i += 1
            else:
                # Skip tokens that are not FIGURE, SIZE, or COLOR.
                i += 1

        return self.figures