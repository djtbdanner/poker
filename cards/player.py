import uuid
from deck import Card

class Hand:
    def __init__(self):    
        self.cards = []

    # list of cards is used for the evaluation of the hand, this will format for that process
    def toEvalList(self):
        '''
        Get cards as list of strings for evaluation
        '''
        result = []
        for card in self.cards:
            result.append(card.rank+card.suit)
        return result

    def setHandFromEvalList(self, evalList):
        self.cards = []
        for cardString in evalList:
            self.cards.append(Card.stringToCard(cardString))
    

    
class Player:
    def __init__(self, name="A Player with no name", chips=100, dealer=False, folded = False, currentBet = 0):
        self.hand = Hand()
        self.name = name  
        self.id=uuid.uuid4()
        self.chips = chips
        self.dealer = dealer
        self.folded = folded
        self.currentBet = currentBet
        self.currentAction = PlayerAction.NONE

    def showHand(self):
        myCards = self.name + ' : '
        if len(self.hand.cards) == 0:
            myCards += " No cards"
        else: 
            for card in self.hand.cards[:-1]:
                myCards  += str(card)
                myCards  +=  ", "
            myCards  += str(self.hand.cards[-1])
        return myCards

    
    def __str__(self):
        result = 'Player: {0} ({1}), {2} chip(s).'.format(self.name, self.id, self.chips)
        if self.dealer:
            result += ' DEALER '
        return result

from enum import Enum
class PlayerAction(Enum):
    NONE = 'none'
    CALL_CHECK_RAISE = 'call, check or raise'
    FOLD = 'fold'
