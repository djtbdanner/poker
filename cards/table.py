import uuid
from random import randint
from deck import Deck
from player import PlayerAction
import logging
logger = logging.getLogger()

class Table:
    def __init__(self, players=None, deck = None, pot = 0,  cards=None, tableId=None, blind = 2, currentBet = 0, statusId=None, winners=None):
        self.players =  players if players is not None else []
        if deck is not None:
            self.deck = deck 
        else:
            self.deck = Deck()
            self.deck.shuffle()
        self.pot = pot
        self.cards = cards if cards is not None else []
        self.tableId = tableId if tableId is not None else str(uuid.uuid4())
        self.blind = blind
        self.currentBet = currentBet
        ## Any table change should update the status id this can then be used to determine if there has been a change on the table
        
        self.statusId = statusId if statusId is not None else 0
        self.winners = winners if winners is not None else []
        
    def setDealerAtRandom(self):
        playerIndex = randint(0, len(self.players) -1)
        logger.debug(' Player index: {0} ({1}) randomly selected to be dealer.'.format( playerIndex, self.players[playerIndex].name))
        self.setDealerPosition(playerIndex)
        self.statusId=self.statusId+1

    def setDealerPosition(self, playerIndxForDealer):
        '''
        Set the position of the dealer. Player that is dealer will be in index 0 of the array of players.
        '''
        self.players[playerIndxForDealer].dealer = True
        logger.info(' {0} is dealer.'.format( self.players[playerIndxForDealer].name))

        resetPlayers = []
        ### set dealer to index 0
        for index in range(len(self.players)):
            nextPlayer = playerIndxForDealer + index
            if nextPlayer >= len(self.players):
                nextPlayer = nextPlayer - len(self.players) 
            player = self.players[nextPlayer]
            player.dealer = playerIndxForDealer==nextPlayer
            resetPlayers.append(player)
            logger.info('player ' + self.players[nextPlayer].name + ' is position ' + str(index))
        self.players = resetPlayers
        self.setBlinds()
        self.statusId=self.statusId+1

    def dealPlayer(self, playerIndex):
        player = self.players[playerIndex]
        card = self.deck.deal()
        logger.info(' {0} received a {1}'.format(player.name, card))
        player.hand.cards.append(card)
        self.statusId=self.statusId+1

    def dealToTable(self, cardCount):
        for _ in range(cardCount):
            card = self.deck.deal()
            self.cards.append(card)
            logger.info(' Table received a {0}'.format(card))
            logger.info(' Table cards: {0}'.format(self.showHand()))
        self.statusId=self.statusId+1

    def playerBetOrCall(self, player, chips):
        logger.info('in bet or call recalling...' + str(player)  + " " + str(chips) + " " + str(len(self.players)))
        self.playerBetOrCallByIndex(self.players.index(player), chips)

    def playerBetOrCallByIndex(self, playerIndex, chips):
        logger.info('in bet or call')
        player = self.players[playerIndex]
        player.currentBet =  player.currentBet + chips
        logger.info(' {0} bets {1} chip(s), for a total of {2} this round'.format(player.name, chips, player.currentBet))
        if player.folded:
            logger.warn(player.name + " asked to bet or call, but is folded, bet will not be made")
            return
        logger.info('in bet or call 2')
        player.chips = player.chips - chips
        player.currentAction = PlayerAction.CALL_CHECK_RAISE
        self.pot = self.pot + chips
        self.currentBet = player.currentBet
        logger.info(' Sets table pot to {0} and current call amount for this round to {1}'.format(self.pot,self.currentBet))
        self.setNextPlayerTurn(player)
        logger.info('in bet or call done')
        self.statusId=self.statusId+1
    
    def playerCheck(self, player):
        self.playerCheckByIndex(self.players.index(player))
        
    def playerCheckByIndex(self, playerIndex):
        player = self.players[playerIndex]
        logger.info(' {0} checks'.format(player.name))
        if player.currentBet < self.currentBet:
            raise ValueError ('Cannot check without meeting the current bet')
        if player.folded:
            logger.warn(player.name + " asked to check, but is folded, bet will not be made")
            return
        player.currentAction = PlayerAction.CALL_CHECK_RAISE
        self.setNextPlayerTurn(player)
        self.statusId=self.statusId+1
 
    def setNextPlayerTurn(self, player):
        player.turn = False
        if self.isRoundComplete():
            pass
        else:
            playerIndex = self.players.index(player)
            nextPlayerIndex = self.getNextPlayerIndex(playerIndex)
            while self.players[nextPlayerIndex].folded:
                nextPlayerIndex = self.getNextPlayerIndex(nextPlayerIndex)
            self.players[nextPlayerIndex].turn = True
    
    def getNextPlayerIndex(self, playerIndex):
        playerIndex = playerIndex + 1
        if (playerIndex == len(self.players)):
            playerIndex = 0
        return playerIndex         

    def playerFold(self, player):
        self.playerFoldByIndex(self.players.index(player))
        
    def playerFoldByIndex(self, playerIndex):
        player = self.players[playerIndex]
        player.folded = True
        logger.info(' {0} folds, player has a total of {1} chips bet this round'.format(player.name, player.currentBet))
        self.statusId=self.statusId+1

    def prepareForNextHand(self):
        '''
        Next dealer, reset pot, shuffle a new deck reset players
        '''
        logger.info("Table is preparing for next hand")
        self.prepareForNextRound()
        self.deck = Deck()
        self.deck.shuffle()
        self.pot = 0
        self.cards = []
        self.winners = []
        
        indexOfDealer = 0
        for playerIndex, player in enumerate(self.players):
            player.hand.cards = []
            player.folded = False
            if player.dealer:
                indexOfDealer = self.getNextPlayerIndex(playerIndex)
        
        self.setDealerPosition(indexOfDealer)
        self.statusId=self.statusId+1

    def prepareForNextRound(self):
        '''
        Reset players for the next round of betting
        '''        
        logger.info("Table is preparing for next round")
        for player in (self.players):
            player.currentBet = 0
            player.currentAction = PlayerAction.NONE
        self.currentBet = 0
        self.statusId=self.statusId+1
        self.setNextPlayerTurn(self.players[0])# dealer is index 0

    def addPlayer(self, player):
        for existingPlayer in self.players:
            if existingPlayer.playerId == player.playerId:
                raise ValueError(" Cannot add player to table as player is already at table.")
        self.players.append(player)
        self.statusId=self.statusId+1
        
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

    def isHandComplete (self):
        if self.isRoundComplete():
            if len(self.cards) == 5:
                return True
        return False

    def addPlayers (self, players):
        for player in players:
            self.addPlayer(player)
            
    def removePlayer(self, player):
        if player in self.players:
            self.players.remove(player)
            
    def removePlayerById(self, playerId):
        for player in self.players:
            if player.playerId == playerId:
                self.players.remove(player)

    def setBlinds(self):
        '''
        Set blinds or bets before table cards or betting. 
        Must have dealer set before this is called. Dealer will be index [0]
        '''
        firstBlindIndex = 1
        secondBlindIndex = self.getNextPlayerIndex(1)
        self.playerBetOrCallByIndex(firstBlindIndex, int(self.blind/2))
        self.playerBetOrCallByIndex(secondBlindIndex, self.blind)
        # since this is blind, give the player a chance to call
        self.players[firstBlindIndex].currentAction = PlayerAction.NONE
        self.players[secondBlindIndex].currentAction = PlayerAction.NONE
        self.setNextPlayerTurn( self.players[secondBlindIndex])
        logger.info(' Blinds set, {0} is low at {1} chip(s) and {2} high with {3} chips '.format( self.players[1].name, int(self.blind/2), self.players[2].name, self.blind))

    def dealRound(self):
        numberOfPlayers = len(self.players)
        for playerIndex in range(1, numberOfPlayers+1):
            if playerIndex >= numberOfPlayers:
                playerIndex = 0
            self.dealPlayer(playerIndex)
        self.statusId=self.statusId+1
     
    def doAllPlayersHaveTwoCards(self):
        for player in self.players:
            if len(player.hand.cards) < 2:
                return False
        return True   

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
    
    def hasDealer(self):
        for player in self.players:
            if player.dealer:
                return True
        return False
