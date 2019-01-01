import uuid
import evaluation.evaluator
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
    
    # Build all 5 card combinations of the 7  cards in the player's hand
    # (At this time will not work for numbers in hand other than 7)
    def get5CardCombosFrom7CardsForEval(self):
        result = []
        cardsInHandCount = len(self.cards)
        if cardsInHandCount != 7:
            raise ValueError ("get5CardCombosFrom7CardsForEval should only be called if there are 7 cards in the hand" )
        
        evalList = self.toEvalList()
        # Pick to cards to exclude and build list with rest of them
        for firstCardindex in range (0, cardsInHandCount):
            for secondCardIndex in range (firstCardindex+1, cardsInHandCount):
                fiveCardHand = []
                for cardIndex in range (0, cardsInHandCount):
                    if (cardIndex != firstCardindex and cardIndex != secondCardIndex):
                        fiveCardHand.append(evalList[cardIndex])
                result.append(fiveCardHand)
        return result
    
    # Get the best 5 cards of the hand as a list
    def getBest5CardHand(self):
        combos = self.get5CardCombosFrom7CardsForEval()
        winner = combos[0]
        for hand in combos:
            handEval = evaluation.evaluator.compare_hands(hand, winner)
            if handEval[0] == evaluation.evaluator.LEFT:
                winner = hand
        return winner

    
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
