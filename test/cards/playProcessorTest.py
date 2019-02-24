import logging
import unittest
from db import datalayer
from evaluation import playProcessor
from player import Player
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


class TestPlay(unittest.TestCase):
    
    logging.basicConfig(level=logging.ERROR)
    def test_play_a_Round_via_processor(self):
        '''
        Attempt to simulate several browsers asking for data and processing
        '''
        try:
            table = datalayer.getOrCreateSavedTable("x")
            player1 = datalayer.getOrCreateSavedPlayer("x", "player one")
            table = datalayer.findATableForPlayer(player1)
            player2 = datalayer.getOrCreateSavedPlayer("x", "player two")
            table = datalayer.findATableForPlayer(player2)
            player3 = datalayer.getOrCreateSavedPlayer("x", "player three")
            table = datalayer.findATableForPlayer(player3) 
            
            currentStatusId = table.statusId
            
            for player in table.players:
                playProcessor.checkForUpdates(table, player, currentStatusId)
            
            if table.statusId != currentStatusId:
                while not table.isHandComplete():
                    while not table.isRoundComplete():
                        for player in table.players:
                            if player.turn:
                                ## just check
                                myBet = table.currentBet - player.currentBet 
                                playProcessor.makePlay(player, table, 'bet', myBet, table.statusId)
                                break
     
            self.assertEquals(len(table.cards), 5)
            if (len(table.winners) == 1):
                assert(table.winners[0].chips, 104)
            for player in table.winners:
                print (str(player) + " wins ")
            self.assertTrue(len(table.winners)>0)
                
            table.prepareForNextHand()
            

        except Exception as error:
            print("Unable to test." + str(error))
            
        finally:       
            datalayer.deleteTable(table)
        

def buildPlayers(count):
    players = []
    for indx in range (1, count + 1):
        players.append(Player("player " + str(indx)))
    return players
