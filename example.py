"""This module demonstrates an example of how to use the Compiler.

Authors: Daniela Cubillos <ldcubillose@udistrital.edu.co>
"""
from compiler import Compiler


# =========== Example usage ========== #
def example1(compiler_: Compiler):
    """
    Demonstrates the compiler usage with a simple crochet pattern.
    
    Args:
        compiler_ (Compiler): An instance of the Compiler class.
    """

    input_text = """
    START
    addSquare(1 BLACK)
    addSquare(2 BLUE)
    addSquare(3 BLACK)
    addSquare(4 BLUE)
    addSquare(5 BLACK)
    END
    """
    
    compiler_.compile(input_text)


def example2(compiler_: Compiler):
    """
    Demonstrates the compiler usage with a simple crochet pattern.
    
    Args:
        compiler_ (Compiler): An instance of the Compiler class.
    """

    input_text = """
    START
    addCircle(5 BLACK)
    addHeart(5 BLUE)
    addTriangle(5 PINK)
    addSquare(5 RED)
    END
    """
    
    compiler_.compile(input_text)


if __name__ == "__main__":
    # Create an instance of the Compiler and run example2
    compiler = Compiler()
    example2(compiler)