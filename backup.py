"""
# Copyright Nick Cheng, Peter Chou 2016, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment.

# Add your functions here.

# Globally Define the symbols for NOT, AND, OR, Left_parenthese, 
# Right_parenthese, and variables allowed
AND = '*'
OR = '+'
NOT = '-'
left_p = '('
right_p = ')'
VARIABLES = 'abcdefghijklmnopqrstuvwxyz'
# define the numerical representation of True and False
TRUTH = '1'
FALSE = '0'
# define alphabet representation of each player
PLAYER0 = 'A'
PLAYER1 = 'E'
# define the how much a child is specified to be indented in draw formula tree
# which is 2 spaces
INDENT = '  '

def not_handler(formula):
    ''' (str) -> (FormulaTree)
    REQ: fomula[0] == '-'
    Returns the FormulaTree where NOT is the root of the tree returns None iff 
    the NOT formula is invalid
    >>> tree = not_handler('-(x+y)')
    >>> compare = NotTree(OrTree(Leaf('x'),Leaf('y')))
    >>> tree.__eq__(compare)
    True
    >>> tree = not_handler('-+x')
    None
    '''
    # A formula with a Not in front has 4 cases
    # case 1 after the NOT there is a variable
    if formula[1] in VARIABLES:
        # then return the NotTree + the Leaf
        tree = NotTree(Leaf(formula[1]))
    # case 2 after the NOT there is a left bracket 
    elif formula[1] is left_p:
        # then call binary_handler
        tree = binary_handler(formula[1:])
        # check if the binary tree is valid if it is not we do not evaluate it
        if tree != None:
            # not the resulting Binary tree
            tree = NotTree(tree)
    # case 3 after the NOT there is another NOT bracket
    elif formula[1] is NOT:
        # then call NOT Handler again
        tree = not_handler(formula[1:])
        # same case applies
        if tree != None:
            tree = NotTree(tree)
    # anything else and the formula rules are violated so return None
    else:
        tree = None
    return tree

def binary_handler(formula):
    ''' (str) -> (FormulaTree)
    REQ: formula[0] == '('
    Returns the FormulaTree where AND or OR is the root of the tree returns
    None iff the BinaryFormula is invalid
    >>>  binary_handler('(x)')
    None
    >>> tree = binary_handler('(x+y)')
    >>> compare = OrTree(Leaf('x'),Leaf('y'))
    >>> tree.__eq__(compare)
    True
    '''
    # define scan variable which will go through the formula
    scan = 1
    # first we evalute the Left Child which must be a leaf, binary tree
    # or Not Tree
    # case 1 Left child is leaf
    if formula[scan] in VARIABLES:
        # then store left child as a leaf
        left_c = Leaf(formula[scan])
    # case 2 Left child is another parenthese
    elif formula[scan] is left_p:
        # then call binary handler again
        left_c = binary_handler(formula[scan:])
    # case 3 Left child is Not tree
    elif formula[scan] is NOT:
        # then call Not Handler
        left_c = not_handler(formula[scan:])
    # case 4 anything else the Left Child is invalid
    else:
        # then set left child to None
        left_c = None
    # evaluate left child to see if it is valid we proceed only if
    # it is valid otherwise tree is None
    if left_c == None:
        tree = None
    else:
        # check the length of the left child using tree2formula helper function
        # and add it to scan
        scan += len(tree2formula(left_c))
        # the character immediately following the left tree must be AND or OR
        # anything else the formula is invalid        
        if formula[scan] is not AND and formula[scan] is not OR:
            tree = None
        else:
            # store the connective
            connect = formula[scan]
            # increment scan to evaluate whatever is Next
            scan += 1
            # Now we apply the same treatment with left child as with the right
            if formula[scan] in VARIABLES:
                right_c = Leaf(formula[scan])
            elif formula[scan] is left_p:
                right_c = binary_handler(formula[scan:])
            elif formula[scan] is NOT:
                right_c = not_handler(formula[scan:])
            else:
                right_c = None
            # check if right child is also invalid if it is then tree is 
            # invalid
            if right_c == None:
                tree = None
            else:
                # check the length of the left child using tree2formula helper
                # function and add it to scan
                scan += len(tree2formula(right_c))
                # the last character must be a right parenthese otherwise the 
                # whole formula is invalid
                if formula[scan] != right_p:
                    tree = None
                else:
                    # now depending on the connective we evaluate the
                    # tree as an AND tree
                    if connect is AND:
                        tree = AndTree(left_c, right_c)
                    # if it is not an And tree it must be OR
                    else:
                        tree = OrTree(left_c, right_c)
    # we return the result
    return tree


def build_tree(formula):
    ''' (str) -> FormulaTree
    Returns the FormulaTree of representing a boolean formula given a string
    representation of the boolean formula
    Return None if the formula is not valid
    - Formula is not valid if there are upper case letters 
    (ex. A*B)
    - Formula is not valid if there are no parenthese around parenthese OR and 
    AND 
    (ex. a*b)
    - Formula is not valid if there are parenthese after
    connective NOT followed by single variable 
    (ex. '-(a)')
    - Formula is not valid if there are parenthese around connective NOT
    (ex. '(-a)')

    >>> tree = build_tree('((-x+y)*-(-y+x))')
    >>> compare = AndTree(OrTree(NotTree(Leaf('x')),Leaf('y')),
                          NotTree(OrTree(NotTree(Leaf('x')),Leaf('x'))))
    >>> tree.__eq__(compare)
    True
    >>> build_tree('-(x)')
    None
    '''
    # if at any point in the handling process a index error was raised
    # the whole formula is invalid
    try:
        # case 1 if formula is a NotTree we call Not Handler helper
        if formula[0] is NOT:
            tree = not_handler(formula)
        # case 2 if formula is a left parenthese then we call binary handler
        elif formula[0] is left_p:
            tree = binary_handler(formula)
        # case 3 if formula consist of single variable and formula is len 1
        elif formula[0] in VARIABLES and len(formula) == 1:
            # then formula is simply a leaf
            tree = Leaf(formula[0])
        # case 4 otherwise formula is invalid
        else:
            tree = None
        # after we finish evaluating we check if tree is Not None and 
        # length of formula is equal to actual formula if it is not then 
        # tree is invalid
        if tree != None and len(tree2formula(tree)) != len(formula):
            tree = None
    except IndexError:
        tree = None
    return tree


def draw_formula_tree(root):
    ''' (FormulaTree, int) -> str
    Return the formula representation of a FormulaTree as a string
    >>> draw_formula_tree(build_tree('((-x+y)*-(-y+x))'))
    * - + x
          - y
        + y
          - x
    '''
    # we call draw helper with level set to 1 since we want the child of the
    # root to be set one level deeper than the root
    return draw_helper(root, 1)


def draw_helper(root, level):
    ''' (FormulaTree, int) -> str
    Return the formula representation of a FormulaTree as a string when
    given a FormulaTree, and an integer representing how many indents you want
    the child of the root to be
    >>> draw_helper(build_tree('((-x+y)*-(-y+x))'), 1)
    * - + x
          - y
        + y
          - x
    '''
    # we define the indent level to be level* the specified amount of INDENT
    # define globally
    indent_level = level*INDENT
    # seperate into 4 cases
    # case 1 the tree is a leaf
    if isinstance(root, Leaf):
        # then just return the Leaf
        string = root.get_symbol()
    # case 2 Not tree
    elif isinstance(root, NotTree):
        # we add a NOT and a space and recursively call the function again
        string = NOT + chr(32) + draw_helper(root.get_children()[0], level + 1)
    # case 3 Or tree
    elif isinstance(root, OrTree):
        # since left child builds on previous levels we do not need to add
        # indent level to it
        left = OR + chr(32) + draw_helper(root.get_children()[1], level + 1)
        # since right child does not build on previous level we add indent
        # level to it
        right = indent_level + draw_helper(root.get_children()[0], level + 1)
        # we sepearate left and right child by a line break
        string  = left + chr(10) + right
    # case 3 And Tree
    elif isinstance(root, AndTree):
        # we apply the same treatment in the case of OrTrees
        left = AND + chr(32) + draw_helper(root.get_children()[1], level + 1)
        right = indent_level + draw_helper(root.get_children()[0], level + 1)
        string  = left + chr(10) + right
    # and we return the final product
    return string


def tree2formula(tree):
    ''' (FormulaTree) -> str
    Return a string representing a formula of the FormulaTree
    >>> tree = NotTree(OrTree(Leaf('x'), AndTree(Leaf('y'), Leaf('y'))))
    >>> tree2formula(tree)
    -(x+(y*y))
    '''
    # case 1 the tree is a leaf
    if isinstance(tree, Leaf):
        # then just return the Leaf
        string = tree.get_symbol()
    # case 2 Not tree
    elif isinstance(tree, NotTree):
        # evaluate string inside
        string = '-{}'.format(tree2formula(tree.get_children()[0]))
    # case 3 Or tree
    elif isinstance(tree, OrTree):
        string = '({}+{})'.format(tree2formula(tree.get_children()[0]),
                                   tree2formula(tree.get_children()[1]))
    # case 3 And Tree
    elif isinstance(tree, AndTree):
        string = '({}*{})'.format(tree2formula(tree.get_children()[0]),
                                   tree2formula(tree.get_children()[1]))
    return string


def evaluate(root, variables, value):
    ''' (FormulaTree, str, str) -> boolean
    REQ: length of variables must match length of 
    (cannot have variables = 'xy' and value = '10101')
    REQ: all variables must match the Leafs of root
    (cannot have root = Leaf('x') and variables = y)
    REQ: values must only contain '1' or '0'
    REQ: No repeated values in variables
    (cannot have variables = 'xx')
    Return boolean based on the formula given by root and the values of the 
    variable
    >>> evaluate(build_tree('(x+y)'), 'xy', '10')
    1
    >>> evaluate(build_tree('(x*y)'), 'xy', '10')
    0
    '''
    # first we evaluate the Root we have 3 cases
    # case 1 root is a Leaf
    if isinstance(root, Leaf):
        # then get the truth value based off of variables based off of given
        # info then we return the integer representation of it
        truth = int(value[variables.find(root.get_symbol())])
    # case 2 root is a NotTree
    elif isinstance(root, NotTree):
        # then recursively evaluate the child and Not the resulting value
        # which is equivalent to 1 - (whatever the child evalutates to)
        truth = 1 - evaluate(root.get_children()[0], variables, value)
    # otherwise case 3 root is a OrTree or NotTree
    else:
        # we evaluate left child and right child 
        left_c = evaluate(root.get_children()[0], variables, value)
        right_c = evaluate(root.get_children()[1], variables, value)
        # then we determine what type of tree is the root
        if isinstance(root, OrTree):
            # if the root is Or by definition it is the minimum of the two
            # childs
            truth = max(left_c, right_c)
        else:
            # otherwise tree must be AND tree which is defined as the maximum
            # of the two childs
            truth = min(left_c, right_c)
    return truth


def play2win(root, turns, variables, values):
    ''' (FormulaTree, str, str, str) -> int
    REQ: len(turns) == len(variables)
    REQ: 0 <= len(values) < len(turns)
    REQ: No repeated variables in variables
    REQ: only the letters A and E are allowed in turns

    Returns the move that will guranteed the next player in the sequence of
    turns wins the formula game given a formula tree, the turns, variables
    and values. 
    - if the next player cannot guranteed the win then we return the default 
    value (1 if its player E, 0 if it is player A)
    
    >>> play2win(build_tree('(x*y)'),'EA','xy','1')
    1
    >>> play2win(build_tree('(x+y)'),'EA','xy','1')
    '''
    # call helper function to evaluate the expected value of playing out 1 or 0
    expect1 = play2win_helper(root, turns, variables, values + TRUTH)
    expect0 = play2win_helper(root, turns, variables, values + FALSE)
    # define the current player which must be the index after the end of value
    c_player = turns[len(values)]
    if (c_player == PLAYER1):
        # if current player is player1 and playing 1 or 0 but not the other
        # leads to 1 then play the option which leads to 1
        if (expect1 == 1 and expect0 == 0):
            win_move = 1
        elif (expect1 == 0 and expect0 == 1):
            win_move = 0
        # otherwise set to default
        else:
            win_move = 1
    # otherwise if player is player0 treat it as the same but reversed
    else:
        if (expect1 == 1 and expect0 == 0):
            win_move = 0
        elif (expect1 == 0 and expect0 == 1):
            win_move = 1
        else:
            win_move = 0
    return win_move


def play2win_helper(root, turns, variables, values):
    ''' (FormulaTree, str, str, str) -> int
    REQ: len(turns) == len(variables)
    REQ: 0 <= len(values) <= len(turns) 
    REQ: No repeated variables in variables

    Return the expected outcome resulting from playing out the game assuming
    both player plays perfectly given a formula tree, the turns, variables
    and values. 

    >>> play2win_helper(build_tree('(x*y)'),'AE','xy','1')
    1
    >>> play2win_helper(build_tree('(x+y)'),'AE','xy','1')
    0
    '''
    # our base case is when length of variables is equal to values
    if len(variables) == len(values):
        # since there is no inputs to match we evaluate the expected output
        # by simply evaluating the expression
        expected = evaluate(root, variables, values)
    else:
        # we evaluate the possibility of winning by playing 1 or 0
        expect1 = play2win_helper(root, turns, variables, values + TRUTH)
        expect0 = play2win_helper(root, turns, variables, values + FALSE)
        # define the current player which must be 1 index after values ended
        # so we use length of value to access it
        c_player = turns[len(values)]
        # if any play leads to truth and current player is player1 then the 
        # expected value must be truth
        if (1 in (expect1, expect0) and c_player == PLAYER1):
            expected = 1
        # if any play leads to false and current player is player0 then the 
        # expected value must be false
        elif (0 in (expect1, expect0) and c_player == PLAYER0):
            expected = 0
        # if both play leads to truth then the expected value must be true
        elif (expect1 == 1 and expect0 == 1):
            expected = 1
        # otherwise both play must lead to false then then expected value is
        # false
        else:
            expected = 0
    return expected



if __name__ == '__main__':
    print(tree2formula(build_tree('((-x+y)*-(-y+x))')))
    tree = build_tree('(--(---x+y)*(--x+z))')
    print(draw_formula_tree(tree))
    tree = build_tree('(x+y)')
    print(evaluate(tree, 'xy', '10'))
    tree = build_tree('(x*y)')
    print(evaluate(tree, 'xy', '11'))
    print(build_tree("(x+y*z)"))                       # Ambiguous
    print(build_tree("(x*y*z)"))                       # and is binary, not trinary
    print(build_tree("((x+y)*(x-y)*(x+z))"))           # Same thing, but also note that "-" is UNARY.
    print(build_tree("(x+(u*v*w*z)+y)"))               # It was just an example of the bonus.
    print(build_tree("-x-y"))                          # - is not binary. Only unary.
    print(build_tree("(x+y*x+y)"))                     # Missing "(" (Thanks anon)
    print(build_tree("x)"))                            # ) not needed 
    print(build_tree("++++x "))                        # Or is not a unary operator.
    print(build_tree("-(-a)"))                         # Brackets not permitted for not
    print(build_tree("(x+y)*(x+z)"))                   # Missing brackets
    print(build_tree("-(ab)"))                         # missing binary operator
    print(build_tree("(a+(B*-c))"))                    # capital variable name
    print(build_tree("(x * c)"))                       # Space in the formula
    print(build_tree("-+x"))                           # binary connective does not distribute
    print(build_tree("!a"))                            # foreign character
    print(build_tree("(x+x(()"))                       # more mismatched parantheses
    print(build_tree("((x+y))"))                       # Extraneous parantheses
    print(build_tree(")x+y("))			       # This one actually got me lol, fixed my code tho.
    print(build_tree("(x+y))"))                        # Extra closing paranthesis
    print(build_tree("((x*y)"))                        # Extra opening paranthesis
    print(build_tree("((x+y)*((y%z)*(-y+-z)))"))       # an illegal character in the middle of a long formula
    print(build_tree("''"))                            # empty str
    print(build_tree("' '"))                           # space
    print(build_tree("(a+*+*+*b)"))
    print(build_tree("(a+*)"))                         # no foreign character, but a symbol should not be a child
    print(build_tree("(((((x*y)))))"))
    tree = build_tree('((-x+y)*z)')
    print(play2win(tree, 'EAE', 'xyz', ''))
    # tree = build_tree('(a+(((((c*v)*(t+u))+-((o+-z)+((p+(r*s))*-q)))+(d*e))*((f+-(y+z))+-((x+j)*((k+(l+w))+(m*-n))))))')
    # play2win(tree, 'EAEAEAEAEAEAEAEAEAEAEA','acvtuozprsqdefyxjklwmn', '')