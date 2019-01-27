import unittest
from deck import Deck, Card
import logging

class TestDeck(unittest.TestCase):
    def test_52_cards_are_unique(self):
        deck = Deck()
        deck.shuffle()
        listOfCards = []
        for _ in range(0, 52):
            card = deck.deal()
            logging.debug(card)
            self.assertFalse(card in listOfCards, "Duplicate card found in deck!!!" + str(card))
            listOfCards.append(card)
 
    def test_52_cards(self):
        deck = Deck()
        deck.shuffle()
        self.assertEqual(52, len(deck.cards))
        print(deck)
        for _ in range(5):
            deck.deal();
        self.assertEqual(47, len(deck.cards))
        print(deck)
        for _ in range(20):
            deck.deal();
        self.assertEqual(27, len(deck.cards))
        print(deck)
        
    def test_card_from_string(self):
        
        card = Card.stringToCard("10H")
        self.assertEqual(card.rank, '10')
        self.assertEqual(card.suit, 'H')
        
        card = Card.stringToCard("KH")
        self.assertEqual(card.rank, 'K')
        self.assertEqual(card.suit, 'H')
        
        card = Card.stringToCard("2S")
        self.assertEqual(card.rank, '2')
        self.assertEqual(card.suit, 'S')
        self.assertEqual(str(card), 'Two of Spades')
                

if __name__ == '__main__':
    unittest.main()


