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

# Globally Define the symbols for NOT, AND, OR, left Parenthese,
# right Parenthese, and variables allowed
AND = '*'
OR = '+'
NOT = '-'
LEFT_P = '('
RIGHT_P = ')'
VARIABLES = 'abcdefghijklmnopqrstuvwxyz'
# define alphabet representation of each player
PLAYER0 = 'A'
PLAYER1 = 'E'
# define the how much a child is specified to be indented in draw formula tree
# which is 2 spaces
INDENT = '  '


def tree2formula(tree):
    ''' (FormulaTree) -> str
    Return a string representing a formula of the FormulaTree

    >>> tree2formula(NotTree(OrTree(Leaf('x'), AndTree(Leaf('y'), Leaf('y')))))
    '-(x+(y*y))'
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


def not_handler(formula):
    ''' (str) -> FormulaTree
    REQ: fomula[0] == '-'
    Returns the FormulaTree where NOT is the root of the tree
    Returns None iff the NOT formula is invalid

    >>> not_handler('-(x+y)')
    NotTree(OrTree(Leaf('x'), Leaf('y')))
    >>> None == not_handler('-+x')
    True
    '''
    # A formula with a Not in front has 4 cases
    # case 1 after the NOT there is a variable
    if formula[1] in VARIABLES:
        # then return the NotTree + the Leaf
        tree = NotTree(Leaf(formula[1]))
    # case 2 after the NOT there is a left bracket
    elif formula[1] is LEFT_P:
        # then call binary_handler
        tree = binary_handler(formula[1:])
        # check if the binary tree is valid if it is not we do not evaluate it
        if tree is not None:
            # not the resulting Binary tree
            tree = NotTree(tree)
    # case 3 after the NOT there is another NOT bracket
    elif formula[1] is NOT:
        # then call NOT Handler again
        tree = not_handler(formula[1:])
        # same case applies
        if tree is not None:
            tree = NotTree(tree)
    # anything else and the formula rules are violated so return None
    else:
        tree = None
    return tree


def binary_handler(formula):
    ''' (str) -> FormulaTree
    REQ: formula[0] == '('
    Returns the FormulaTree where AND or OR is the root of the tree
    Returns None iff the BinaryFormula is invalid

    >>> binary_handler('(x+y)')
    OrTree(Leaf('x'), Leaf('y'))
    >>> None == binary_handler('(x)')
    True
    '''
    # define scan variable which index each character in formula we start off
    # at 1 to skip the first parenthese
    scan = 1
    # First we evaluate the left child
    # case 1 Left child is leaf
    if formula[scan] in VARIABLES:
        # then store left child as a leaf
        left_c = Leaf(formula[scan])
    # case 2 Left child is another parenthese
    elif formula[scan] is LEFT_P:
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
    if left_c is None:
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
            elif formula[scan] is LEFT_P:
                right_c = binary_handler(formula[scan:])
            elif formula[scan] is NOT:
                right_c = not_handler(formula[scan:])
            else:
                right_c = None
            # check if right child is also invalid if it is then tree is
            # invalid
            if right_c is None:
                tree = None
            else:
                # check the length of the left child using tree2formula helper
                # function and add it to scan
                
                scan += len(tree2formula(right_c))
                # the last character must be a right parenthese otherwise the
                # whole formula is invalid
                if formula[scan] != RIGHT_P:
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
    Return None if the formula is invalid
    - Formula is valid if every OR, AND operator is surrounded by parenthese
    (x+y)
    - Formula is valid if every unary operator is not surrounded by parenthese
    (-x or x)
    - Formula is valid if it only contains lower case letters
    - if any rule is violated then formula is invalid

    >>> build_tree('(x+y)')
    OrTree(Leaf('x'), Leaf('y'))
    >>> None == build_tree('-(A)')
    True
    '''
    # if at any point in the handling process a index error was raised
    # the whole formula is invalid
    try:
        # there are only 4 cases for every type of formula
        # case 1 if formula is a NotTree we call not helper function
        if formula[0] is NOT:
            tree = not_handler(formula)
        # case 2 if formula is closed off by parenthese then we call binary
        # handler helper function
        elif formula[0] is LEFT_P and formula[-1] is RIGHT_P:
            tree = binary_handler(formula)
        # case 3 if formula is variable of length 1 then formula is a leaf
        elif formula in VARIABLES and len(formula) == 1:
            tree = Leaf(formula)
        # case 4 otherwise formula is invalid
        else:
            tree = None
    except IndexError:
        tree = None
    return tree


def draw_formula_tree(root):
    ''' (FormulaTree) -> str
    Return the string representation of a FormulaTree given a FormulaTree
    - the string representation return is the formula tree turn sideways
    with the right child on Top and the left on the bottom
    - every left child is indented two spaces from the parent as specified by
    the globally defined INDENT string

    >>> draw_formula_tree(build_tree('((-x+y)*-(-y+x))'))
    '* - + x\\n      - y\\n  + y\\n    - x'
    '''
    # we call draw helper with level set to 1 since we want the left child
    # of the root to be set one level deeper than the root
    return draw_helper(root, 1)


def draw_helper(root, level):
    ''' (FormulaTree, int) -> str
    Return the formula representation of a FormulaTree as a string when
    given a FormulaTree, and an integer representing how many level of indent
    you want the left child of the root start at

    >>> draw_helper(build_tree('((-x+y)*-(-y+x))'), 1)
    '* - + x\\n      - y\\n  + y\\n    - x'
    '''
    # we define the indent level to be level*the specified amount of INDENT
    # define globally we define it this way because every level has a different
    # amount of indent
    indent_level = level*INDENT
    # there are 4 cases for the root: case 1 the tree is a leaf
    if isinstance(root, Leaf):
        # then just return the Leaf
        string = root.get_symbol()
    # case 2 Not tree
    elif isinstance(root, NotTree):
        # we add a NOT and a space and recursively call the function again
        # we increment the level because we are going one level deeper
        string = NOT + chr(32) + draw_helper(root.get_children()[0], level + 1)
    # case 3 Or tree
    elif isinstance(root, OrTree):
        # evaluate right and left child with proper spacing we add indent_level
        # to the left child because unlike the right child it does not build
        # on previous levels
        right = OR + chr(32) + draw_helper(root.get_children()[1], level + 1)
        left = indent_level + draw_helper(root.get_children()[0], level + 1)
        # we sepearate left and right child by a line break
        string = right + chr(10) + left
    # case 4 And Tree
    else:
        # we apply the same treatment as with Ortree case
        right = AND + chr(32) + draw_helper(root.get_children()[1], level + 1)
        left = indent_level + draw_helper(root.get_children()[0], level + 1)
        string = right + chr(10) + left
    return string


def evaluate(root, variables, value):
    ''' (FormulaTree, str, str) -> int
    REQ: len(variable) == len(value)
    REQ: all variables must match the Leafs of root
    REQ: values must only contain '1' or '0'
    REQ: No repeated letters in variables
    Return truth value of the formula given by root given the FormulaTree,
    string representing the variables of FormulaTree and string representing
    the truth value of each variable

    >>> evaluate(build_tree('(x+y)'), 'xy', '10')
    1
    >>> evaluate(build_tree('(x*y)'), 'xy', '10')
    0
    '''
    # we have 3 cases when evaluating root: case 1 if root is a Leaf
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
        # we evaluate left child and right child and determine the type of root
        left_c = evaluate(root.get_children()[0], variables, value)
        right_c = evaluate(root.get_children()[1], variables, value)
        if isinstance(root, OrTree):
            # if the root is Or by definition it is the maximum of the two
            # childs since (1,0) -> 1 and (0,1) -> 1 and (0,0) -> 0
            truth = max(left_c, right_c)
        else:
            # otherwise tree must be AND tree which is defined as the minimum
            # of the two childs since (1,0) -> 0 and (0,1) -> 0 and (1,1) -> 1
            truth = min(left_c, right_c)
    return truth


def play2win(root, turns, variables, values):
    ''' (FormulaTree, str, str, str) -> int
    REQ: len(turns) == len(variables)
    REQ: 0 <= len(values) < len(turns)
    REQ: No repeated variables in variables
    REQ: only the letters A and E are allowed in turns
    Returns the move that will guranteed the next player in the sequence of
    turns to win the formula game given a formula tree, the turns, variables
    and values.
    - if the next player cannot guranteed the win then we return the default
    value (1 if its player E, 0 if it is player A)

    >>> play2win(build_tree('(x*y)'),'AE','xy','')
    0
    >>> play2win(build_tree('(x+y)'),'EA','xy','')
    1
    '''
    # call helper function to evaluate the expected value of playing out 1 or 0
    expect1 = play2win_helper(root, turns, variables, values + '1')
    expect0 = play2win_helper(root, turns, variables, values + '0')
    # define the current player which must be the index after the end of value
    # so we can use length of value to access the current player
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
    REQ: only the letters A and E are allowed in turns
    Return the expected outcome resulting from playing out the game assuming
    both player plays perfectly given a formula tree, the turns, variables
    and values.

    >>> play2win_helper(build_tree('(x*y)'),'AE','xy','')
    0
    >>> play2win_helper(build_tree('(x+y)'),'EA','xy','')
    1
    '''
    # our base case is when length of variables is equal to values since this
    # is the only time we can evaluate the formula as a whole
    if len(variables) == len(values):
        # since there is no inputs to match we evaluate the expected output
        # by simply evaluating the expression
        expected = evaluate(root, variables, values)
    else:
        # we evaluate the possibility of winning by playing 1 or 0
        expect1 = play2win_helper(root, turns, variables, values + '1')
        expect0 = play2win_helper(root, turns, variables, values + '0')
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
        # otherwise both play must lead to false then expected value is false
        else:
            expected = 0
    return expected
