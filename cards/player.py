import uuid
import evaluation.evaluatorsort
from deck import Card
class Hand:
    def __init__(self):    
        self.cards = []

    # list of cards is used for the evaluation of the hand, this will format for that process
    def toEvalList(self):
        result = []
        for card in self.cards:
            result.append(card.rank+card.suit)
        return result
    
    # Build all 5 card combinations of the 7 (or whatever number) cards in the player's hand 
    def getFiveCardCombosForEval(self):
        result = []
        added = len(self.cards) - 5
        if (added > 2):
            added = 2
        for index, _ in enumerate(self.toEvalList()):
            for nextIndex in range (1, added+2):
                result.append(self.buildList(index, nextIndex, nextIndex+4))
            for nextIndex in range (0, added+2):
                for skipSize in range (1, added+1 ):
                    result.append(self.buildSkippedList(index, nextIndex, skipSize))
        return result

    # Build the list of different combinations of cards for 5 card evaluation
    # spins through list reducing size to 5
    # then moving over one and doing it again
    def buildList(self, initialIndex, a, b):
        cardsInHand = self.toEvalList()
        fiveCardHand = []
        fiveCardHand.append(cardsInHand[initialIndex])
        for index in range(a, b):
            cardIndex = initialIndex+index
            fiveCardHand.append(cardsInHand[self._checkCardIndex(cardIndex)])
        return fiveCardHand
    
    # Builds list skipping one or two fields 
    def buildSkippedList(self, initialIndex, index, skip):
        cardsInHand = self.toEvalList()
        fiveCardHand = []
        fiveCardHand.append(cardsInHand[initialIndex])
        for indicator in range(initialIndex+1, initialIndex + index+1):
            fiveCardHand.append(cardsInHand[self._checkCardIndex(indicator)])
            
        start = len(fiveCardHand)+initialIndex
        for ind in range(start, start+(5-len(fiveCardHand))):
            cardIndex = ind + skip
            fiveCardHand.append(cardsInHand[self._checkCardIndex(cardIndex)])
        return fiveCardHand
    
    def _checkCardIndex(self,index):
        listSize = len(self.toEvalList())
        if index >= listSize:
            index = index - listSize
        return index
    
    # Get the best 5 cards of the hand as a list
    def getBest5CardHand(self):
        combos = self.getFiveCardCombosForEval()
        evaluation.evaluatorsort.quickSort(combos)
        return combos.pop()
    
    def bestHandAsCards(self):
        bestHand = self.getBest5CardHand()
        result = []
        for cardString in bestHand:
            result.append(Card.stringToCard(cardString))
        return result
    
class Player:
    def __init__(self, name="A Player with no name", chips=100, dealer=False):
        self.hand = Hand()
        self.name = name  
        self.id=uuid.uuid4()
        self.chips = chips
        self.dealer = dealer
        self.position = 1

    def showHand(self):
        print("\n"+ self.name + ":")
        myCards = '\t'
        for card in self.hand.cards[:-1]:
            myCards = myCards + str(card)
            myCards = myCards + ", "
        myCards = myCards + str(self.hand.cards[-1])
        print(myCards)
