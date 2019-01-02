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
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)

        left = ['QD', 'KD', '9D', 'JD', '10D'] 
        right = ['JS', '8S', 'KS', 'AS', 'QS']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
            
        left = ['QD', 'KD', '9D', 'JD', '10D'] 
        right = ['QS', '9S', 'KS', 'JS', '10S']
        self.evaluateAndValidate(left, right, evaluation.evaluator.TIE)
            
        left=['12S', '12H', '2D', '3D', '4D']
        right = ['14S', '13H', '12D', '11D', '10D']
        self.evaluateAndValidate(left, right, evaluation.evaluator.RIGHT)
            
            
        left = ['QS', 'QH', '2D', '3D', '4D'] 
        right = ['10H', 'QH', '2D', '3D', '4D']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
          
        left = ['QS', 'QH', 'QD', '3D', '4D'] 
        right = ['10H', '10D', 'AD', 'AH', 'KD']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
          
        left = ['QS', 'QH', 'QD', '3D', '3H'] 
        right = ['10H', '9H', 'AH', 'KH', 'QH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
          
        left = ['10H', '9H', 'AH', 'KH', 'QH']
        right = ['QS', 'QH', 'QD', '3D', '4D'] 
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
        
        left = ['10H', 'JH', 'AH', 'KH', 'QH']
        right = ['QS', 'JS', '10S', 'KS', 'AS'] 
        self.evaluateAndValidate(left, right, evaluation.evaluator.TIE)
        
        left = ['10H', '10D', '9H', '9D', 'QH']
        right = ['10S', '10C', '9S', '9C', 'JH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
        
        left = ['JH', 'JD', 'JS', 'JC', 'QH']
        right = ['10H', '10D', '10S', '10C', 'QH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)     
        
        left = ['10H', '10D', '10S', '10C', 'QH']
        right = ['10H', '10D', '10S', '10C', 'JH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)

        end = datetime.datetime.now()
        delta = end - start
        print("Time = " + str(int(delta.total_seconds() * 1000)) + " millisecond ")

    def test_evaluators_edge_cases_and_more(self):
        
        ## Royal vs straight flush                   
        left = ['JH', '10H', 'QH', 'KH', 'AH']
        right = ['10S', '9S', '8S', '7S', 'JS']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)

        ## Straight Flush vs  Straight Flush
        left = ['10S', '9S', '8S', '7S', 'JS']
        right = ['10H', '9H', '8H', '7H', '6H'] 
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
 
        ## Straight Flush vs 4 of a kind
        left = ['10S', '9S', '8S', '7S', 'JS']
        right = ['10H', '10D', '10S', '10C', 'JH'] 
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
         
        ## 4 of a kind variants
        left = ['JH', 'JD', 'JS', 'JC', 'QH']
        right = ['10H', '10D', '10S', '10C', 'QH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
         
        left = ['JH', 'JD', 'JS', 'JC', 'QH']
        right = ['JH', 'JD', 'JS', 'JC', 'QH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.TIE)
 
        left = ['JH', 'JD', 'JS', 'JC', 'QH']
        right = ['JH', 'JD', 'JS', 'JC', '5H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)

        ### Full House Variants
        left = ['JH', 'JD', 'JS', '8C', '8H']
        right = ['10H', '10D', '10S', '9C', '9H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
#         
        left = ['10H', '10D', '10S', '8C', '8H']
        right = ['10H', '10D', '10S', '8C', '8H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.TIE)
#         
        left = ['10H', '10D', '10S', '8C', '8H']
        right = ['10H', '10D', '10S', '7C', '7H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)

#         ### Flush Variants
        left = ['10H', '9H', 'AH', 'QH', '6H']
        right = ['10D', '9D', 'AD', 'QD', '6D']
        self.evaluateAndValidate(left, right, evaluation.evaluator.TIE)
#         
        left = ['10H', '9H', 'AH', 'QH', '6H']
        right = ['10D', '7D', 'AD', 'QD', '6D']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)

        ## Straight Variants
        left = ['10H', 'AD', 'KS', 'QC', 'JH'] 
        right = ['JH', '10D', '9S', '8C', 'QH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)# 
#          
        left = ['JH', '10D', '9S', '8C', 'QH']
        right = ['JH', '10C', '9H', '8D', 'QS']
        self.evaluateAndValidate(left, right, evaluation.evaluator.TIE)
        
        left = ['JH', '10D', '9S', '8C', 'KH']# NOT A STRAIGHT
        right = ['JH', '10C', '9H', '8D', 'QS']
        self.evaluateAndValidate(left, right, evaluation.evaluator.RIGHT)
        
        ## Three of a kind Variants
        left = ['10H', '10D', '10S', '8C', 'QH']
        right = ['10H', '10D', '10S', '8C', 'JH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
#  
        left = ['10H', '10D', '10S', '8C', 'QH']
        right = ['9H', '9D', '9S', 'AC', 'KH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
#          
        left = ['2H', '2D', '2S', 'AC', '4H']
        right = ['2H', '2D', '2S', 'AC', '3H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)

        ## Two Pair Variants
        left = ['10H', '10D', '8S', '8C', 'QH']
        right = ['10H', '10D', '8S', '8C', 'JH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
   
        left = ['10H', '10D', '8S', '8C', 'QH']
        right = ['9H', '9D', '8S', '8C', 'KH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
           
        left = ['AH', 'AD', 'QS', 'QC', '4H']
        right = ['AH', 'AD', 'QS', 'QS', '4D']
        self.evaluateAndValidate(left, right, evaluation.evaluator.TIE)
        
        ## Pair Variants
        left = ['10H', '10D', 'AS', 'KH', 'QH']
        right = ['10H', '10D', 'AC', 'KC', 'JH']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
   
        left = ['10H', '10D', 'AS', 'KC', 'QH']
        right = ['9H', '9D', '2S', '3C', '4H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
            
        left = ['AH', 'AD', '2S', '3C', '4H']
        right = ['KH', 'KD', 'AS', 'QS', 'JD']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)

        ## High card and different types
        left = ['JH', '10D', 'AS', '8C', 'QH']
        right = ['AH', '10D', 'JS', 'QC', '7H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
 
        left = ['JH', '10D', 'AS', '8C', 'QH']
        right = ['AH', '10D', 'JS', '8H', '7H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)

        left = ['2H', '3D', '4S', '5H', '2D']
        right = ['AH', '10D', 'JS', '8H', '7H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.LEFT)
        
        left = ['2H', '3D', '4S', '5H', '2D']
        right = ['AH', 'AD', 'JS', '8H', '7H']
        self.evaluateAndValidate(left, right, evaluation.evaluator.RIGHT)

        left = ['2H', 'KD', '7S', 'QH', '10D']
        right = ['10H', 'QD', '7S', 'KH', '2D']
        self.evaluateAndValidate(left, right, evaluation.evaluator.TIE)
       
    def evaluateAndValidate(self, left, right, winner):
        print(left, right)
        handEval = evaluation.evaluator.compare_hands(left, right)
        print (handEval)
        
        self.assertEquals(winner, handEval[0])
        
    def test_best_of_seven_two_of_a_kind (self):
#         pass
#Four of Diamonds, Ace of Spades, Six of Clubs, Two of Spades, Ace of Diamonds, Six of Diamonds, King of Diamonds
# This test failed with the initial evaluator
        hand = Hand()
        card = Card('4','D')
        hand.cards.append(card)
        card = Card('14','S')
        hand.cards.append(card)
        card = Card('6','C')
        hand.cards.append(card)
        card = Card('2','S')
        hand.cards.append(card)
        card = Card('14','D')
        hand.cards.append(card)
        card = Card('6','D')
        hand.cards.append(card)
        card = Card('13','D')
        hand.cards.append(card)
  
        print(hand.toEvalList())
        lst = hand.get5CardCombosFrom7CardsForEval()
        print("there were " + str(len(lst)) + " variations found")
        lst.sort()
        print(lst)
          
        for cardList in lst:
            self.assertEqual(len(cardList),5) 

        print(lst)
        print(lst)
        wins = hand.getBest5CardHand()
        self.assertEqual(len(wins), 5)
        self.assertTrue('14S' in wins)
        self.assertTrue('14D' in wins)
        self.assertTrue('6C' in wins)
        self.assertTrue('6D' in wins)
        self.assertTrue('13D' in wins)           

if __name__ == '__main__':
    unittest.main()
