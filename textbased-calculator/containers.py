# Module for the container classes


# Container acts as a superclass for Queue and Stack
class Container():
    def __init__(self):
        self._items = []  # Core of the classes

    def size(self):
        return len(self._items)

    def is_empty(self):  # Used in various checks
        if len(self._items) == 0:
            return True
        return False

    def push(self, item):
        self._items.append(item)  # End of list for both subclasses

    def pop(self):
        # Defined in subclass
        raise NotImplementedError

    def peek(self):
        # Defined in subclass
        raise NotImplementedError



class Queue(Container):
    def __init__(self):
        super(Queue, self).__init__()  # Supers constructor

    def peek(self):
        assert not self.is_empty()  # First element
        return self._items[0]

    def pop(self):
        assert not self.is_empty()  # First in - first out
        return self._items.pop(0)



class Stack(Container):
    def __init__(self):   # Supers constructor
        super(Stack, self).__init__()

    def peek(self):
        assert not self.is_empty()   # Last element
        return self._items[len(self._items)-1]

    def pop(self):
        assert not self.is_empty()
        return self._items.pop()   # Last in - first out



"""
# ----- Testing Queue and Stack -----
def unit_test():
    Q1 = Queue()
    Q1.push(6)
    Q1.push(12)
    Q1.push(127)
    while not Q1.is_empty():
        x = Q1.pop()
        print(x, "removed,", Q1.size(), "elements left in the queue")
    print("-------------------")
    S1 = Stack()
    S1.push(1000)
    S1.push(34)
    S1.push(7)
    while not S1.is_empty():
        x = S1.pop()
        print(x, "removed,", S1.size(), "elements left in the stack")

unit_test()
"""
