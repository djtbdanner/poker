import unittest
from deck import Card
from player import Hand
import evaluation

class TestEvaluator(unittest.TestCase):
    
    def test_best_of_seven_two_of_a_kind (self):
#         pass
#Four of Diamonds, Ace of Spades, Six of Clubs, Two of Spades, Ace of Diamonds, Six of Diamonds, King of Diamonds
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
        lst = hand.getFiveCardCombosForEval()
        print("there were " + str(len(lst)) + " variations found")
         
        for cardList in lst:
            self.assertEqual(len(cardList),5) 
        print(lst)
        evaluation.evaluatorsort.quickSort(lst)
        print(lst)
        wins = hand.getBest5CardHand()
        self.assertEqual(len(wins), 5)
        self.assertTrue('14S' in wins)
        self.assertTrue('14D' in wins)
        self.assertTrue('6C' in wins)
        self.assertTrue('6D' in wins)
        self.assertTrue('13D' in wins)   

    def test_best_of_10_two_of_a_kind (self):
#          pass
#Four of Diamonds, Ace of Spades, Six of Clubs, Two of Spades, Ace of Diamonds, Six of Diamonds, King of Diamonds
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
        card = Card('11','S')
        hand.cards.append(card)
        card = Card('9','D')
        hand.cards.append(card)
        card = Card('7','D')
        hand.cards.append(card)

        print(hand.toEvalList())
        lst = hand.getFiveCardCombosForEval()
        print("there were " + str(len(lst)) + " variations found")
        
        for cardList in lst:
            self.assertEqual(len(cardList),5) 
        print(lst)
        evaluation.evaluatorsort.quickSort(lst)
        print(lst)
        wins = hand.getBest5CardHand()
        self.assertEqual(len(wins), 5)
        self.assertTrue('6D' in wins)
        self.assertTrue('14D' in wins)
        self.assertTrue('4D' in wins)
        self.assertTrue('9D' in wins)
        self.assertTrue('7D' in wins)        
          
if __name__ == '__main__':
    unittest.main()
