'''
Python 3

Write code that takes some Lisp code and returns an abstract syntax tree. 
The AST should represent the structure of the code and the meaning of each token. 
For example, if your code is given "(first (list 1 (+ 2 3) 9))" 
it could return a nested array like ["first", ["list", 1, ["+", 2, 3], 9]].

TODO: evaluate AST

'''

class Parser:
    '''
    parser class is able to parse a snippet of Lisp code in order to turn it into an abstract syntax tree
    '''
    def __init__(self, code):
        self.code = code
        self.AST = AbstractSyntaxTree()

    def buildAbstractSyntaxTree(self):
        '''
        calls parse method and returns an updated abstract syntax tree
        '''
        self.AST.root = self.parse(self.code)

        return self.AST

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
        if code.replace(' ', '') == code:
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
                    expressionNode = ExpressionNode(token)
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







class AbstractSyntaxTree:
    '''
    creates an empty tree
    can add an expression node to build tree
    '''

    def __init__(self):
        self.root = []
    

    def evaluate_tree(self):
        '''
        TODO
        evaluates tree to return a singular value
        '''
        

        # i think if we evaluate the root then we successfully evaluate entire tree
        return self.root.evaluate_node()



    def __str__(self):
        return str(self.root)


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

class ExpressionNode(Node):
    '''
    an expression node has a token which states which operatation to perform
    and a list of children which the operation will be performed on
    '''

    def __init__(self, token):
        super()
        self.token = token
        self.children = []


    def evaluate_node(self):
        '''
        TODO
        evaluates single node and returns a single value (or eventually, object)
        '''


        # evaluate children
        evaluated_children = []

        # loop over children and call their evaluate node method
        for child in self.children:
            evaluated_children.append(child.evaluate_node())



        # check if token is an operator and if so, perform operation on children
        # otherwise return -1 for now until we are able to extend method
        if self.token in ['+', '-', '*', '/']:

            if self.token == '+':
                return sum(evaluated_children)

            elif self.token == '-':
                return evaluated_children[0] - evaluated_children[1]

            elif self.token == '*':
                return evaluated_children[0] * evaluated_children[1]

            elif self.token == '/':
                return evaluated_children[0] / evaluated_children[1]
                # TODO: handle error if trying to divide by 0



        elif self.token == 'list':

            return evaluated_children

        elif self.token in ['first', 'last']:
            # we can only call first or last on a list obj so we know a list will be nested inside evaluated children

            if self.token == 'first':
                return evaluated_children[0][0]

            elif self.token == 'last':
                return evaluated_children[0][-1]



        return -1



    def __str__(self):
        '''
        builds a string representation of class object
        '''
        out = '["' + self.token + '"'

        for child in self.children:
            out += ', ' + str(child)

        out += ']'

        return out


class LiteralNode(Node):
    '''
    literal node contains single instance of data
    '''

    def __init__(self, data):
        super()
        self.data = data

    def evaluate_node(self):
        '''
        TODO
        literal nodes don't really need to be 'evaluated' so I think we can just return data
        '''
        return self.data

    def __str__(self):
        '''
        returns string representation of data
        '''
        return str(self.data)
 






if __name__ == "__main__":

    parser = Parser('(first (list (+ (last (list 1 2)) 3) 1 9))')

    ast = parser.buildAbstractSyntaxTree()

    evaluated_tree = ast.evaluate_tree()

    print(evaluated_tree)





    



