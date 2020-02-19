'''

python3

takes in a mathematical expression in string form and takes the derivative

to begin, we will assume mathematical expression
1. is valid
2. contains only integers, +, *, ^, and the letter x

'''

class Differentiator:

    def __init__(self):
        pass



class Node:
    def __init__(self, data = None):
        self.data = data
        self.parent = None
        self.lchild = None
        self.rchild = None

    # return a string representation of a link
    def __str__(self):
        s = str(self.data)
        return s



class ExpressionTree:
    def __init__(self):
        self.root = None




if __name__ == "__main__":
    pass