import uuid
from deck import Card

class Hand:
    def __init__(self, cards=None):    
        self.cards =  cards if cards is not None else []

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

class PlayerAction():
    NONE = 'none'
    CALL_CHECK_RAISE = 'call, check or raise'
    FOLD = 'fold'

class Player:
    def __init__(self, name="A Player with no name", hand = None, playerId = None,  chips=100, dealer=False, folded = False, currentBet = 0, currentAction=PlayerAction.NONE, turn=False):
        self.hand = hand if hand is not None else Hand()
        self.name = name  
        self.playerId=playerId if playerId is not None else str(uuid.uuid4())
        self.chips = chips
        self.dealer = dealer
        self.folded = folded
        self.currentBet = currentBet
        self.currentAction = currentAction
        self.turn = turn

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
        result = 'Player: {0} ({1}), {2} chip(s).'.format(self.name, self.playerId, self.chips)
        if self.dealer:
            result += ' DEALER '
        return result


