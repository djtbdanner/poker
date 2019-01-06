import uuid
from random import randint
from deck import Deck
from player import PlayerAction
import logging

class Table:
    
    def setDealerAtRandom(self):
        playerIndex = randint(0, len(self.players) -1)
        logging.debug(' Player index: {0} ({1}) randomly selected to be dealer.'.format( playerIndex, self.players[playerIndex].name))
        self.setDealerPosition(playerIndex)

    def setDealerPosition(self, playerIndxForDealer):
        '''
        Set the position of the dealer. Player that is dealer will be in index 0 of the array of players.
        '''
        self.players[playerIndxForDealer].dealer = True
        logging.info(' {0} is dealer.'.format( self.players[playerIndxForDealer].name))

        resetPlayers = []
        ### set dealer to index 0
        for index in range(len(self.players)):
            nextPlayer = playerIndxForDealer + index
            if nextPlayer >= len(self.players):
                nextPlayer = nextPlayer - len(self.players) 
            player = self.players[nextPlayer]
            player.dealer = playerIndxForDealer==nextPlayer
            resetPlayers.append(player)
            logging.debug('player ' + self.players[nextPlayer].name + ' is position ' + str(index))
        self.players = resetPlayers

    def dealPlayer(self, playerIndex):
        player = self.players[playerIndex]
        card = self.deck.deal()
        logging.debug(' {0} received a {1}'.format(player.name, card))
        player.hand.cards.append(card)

    def dealToTable(self, cardCount):
        for _ in range(cardCount):
            card = self.deck.deal()
            self.cards.append(card)
            
    def playerBet(self, playerIndex, chips):
        player = self.players[playerIndex]
        player.currentBet =  player.currentBet + chips
        logging.info(' {0} bets {1} chip(s), for a total of {2} this round'.format(player.name, chips, player.currentBet))
        if player.folded:
            logging.warn(player.name + " asked to bet, but is folded, bet will not be made")
            return
        player.chips = player.chips - chips
        player.currentAction = PlayerAction.CALL_CHECK_RAISE
        self.pot = self.pot + chips
        self.currentBet = player.currentBet
        logging.info(' Sets table pot to {0} and current call amount for this round to {1}'.format(self.pot,self.currentBet))
        
    def playerCheck(self, playerIndex):
        player = self.players[playerIndex]
        logging.info(' {0} checks'.format(player.name))
        if player.currentBet < self.currentBet:
            raise ValueError ('Cannot check without meeting the current bet')
        if player.folded:
            logging.warn(player.name + " asked to check, but is folded, bet will not be made")
            return
        player.currentAction = PlayerAction.CALL_CHECK_RAISE
        
    def playerFold(self, playerIndex):
        player = self.players[playerIndex]
        player.folded = True
        logging.info(' {0} folds, player has a total of {1} chips bet this round'.format(player.name, player.currentBet))

    def prepareForNextHand(self):
        '''
        Next dealer, reset pot, shuffle a new deck reset players
        '''
        indexOfDealer = 0
        for playerIndex, player in enumerate(self.players):
            player.hand.cards = []
            player.folded = False
            if player.dealer:
                indexOfDealer = playerIndex + 1
        
        self.setDealerPosition(indexOfDealer)
        self.prepareForNextRound()
        self.deck = Deck()
        self.deck.shuffle()
        self.pot = 0
        self.cards = []
        
    def prepareForNextRound(self):
        '''
        Reset players for the next round of betting
        '''        
        for player in (self.players):
            player.currentBet = 0
            player.currentAction = PlayerAction.NONE
        self.currentBet = 0


    def addPlayer(self, player):
        for existingPlayer in self.players:
            if existingPlayer.id == player.id:
                raise ValueError(" Cannot add player to table as player is already at table.")
        self.players.append(player)
        
    def isRoundComplete(self):
        '''
        Check to see that all bets are completed for the round of betting
        '''
        for player in self.players:
            if player.currentAction == PlayerAction.NONE and not player.folded:
                return False
            if player.currentAction == PlayerAction.CALL_CHECK_RAISE and player.currentBet < self.currentBet and not player.folded:
                return False
        return True


    def addPlayers (self, players):
        for player in players:
            self.addPlayer(player)

    def setBlinds(self):
        '''
        Set blinds or bets before table cards or betting. 
        Must have dealer set before this is called. Dealer will be index [0]
        '''
        self.playerBet(1, int(self.blind/2))
        self.playerBet(2, self.blind)
        # since this is blind, give the player a chance to call
        self.players[1].currentAction = PlayerAction.NONE
        self.players[2].currentAction = PlayerAction.NONE
        logging.info(' Blinds set, {0} is low at {1} chip(s) and {2} high with {3} chips '.format( self.players[1].name, int(self.blind/2), self.players[2].name, self.blind))

    def dealRound(self):
        numberOfPlayers = len(self.players)
        for playerIndex in range(1, numberOfPlayers+1):
            if playerIndex >= numberOfPlayers:
                playerIndex = 0
            self.dealPlayer(playerIndex)
            
    def showHand(self):
        myCards = "Table : "
        if len(self.cards) == 0:
            myCards += " No cards"
        else:
            for card in self.cards[:-1]:
                myCards  += str(card)
                myCards  +=  ", "
            myCards  +=  str(self.cards[-1])
        return myCards

    def __init__(self, pot = 0, blind = 2):
        
        self.players = []
        self.id = uuid.uuid4()
        self.pot = pot
        self.cards = []
        self.blind = blind
        self.currentBet = blind
        deck = Deck()
        deck.shuffle()  
        self.deck = deck 
        
        