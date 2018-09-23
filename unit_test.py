import unittest
from formula_game_functions import *


class TestBuildTree(unittest.TestCase):
    
    def test_01_OR(self):
        mytree = build_tree('(x+y)')
        mytree2 = OrTree(Leaf('x'), Leaf('y'))
        self.assertEqual(mytree, mytree2, 'testing OR tree capabilities')
    
    def test_02_AND(self):
        mytree = build_tree('(x*y)')
        mytree2 = AndTree(Leaf('x'), Leaf('y'))
        self.assertEqual(mytree, mytree2, 'testing AND tree capabilities')

    def test_03_NOT(self):
        mytree = build_tree('-x')
        mytree2 = NotTree(Leaf('x'))
        self.assertEqual(mytree, mytree2, 'testing NOT tree capabilities')
    
    def test_04_NOT_with_parenthese(self):
        mytree = build_tree('-(x+y)')
        mytree2 = NotTree(OrTree(Leaf('x'), Leaf('y')))
        self.assertEqual(mytree, mytree2, 'testing NOT with parenthese')
    
    def test_05_Multiple(self):
        mytree = build_tree('-(x*-((x*y)+a))')
        mytree2 = NotTree(AndTree(Leaf('x'), NotTree(OrTree(AndTree(Leaf('x'),Leaf('y')), Leaf('a')))))
        self.assertEqual(mytree, mytree2, 'testing Multiple parenthese')
    
    def test_06_Invalid_miss_p(self):
        my_tree = build_tree('x+y')
        self.assertEqual(my_tree, None, 'invalid missing parenthese')
    
    def test_07_Invalid_upper_case(self):
        my_tree = build_tree('X')
        self.assertEqual(my_tree, None, 'invalid case')
    
    def test_08_mismatch_p(self):
        my_tree = build_tree('(x+(y)+z)')
        self.assertEqual(my_tree, None, 'mismatch parenthese')
    
    def test_09_mismatch_p(self):
        my_tree = build_tree('-(x)')
        self.assertEqual(my_tree, None, 'extranueous parenthese')

class TestPlay2Win(unittest.TestCase):
    '''  E wants 1 A wants 0 '''
    def test_1_A_wins(self):
        win = play2win(build_tree('(x+-y)'), "EA", "xy", "0")
        self.assertEqual(win, 1, 'A should play 1')
    def test_2_E_wins(self):
        win = play2win(build_tree('(-x*y)'), "AE", "xy", "0")
        self.assertEqual(win, 1, 'E should play 1')    
    
    def test_3_E_cannot_win(self):
        win = play2win(build_tree('(x*y)'), "AE", "xy", "0")
        self.assertEqual(win, 1, 'E defaults to 1')         
        
    def test_4_A_cannot_win(self):
        win = play2win(build_tree('(x+y)'), "EA", "xy", "1")
        self.assertEqual(win, 0, 'A defaults to 0')         
    
      
    


if(__name__ == "__main__"):
    unittest.main(exit=False)

    
    