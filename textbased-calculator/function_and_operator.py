# Module containing the mathematical operations needed for our calculator

import numbers  # Used to validate class input
import numpy  # Mathematical functions and operations

# Wraps our mathematical functions, and is also used to identify/validate them
class Function:
    def __init__(self, func):
        self.func = func

    def execute(self, element, debug=True):
        if not isinstance(element, numbers.Number):  # Simple check
            raise TypeError("Cannot execute func if element is not a number")
        result = self.func(element)
        if debug is True:  # Formatting of our function execution
            print("Function: " + self.func.__name__
                  + "({:f}) = {:f}".format(element, result))
        return result

# Wraps our mathematical functions, and is also used to identify/validate them
class Operator:
    def __init__(self, operation, strength):  # Sets the operators "strength" aswell
        self.operation = operation
        self.strength = strength

    def execute(self, element1, element2, debug=True):  # Note that operator takes in two elements
        if not isinstance(element1, numbers.Number) or not isinstance(element2, numbers.Number):
            raise TypeError("Cannot execute operation if an element is not a number")
        result = self.operation(element1, element2)
        if debug is True: # Formatting of our function execution
            print("Operation: " + self.operation.__name__
                  + "({:f}, {:f}) = {:f}".format(element1, element2, result))
        return result

    def get_strength(self):  # Simple get method used for comparing strengths in calculator class
        return self.strength


"""
# ----- Testing Function ----
exponential_func = Function(numpy.exp)
sin_func = Function(numpy.sin)
print(exponential_func.execute(sin_func.execute(2)))

# ----- Testing Operator -----

add_op = Operator(operation=numpy.add, strength=0)
multiply_op = Operator(operation=numpy.multiply, strength=1)
print(add_op.execute(1, multiply_op.execute(2, 3)))
"""
