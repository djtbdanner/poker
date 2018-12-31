import unittest
from deck import Deck, Card
from player import Hand, Player
import evaluation.evaluator
import datetime

class TestEvaluator(unittest.TestCase):
    
    def test_evaluator(self):
#         pass
        '''
        This tests shuffle play view - manual no actual tests
        '''
        deck = Deck()
        deck.shuffle()
        player = Player()
         
        for _ in range(7):
            player.hand.cards.append(deck.deal())
             
        player.showHand()   
        print(player.hand.getBest5CardHand())
        
    def test_best_of_seven_3_of_a_kind (self):
#         pass
        hand = Hand()
        card = Card('4','D')
        hand.cards.append(card)
        card = Card('14','C')
        hand.cards.append(card)
        card = Card('14','D')
        hand.cards.append(card)
        card = Card('11','S')
        hand.cards.append(card)
        card = Card('10','H')
        hand.cards.append(card)
        card = Card('14','S')
        hand.cards.append(card)
        card = Card('5','D')
        hand.cards.append(card)
        wins = hand.getBest5CardHand()
        self.assertTrue('14C' in wins)
        self.assertTrue('14D' in wins)
        self.assertTrue('14S' in wins)
        self.assertTrue('11S' in wins)
        self.assertTrue('10H' in wins)
        
    def test_best_of_seven_flush_and_straight (self):
#         pass
        hand = Hand()
        card = Card('14','H')
        hand.cards.append(card)
        card = Card('13','H')
        hand.cards.append(card)
        card = Card('12','H')
        hand.cards.append(card)
        card = Card('11','S')
        hand.cards.append(card)
        card = Card('10','H')
        hand.cards.append(card)
        card = Card('5','S')
        hand.cards.append(card)
        card = Card('2','H')
        hand.cards.append(card)

        wins = hand.getBest5CardHand()
        self.assertEqual(len(wins), 5)
        self.assertTrue('14H' in wins)
        self.assertTrue('13H' in wins)
        self.assertTrue('12H' in wins)
        self.assertTrue('10H' in wins)
        self.assertTrue('2H' in wins)      

    def test_best_of_seven_straight (self):
#         pass
        hand = Hand()
        card = Card('14','H')
        hand.cards.append(card)
        card = Card('13','H')
        hand.cards.append(card)
        card = Card('12','H')
        hand.cards.append(card)
        card = Card('11','S')
        hand.cards.append(card)
        card = Card('10','H')
        hand.cards.append(card)
        card = Card('5','S')
        hand.cards.append(card)
        card = Card('2','D')
        hand.cards.append(card)

        wins = hand.getBest5CardHand()
        self.assertEqual(len(wins), 5)
        self.assertTrue('14H' in wins)
        self.assertTrue('13H' in wins)
        self.assertTrue('12H' in wins)
        self.assertTrue('10H' in wins)
        self.assertTrue('11S' in wins)   
        
    def test_best_of_seven_two_pair (self):
#         pass
        hand = Hand()
        card = Card('2','H')
        hand.cards.append(card)
        card = Card('2','D')
        hand.cards.append(card)
        card = Card('3','H')
        hand.cards.append(card)
        card = Card('3','S')
        hand.cards.append(card)
        card = Card('14','H')
        hand.cards.append(card)
        card = Card('11','S')
        hand.cards.append(card)
        card = Card('5','D')
        hand.cards.append(card)

        wins = hand.getBest5CardHand()
        self.assertEqual(len(wins), 5)
        self.assertTrue('2H' in wins)
        self.assertTrue('2D' in wins)
        self.assertTrue('3H' in wins)
        self.assertTrue('3S' in wins)
        self.assertTrue('14H' in wins)

    def test_best_of_seven_low_straight (self):
#         pass
        hand = Hand()
        card = Card('14','H')
        hand.cards.append(card)
        card = Card('13','H')
        hand.cards.append(card)
        card = Card('2','H')
        hand.cards.append(card)
        card = Card('3','S')
        hand.cards.append(card)
        card = Card('4','H')
        hand.cards.append(card)
        card = Card('5','S')
        hand.cards.append(card)
        card = Card('10','D')
        hand.cards.append(card)

        wins = hand.getBest5CardHand()
        self.assertEqual(len(wins), 5)
        self.assertTrue('14H' in wins)
        self.assertTrue('2H' in wins)
        self.assertTrue('3S' in wins)
        self.assertTrue('4H' in wins)
        self.assertTrue('5S' in wins)   

    def test_evaluations(self):

        start = datetime.datetime.now()
          
        left = ['14C', '14D', '11S', '10H', '14S'] 
        right = ['14D', '14S', '5D', '4D', '14C']
        print(left, right)
        print (evaluation.evaluator.compare_hands(left, right))
        self.assertTrue(evaluation.evaluator.leftIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.rightIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.leftIsLessThanOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.rightIsLessThanOrEqual(left, right))

        left = ['QD', 'KD', '9D', 'JD', 'TD'] 
        right = ['JS', '8S', 'KS', 'AS', 'QS']
        print(left, right)
        print (evaluation.evaluator.compare_hands(left, right))
        self.assertTrue(evaluation.evaluator.leftIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.rightIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.leftIsLessThanOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.rightIsLessThanOrEqual(left, right))
            
        left = ['QD', 'KD', '9D', 'JD', 'TD'] 
        right = ['QS', '9S', 'KS', 'JS', 'TS']
        print(left, right)
        print (evaluation.evaluator.compare_hands(left, right))
        self.assertTrue(evaluation.evaluator.leftIsGreaterOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.rightIsGreaterOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.leftIsLessThanOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.rightIsLessThanOrEqual(left, right))
            
        left=['12S', '12H', '2D', '3D', '4D']
        right = ['14S', '13H', '12D', '11D', '10D']
        print(left, right)
        print (evaluation.evaluator.compare_hands(left, right))
        self.assertFalse(evaluation.evaluator.leftIsGreaterOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.rightIsGreaterOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.leftIsLessThanOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.rightIsLessThanOrEqual(left, right))
            
            
        left = ['QS', 'QH', '2D', '3D', '4D'] 
        right = ['10H', 'QH', '2D', '3D', '4D']
        print(left, right)
        print (evaluation.evaluator.compare_hands(left, right))
        self.assertTrue(evaluation.evaluator.leftIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.rightIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.leftIsLessThanOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.rightIsLessThanOrEqual(left, right))
          
        left = ['QS', 'QH', 'QD', '3D', '4D'] 
        right = ['10H', '10D', 'AD', 'AH', 'KD']
        print(left, right)
        print (evaluation.evaluator.compare_hands(left, right))
        self.assertTrue(evaluation.evaluator.leftIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.rightIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.leftIsLessThanOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.rightIsLessThanOrEqual(left, right))     
          
        left = ['QS', 'QH', 'QD', '3D', '3H'] 
        right = ['10H', '9H', 'AH', 'KH', 'QH']
        print(left, right)
        print (evaluation.evaluator.compare_hands(left, right))
        self.assertTrue(evaluation.evaluator.leftIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.rightIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.leftIsLessThanOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.rightIsLessThanOrEqual(left, right))  
          
        left = ['10H', '9H', 'AH', 'KH', 'QH']
        right = ['QS', 'QH', 'QD', '3D', '4D'] 
        print(left, right)
        print (evaluation.evaluator.compare_hands(left, right))
        self.assertTrue(evaluation.evaluator.leftIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.rightIsGreaterOrEqual(left, right))
        self.assertFalse(evaluation.evaluator.leftIsLessThanOrEqual(left, right))
        self.assertTrue(evaluation.evaluator.rightIsLessThanOrEqual(left, right))           
          
        end = datetime.datetime.now()
        delta = end - start
        print("Time = " + str(int(delta.total_seconds() * 1000)) + " millisecond ")

if __name__ == '__main__':
    unittest.main()
