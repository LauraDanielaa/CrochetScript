"""This module contains the Compiler class.

Authors: Daniela Cubillos <ldcubillose@udistrital.edu.co>
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas 
from reportlab.lib.colors import HexColor
from lexical import LexicalAnalyzer
from sintactic import SintacticAnalyzer
from semantic import SemanticAnalyzer


class Compiler:
    """
    This class represents the behavior of a complete compiler.
    It processes the input code through lexical, syntactic, and semantic analyses,
    generates pattern figures, and exports the final crochet pattern as a PDF.
    """

    def __init__(self):
        # A dictionary mapping color names to their hexadecimal codes.
        self.hex_colors = {
            "RED": "#f70529",
            "PINK": "#feb1f1",
            "BLUE": "#648efd",
            "BLACK": "#000000"
        }


    def compile(self, code: str):
        """
        Compiles the given code.

        1. Uses LexicalAnalyzer to extract tokens.
        2. Uses SintacticAnalyzer to ensure tokens follow the grammar.
        3. Uses SemanticAnalyzer to extract figures (with colors and sizes).
        4. Exports the generated pattern as a PDF.
        """

        # Extract tokens from the code
        tokens_ = LexicalAnalyzer.lex(code)

        # Check that the tokens follow the grammar
        sintactic_analyzer = SintacticAnalyzer(tokens_)
        sintactic_analyzer.parse()

        # Extract figures, colors and sizes from the tokens, in format (figure, size, color)
        semantic_analyzer_ = SemanticAnalyzer(tokens_)
        figures = semantic_analyzer_.analyze()
        print(figures)

        # Generate and export the crochet pattern PDF
        self.export_pattern(figures)

    def generate_figures(self, figures: list):
        """
        Generates pattern figures from the figures list.

        Each element in the 'figures' list is expected to be a tuple where:
          - fig[0] is the command (e.g., 'addCircle', 'addSquare', etc.).
          - fig[1] is the size.
          - fig[2] is the color.

        Returns:
            A list of tuples (steps, color_hex, name) representing the generated patterns.
        """

        patterns = []

        for fig in figures:
            if(fig[0] == 'addCircle'):
                patterns.append(self.generate_circle(int(fig[1]), fig[2]))
            elif(fig[0] == 'addSquare'):
                patterns.append(self.generate_square(int(fig[1]), fig[2]))
            elif(fig[0] == 'addTriangle'):
                patterns.append(self.generate_triangle(int(fig[1]), fig[2]))
            elif(fig[0] == 'addHeart'):
                patterns.append(self.generate_heart(int(fig[1]), fig[2]))

        return patterns


    def generate_circle(self, size: int, color: str):
        """
        Generates a circle pattern with the given size and color.

        The pattern consists of an initial set of steps followed by additional rounds
        based on the size. Finally, a FO (fasten off) step is appended.

        Returns:
            A tuple (circle_steps, color_hex, "CIRCLE")
        """

        # Get the hex color from the dictionary
        color = self.hex_colors.get(color)
        circle = [
        "1. 6 SC in magic ring",
        "2. 6 INC (12 SC)"
        ]

        # Add aditional steps based in size
        for i in range(size):
            total_points = 18 + (i * 6)
            step = f"{i+3}. ({i+1} SC, 1 INC) *6 ({total_points} SC)"
            circle.append(step)

        circle.append(f"{len(circle)+1}. FO")
        return circle, color, "CIRCLE"

    def generate_square(self, size: int, color: str):
        """
        Generates a square pattern with the given size and color.

        The pattern uses an initial number of chains based on the size and includes
        subsequent instructions for forming the square, ending with FO.

        Returns:
            A tuple (square_steps, color_hex, "SQUARE")
        """

        # Get the hex color from the dictionary
        color = self.hex_colors.get(color)
        initial_chains = {1: 5, 2: 7, 3: 9, 4: 11, 5: 13}

        # Get the initial number of chains from the dictionary
        chain = initial_chains.get(size)

        # Generate first square steps
        square = [
            f"1. {chain + 1} chains",
            f"2. {chain} SC (starts since first stich)"
        ]

        for _ in range(chain):
            square.append(f"{len(square)+1}. Chain 1, turn and {chain} SC.")

        # Add final step
        square.append(f"{len(square)+1}. FO")

        return square, color, "SQUARE"

    def generate_triangle(self, size: int, color: str):
        """
        Generates a triangle pattern with the given size and color.

        The pattern begins with an initial number of chains, then decreases
        the number of SCs on each row until completion, ending with FO.

        Returns:
            A tuple (triangle_steps, color_hex, "TRIANGLE")
        """

        color = self.hex_colors.get(color)
        
        # Calcular hasta qué fila necesitamos basado en el tamaño
        final_row = size * 2 + 1

        # Iniciar el patrón con las primeras dos filas que son fijas
        triangle = [
            "1. Ch 2. Sc in the 2nd loop from hook [total 1 sts]",
            "2. Ch 1, turn. 3sc in the same space [3 sts]"
        ]

        current_stitches = 3
        row = 3

        while row <= final_row:
            if row % 2 == 1:
                # Filas impares: sc en cada punto
                triangle.append(f"{row}. Ch 1, turn. Sc in each st [{current_stitches} sts]")
            else:
                # Filas pares: incrementos en los extremos
                new_stitches = current_stitches + 2
                middle_sts = current_stitches - 2
                triangle.append(f"{row}. Ch 1, turn. Inc, sc in next {middle_sts} sts, inc [{new_stitches} sts]")
                current_stitches = new_stitches
            row += 1

        # Añadir FO al final
        triangle.append(f"{len(triangle) + 1}. FO")

        return triangle, color, "TRIANGLE"

    def generate_heart(self, size: int, color: str):
        """
        Generates a heart pattern with the given size and color.

        The pattern consists of a series of rounds with SC and INC instructions,
        followed by additional steps to form the lobes of the heart, and finishes with FO.

        Returns:
            A tuple (heart_steps, color_hex, "HEART")
        """
        color = self.hex_colors.get(color)


        # constants of the pattern
        base_stitches = {1: "sc", 2: "hdc", 3: "dc", 4: "tr", 5: "tr"}
        initial_chains = {1: 1, 2: 1, 3: 2, 4: 3, 5: 2}
    
        # get values based on size
        base_stitch = base_stitches[size]
        chains = initial_chains[size]
        total_stitches = {1: 6, 2: 9, 3: 11, 4: 13, 5: [12, 22, 31]}
        stitches = total_stitches[size]
    
        # start the pattern
        pattern = ["1. Make a MC."]
        step = 2
    
        # Special pattern for size 5
        if size == 5:
            pattern.extend([
                f"{step}. Ch {chains}, {stitches[0]} dc in MC, join with a sl st.",
                f"{step+1}. hdc 1 in first st, [dc 4] in next st, [hdc 1, sc 1] in next st, sc 1, ",
                f"{step+2}. sc inc 1, hdc 2, sc inc 1, sc 1, [sc 1, hdc 1] in next st, [dc 4] in next st, ",
                f"{step+3}. hdc 1, sl st.",
                f"{step+4}. sc 2, sc inc 3, sc 5, [sc 1, hdc 1] in next st, ch 1, [hdc 1, sc 1] ",
                f"{step+5}.in next st, sc 5, sc inc 3, sc 2, sl st."
            ])
            step += 3
        else:
            # generate 1 step
            pattern.append(f"{step}. Ch {chains}")
            step += 1
    
            # get points for each size
            side_stitches = (stitches - 2) // 2 if size >= 2 else stitches // 2
    
            # first side
            pattern.append(f"{step}. {base_stitch} {side_stitches}")
            step += 1
    
            # central point for sizes 2-4
            if size >= 2:
                pattern.append(f"{step}. ch 1, {base_stitch} 1, ch 1")
                step += 1
    
            # second side
            pattern.append(f"{step}. {base_stitch} {side_stitches}")
            step += 1
    
            # close the heart
            pattern.append(f"{step}. sl st in MC.")
            step += 1
    
        # final steps
        pattern.extend([
            f"{len(pattern)+1}. Pull the MC close.",
            f"{len(pattern)+2}. FO"
        ])
    
        return pattern, color, "HEART"


    def check_page(self, c, y, margin_bottom, height, margin_top, color):
        """
        Checks if the current y-coordinate is below the bottom margin.
        If so, creates a new page, resets the y-coordinate, and sets default styles.

        Args:
            c: The canvas object.
            y: The current y-coordinate.
            margin_bottom: The bottom margin.
            height: The height of the page.
            margin_top: The top margin.
            color: The hexadecimal color code for the steps.

        Returns:
            The updated y-coordinate.
        """

        if y < margin_bottom:
            c.showPage()
            c.setFont("Helvetica", 12)
            color_obj = HexColor(color)
            c.setFillColor(color_obj)
            return height - margin_top

        return y

    def draw_title(self, c, width, height, margin_top, margin_left, margin_right, title):
        """
        Draws the title centered at the top of the first page,
        along with a decorative line below it.

        Args:
            c: The canvas object.
            width: The width of the page.
            height: The height of the page.
            margin_top: The top margin.
            margin_left: The left margin.
            margin_right: The right margin.
            title: The title string to be drawn.

        Returns:
            The y-coordinate of the title.
        """

        c.setFont("Helvetica-Bold", 24)
        title_y = height - margin_top
        c.drawCentredString(width / 2, title_y, title)

        # Draw decorative line below the title
        c.setLineWidth(1)
        c.setStrokeColor(HexColor("#000000"))
        c.line(margin_left, title_y - 10, width - margin_right, title_y - 10)
        return title_y


    def draw_terms(self, c, width, height, margin_top):
        """
        Draws a section containing crochet abbreviations below the title.

        Args:
            c: The canvas object.
            width: The width of the page.
            height: The height of the page.
            margin_top: The top margin.
        """
        terms = [
            "Ch – Chain",
            "Sc - Single crochet",
            "Dc – Double Crochet",
            "HDc - Half double crochet",
            "Tr – Treble Crochet",
            "MC – Magic Circle",
            "Sl St – Slip Stitch",
            "St – Stitch"
        ]

        y = height - margin_top - 40

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "US TERMS")
        y -= 25
        
        c.setFont("Helvetica", 12)
        for term in terms:
            c.drawString(50, y, term)
            y -= 20
        return y

    
    def draw_pattern(self, c, steps, color, name, y, margin_bottom, height, margin_top):
        """
        Draws a single pattern, including its name and steps.
        Checks for page breaks when necessary.

        Args:
            c: The canvas object.
            steps: A list of strings representing the pattern steps.
            color: The hexadecimal color code for the steps.
            name: The name of the pattern.
            y: The current y-coordinate.
            margin_bottom: The bottom margin.
            height: The height of the page.
            margin_top: The top margin.

        Returns:
            The updated y-coordinate after drawing the pattern.
        """

        # Ensure there's enough space for the pattern name
        y = self.check_page(c, y, margin_bottom, height, margin_top, color)

        # Draw the pattern name in bold black
        c.setFillColor(HexColor("#000000"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, name)
        y -= 25

        # Convert the hexadecimal color code for the steps
        color_obj = HexColor(color)
        c.setFillColor(color_obj)
        c.setFont("Helvetica", 12)

        # Draw each step on a new line
        for step in steps:
            y = self.check_page(c, y, margin_bottom, height, margin_top, color)
            c.drawString(50, y, step)
            y -= 20

        # Add extra space after the pattern
        y -= 20
        return y

    def create_pdf(self, patterns):
        """
        Creates a PDF file named "PatronCrochet.pdf" that contains a title and a series of patterns.
        Each pattern is a tuple (steps, color_hex, name). The PDF handles page breaks automatically.

        Args:
            patterns: A list of tuples representing the patterns.
        """

        c = canvas.Canvas("PatronCrochet.pdf", pagesize=letter)
        width, height = letter

        # Define margins
        margin_left = 50
        margin_right = 50
        margin_top = 50
        margin_bottom = 50

        # Draw the title on the first page
        title = "YOUR PATTERN"
        title_y = self.draw_title(c, width, height, margin_top, margin_left, margin_right, title)

        # Draw the crochet abbreviations below the title
        y = self.draw_terms(c, width, height, margin_top)

        # Set the initial y-coordinate for the content (below the terms)
        y -= 20

        # Draw each pattern
        for steps, color, name in patterns:
            y = self.draw_pattern(c, steps, color, name, y, margin_bottom, height, margin_top)

        c.save()

    def export_pattern(self, figures: list):
        """
        Generates the pattern figures based on the provided figures list and creates a PDF file.
        Prints a confirmation message upon completion.

        Args:
            figures: A list of tuples with information to generate each figure.
        """

        pattern = self.generate_figures(figures)
        self.create_pdf(pattern)
        print("the pdf with your crochet pattern has been created! :)")

