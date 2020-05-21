# Main class Calculator
import re  # Regex for the string parser
import numpy  # Numpy for our mathematical functions and operations
from function_and_operator import *  # Module import
from containers import *  # Module import

# Main class for this project
class Calculator():
    def __init__(self):
        # Contains a reference to all functions
        self.functions = {'EXP': Function(numpy.exp),
                          'LOG': Function(numpy.log),
                          'SIN': Function(numpy.sin),
                          'COS': Function(numpy.cos),
                          'SQRT': Function(numpy.sqrt)}
        # Contains a reference to all operators
        self.operators = {'PLUSS': Operator(numpy.add, 0),
                          'GANGE': Operator(numpy.multiply, 1),
                          'DELE': Operator(numpy.divide, 1),
                          'MINUS': Operator(numpy.subtract, 0)}

        self.output_queue = Queue()  # Queue for outgoing calculations

        self.storage = Stack()  # Stack for temporary storage during calculations

    # Does calculations on a queue sorted in Reverse Polish Notation
    def rpn_calculation(self):
        while not self.output_queue.is_empty():
            element = self.output_queue.peek()

            if isinstance(element, int) or isinstance(element, float):
                self.storage.push(self.output_queue.pop())

            elif isinstance(element, Function):  # Executes function on elements in storage
                function = self.output_queue.pop()
                value = function.execute(self.storage.pop())
                self.storage.push(value)

            elif isinstance(element, Operator):  # Executes operator on elements in storage
                value1 = self.storage.pop()
                value2 = self.storage.pop()
                operator = self.output_queue.pop()
                calcedvalue = operator.execute(value2, value1)
                self.storage.push(calcedvalue)

        return self.storage.pop()  # Last element left is our final calculated value

    # Algorithm for sorting elements into RPN
    def shunting_yard(self, input_queue):
        self.input_queue = input_queue
        operator_stack = Stack()

        while not self.input_queue.is_empty():
            element = self.input_queue.peek()

            if isinstance(element, int) or isinstance(element, float):
                self.input_queue.pop()
                self.output_queue.push(element)

            elif isinstance(element, Function):
                self.input_queue.pop()
                operator_stack.push(element)

            elif element == "(":
                self.input_queue.pop()
                operator_stack.push(element)

            elif element == ")":  # Pushed on output_queue until it finds a start parenthesis
                while operator_stack.peek() != "(":
                    value = operator_stack.pop()
                    self.output_queue.push(value)
                operator_stack.pop()  # Throws away both parentheses
                self.input_queue.pop()

            elif isinstance(element, Operator):
                if not operator_stack.is_empty():
                    peek = operator_stack.peek()
                    # Needs to check if the next element is a function or operator with a lower strength
                    while isinstance(peek, Function) or (isinstance(peek, Operator) and peek.get_strength() >= element.get_strength()):
                        self.output_queue.push(operator_stack.pop())
                        if operator_stack.is_empty():
                            break
                        peek = operator_stack.peek()
                operator_stack.push(element)
                self.input_queue.pop()

        # When input_queue is empty, this will simply move the last elements on operator_stack
        while not operator_stack.is_empty():
            tempval = operator_stack.pop()
            self.output_queue.push(tempval)

    # Parses the input string to a queue suitable for shunting_yard
    def text_parse(self, text):
        text = text.replace(" ", "").upper()
        new_input_queue = Queue()

        # These variables defines searches for the three types of elements
        function_search = "|".join(["^" + func for func in self.functions.keys()])
        operator_search = "|".join(["^" + op for op in self.operators.keys()])
        number_search = "^[-0123456789.]+"

        while len(text) > 0:
            if text[0] == "(" or text[0] == ")":
                # Parentheses can simply be pushed as strings
                new_input_queue.push(text[0])
                text = text[1:]

            else:
                if re.search(function_search, text) != None:
                    # Functions needs to be looked up in the function dict
                    check = re.search(function_search, text)
                    match = self.functions[check.group(0)]
                    new_input_queue.push(match)

                elif re.search(operator_search, text) != None:
                    # Operators needs to be looked up in the operators dict
                    check = re.search(operator_search, text)
                    match = self.operators[check.group(0)]
                    new_input_queue.push(match)

                elif re.search(number_search, text) != None:
                    # All numbers are pushed as float
                    check = re.search(number_search, text)
                    match = float(check.group(0))
                    new_input_queue.push(match)

                else:  # If element in text doesnt fit any of the above, return
                       # No in-depth error/exception handling is needed in this project
                    print("Unknown element in text")
                    return

                #Text is set to the part that didnt match
                text = text[check.end(0):]

        # Returns the built queue
        return new_input_queue

    # Combines all methods to run a calculation based on the input string
    def calculate_expression(self, text):
        print("----- Operations in order: -----")
        input_queue = self.text_parse(text)
        self.shunting_yard(input_queue)
        calculation = self.rpn_calculation()
        print("----- Calculation: -----")
        print(calculation)
        return calculation



# Tests used during project development
""""
# ----- Testing Calculator Basics -----
calc = Calculator()
print(calc.functions['EXP'].execute(
calc.operators['PLUSS'].execute(
1, calc.operators['GANGE'].execute(2, 3))))


# ----- Testing RPN -----
print("Test av RPN:")
calc.output_queue.push(1)
calc.output_queue.push(2)
calc.output_queue.push(3)
calc.output_queue.push(calc.operators['GANGE'])
calc.output_queue.push(calc.operators['PLUSS'])
calc.output_queue.push(calc.functions['EXP'])
print(calc.rpn_calculation())


# ----- Testing shunting_yard -----
print("Test av Shunting yard:")
calctest = Calculator()
iq = Queue()
iq.push(calctest.functions['EXP'])
iq.push("(")
iq.push(1)
iq.push(calctest.operators['PLUSS'])
iq.push(2)
iq.push(calctest.operators['GANGE'])
iq.push(3)
iq.push(")")
calctest.shunting_yard(iq)
print(calctest.rpn_calculation())


# ----- Testing text_parser ----
calcparsetest = Calculator()
print(calcparsetest.text_parse("exp(1pluss2gange3)")._items)
"""

# ----- Testing Calculator -----
calculator = Calculator()
calculator.calculate_expression("EXP((1 pluss 5 gange 4) minus 2)")
calculator.calculate_expression("EXP(1 pluss 2 gange 3)")
calculator.calculate_expression("((15 DELE (7 MINUS (1 PLUSS 1))) GANGE 3) MINUS (2 PLUSS (1 PLUSS 1))")
while True:
    calculator.calculate_expression(input("Hva vil du kalkulere? "))
