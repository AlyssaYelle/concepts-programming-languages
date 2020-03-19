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
        each child of the expression node calls their own respective evaluate_node fn
        returns a list of evaluated child nodes
        '''

        evaluated_children = []

        for child in self.children:
            evaluated_children.append(child.evaluate_node())

        return evaluated_children


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

        evaluated_children = self.evaluate_children()

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


class ListNode(ExpressionNode):
    '''
    ListNode contains the data to create a list object
    token is list
    '''

    def evaluate_node(self):

        evaluated_children = self.evaluate_children()

        return evaluated_children


class IdxNode(ExpressionNode):
    '''
    returns element at specific position in a list
    will accept args "first", "last", or a numeric index

    TODO: handle index out of bound errors
    '''

    def evaluate_node(self):

        evaluated_children = self.evaluate_children()

        if self.token.isnumeric():
            return evaluated_children[0][int(self.token)]
        else:
            if self.token == 'first':
                print('we are here at first', evaluated_children)
                return evaluated_children[0][0]
            elif self.token == 'last':
                return evaluated_children[0][-1]


class AbstractSyntaxTree:
    '''
    creates an empty tree
    can add an expression node to build tree
    '''

    def __init__(self, root = []):
        self.root = root
    

    def evaluate_tree(self):
        '''
        TODO
        evaluates tree to return a singular value
        '''
        

        # i think if we evaluate the root then we successfully evaluate entire tree
        return self.root.evaluate_node()



    def __str__(self):
        return str(self.root)


class Parser:
    '''
    parser class is able to parse a snippet of Lisp code in order to turn it into an abstract syntax tree
    '''
    def __init__(self):
        pass

    def buildAbstractSyntaxTree(self, code):
        '''
        calls parse method and returns an updated abstract syntax tree
        '''
        root = self.parse(code)

        AST = AbstractSyntaxTree(root)

        return AST

    def setExpressionNode(self, token):
        '''
        determines which type of expression node to build based on token
        '''

        if token in ['+', '-', '*', '/', '^', '%']:
            return MathOperatorNode(token)
        elif token == 'list':
            return ListNode(token)
        elif (token in ['first', 'last']) or token.isnumeric():
            print('setting an index node')
            return IdxNode(token)

    def parse(self, code):
        '''
        recursively parses Lisp code
        based on knowledge that each layer starts with an operator/token and is then followed by children
        which can be literals (like an int or str) or another layer with token + children
        '''

        # if code is a single number, return it as a literal node
        if code.isnumeric():
            return LiteralNode(int(code)) # prob should update this to handle floats

        # handle possibility that code is a single non-token string
        if (code[0] in ['"', "'"]) and (code[-1] in ['"', "'"]):
            return LiteralNode(code[1:-1])

        # if code is wrapped in parens we want to parse what is in between
        if code[0] == '(':
            #print('stripping parentheses')
            return self.parse(code[1:-1])

        # the format must now be (operator child1 child2 ....) where each child has same format or is literal
        token = ''

        currentChild = ''
        children = []

        # set state
        # isLookingForToken is mutually exclusive from isLookingForChildren and isLookingForExpression
        isLookingForToken = True
        isLookingForChildren = False
        isLookingForExpression = False

        # in case we need to count parens to build a valid expression
        openParens = 0
        closeParens = 0

        # keep track of index
        idx = 0

        for ch in code:

            # when in state isLookingForToken we build out token by adding characters until reaching a space
            # then we create an ExpressionNode using this token and change state
            if isLookingForToken:

                if ch == ' ':
                    expressionNode = self.setExpressionNode(token)
                    isLookingForToken = False
                    isLookingForChildren = True
                else:
                    token += ch


            # when in state isLookingForChildren we build out each child by adding chars to currentChild
            # until we see a space, then append the child to children array
            # if we see an opening parenthesis we add a second state, isLookingForExpression
            # while in state isLookingForExpression we ignore spaces and count parentheses until expression is built
            # we will know expression is built when num ( matches num ), then we can parse that expression and append the parsed expression to children array
            elif isLookingForChildren:

                if isLookingForExpression:
                    if ch == '(':
                        currentChild += ch
                        openParens += 1
                    elif ch == ')':
                        closeParens += 1
                        currentChild += ch
                        if closeParens == openParens:

                            isLookingForExpression = False

                        if idx == len(code) -1:
                            children.append(self.parse(currentChild))
                            currentChild = ''

                    else:
                        currentChild += ch

                elif (ch == ' '):

                    children.append(self.parse(currentChild))
                    currentChild = ''
                elif ch == '(':
                    currentChild += ch
                    isLookingForExpression = True
                    openParens += 1
                else:
                    currentChild += ch

                    if idx == len(code) -1:

                        children.append(self.parse(currentChild))
                        currentChild = ''

            idx += 1

        # set children of out expression node and return
        expressionNode.children = children
        return expressionNode








if __name__ == '__main__':

    lisp_code = '(2 (list 1 2 3 4))'

    my_parser = Parser()

    ast = my_parser.buildAbstractSyntaxTree(lisp_code)

    print(ast)

    print(ast.evaluate_tree())









