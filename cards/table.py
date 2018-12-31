import uuid
from random import randint

class Table:
    
    def setDealerAtRandom(self):
        playerIndex = randint(0, len(self.players) -1)
        self.players[playerIndex].dealer = True
        for indexOut, player in enumerate(self.players):
            if (player.dealer):
                break
            
        # Set position 0 at dealer
        for index, player in enumerate(self.players):
            seq = index + indexOut
            if seq >= len(self.players):
                seq = seq -len(self.players)
            player.position = seq

    def dealPlayer(self, position):
        for player in self.players:
            if player.position == position:
                card = self.deck.deal()
                print(player.name + " got a " + str(card))
                player.hand.cards.append(card)
            

    def getDealer(self):
        for player in self.players:
            if (player.dealer):
                return player  
            
    def dealToTable(self, cardCount):
        
        for _ in range(cardCount):
            card = self.deck.deal()
            print('Table got a ' + str(card))
            self.cards.append(card)
                      

    def __init__(self):
        
        self.players = None
        self.id = uuid.uuid4()
        self.pot = 0
        self.deck = None
        self.cards = []
        
        