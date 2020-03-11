class Node:
    '''
    node interface
    has contract with expression node and literal node
    '''
    def __init__(self):
        pass

    def evaluate_node(self):
        raise NotImplementedError


    # return a string representation of a link
    def __str__(self):
        raise NotImplementedError




class LiteralNode(Node):
    '''
    literal node contains single instance of data
    '''

    def __init__(self, data):
        super()
        self.data = data

    def evaluate_node(self):
        '''
        since literal nodes just contain a single piece of data we just return the data
        '''
        return self.data

    def __str__(self):
        '''
        returns string representation of data
        '''
        return str(self.data)



class ExpressionNode(Node):
    '''
    an expression node has a token which states which operatation to perform
    and a list of children which the operation will be performed on
    '''

    def __init__(self, token):
        super()
        self.token = token
        self.children = []

    def evaluate_children(self):
        '''
        each child of the expression node calls their own respection evaluate_node fn
        '''

        evaluated_children = []

        for child in self.children:
            evaluated_children.append(child.evaluate_node())


    def evaluate_node(self):
        raise NotImplementedError

    def __str__(self):
        '''
        builds a string representation of class object
        '''
        out = '["' + self.token + '"'

        for child in self.children:
            out += ', ' + str(child)

        out += ']'

        return out


class MathOperatorNode(ExpressionNode):
    '''
    this node performs math operations

    +, -, *, /, ^, %

    can only have two children which must evaluate to numbers
    '''

    # TODO
    # check validity of node
    # should be done within parser class?

    def evaluate_node(self):
        '''
        performs math op on its two children
        '''

        if self.token == '+':
            return sum(evaluated_children)

        elif self.token == '-':
            return evaluated_children[0] - evaluated_children[1]

        elif self.token == '*':
            return evaluated_children[0] * evaluated_children[1]

        elif self.token == '/':
            return evaluated_children[0] / evaluated_children[1]
            # TODO: handle error if trying to divide by 0

        elif self.token == '^':
            return evaluated_children[0] ** evaluated_children[1]

        elif self.token == '%':
            return evaluated_children[0] % evaluated_children[1]














if __name__ == '__main__':
    print('hello')