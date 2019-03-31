import logging
import unittest
from db import datalayer
from evaluation import playProcessor
from player import Player
import sys, traceback
import time
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
            player4 = datalayer.getOrCreateSavedPlayer("x", "player four")
            table = datalayer.findATableForPlayer(player4) 
            
            currentStatusId = table.statusId
            
            for player in table.players: 
                playProcessor.checkForUpdates(table, player, currentStatusId)
            
            if table.statusId != currentStatusId:
                tableCards = 0;
                while not tableCards == 5: #isHandComplete (processes on own)
                    playedCount = 0
                    while playedCount < len(table.players): ## is round complete
                        for player in table.players:
                            if player.turn:
                                myBet = table.currentBet - player.currentBet 
                                playProcessor.makePlay(player, table, 'bet', myBet, table.statusId)
                                playedCount = playedCount + 1
                                # the processor will automatically reset this above, so we need to fake this out to test 
                                if len(table.cards) > 0:
                                    tableCards = len(table.cards)
                                break
     
            self.assertEquals(len(table.cards), 5)
            if (len(table.winners) == 1):
                assert(table.winners[0].chips, 104)
            for player in table.winners:
                print (str(player) + " wins ")
            self.assertTrue(len(table.winners)>0)
                
            table.prepareForNextHand()
            playerTurnCount = 0
            for player in table.players:
                if player.turn:
                    playerTurnCount = playerTurnCount + 1
            self.assertEqual(playerTurnCount, 1)

        except Exception as error:
            print("Unable to test." + str(error))
            print ('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print ('-' * 60)
            
        finally:       
            datalayer.deleteTable(table)
        


    def test_player_evicted_after_timout (self):
        try:
            table = datalayer.getOrCreateSavedTable("x")
            player1 = datalayer.getOrCreateSavedPlayer("x", "player one")
            table = datalayer.findATableForPlayer(player1)
            player2 = datalayer.getOrCreateSavedPlayer("x", "player two")
            table = datalayer.findATableForPlayer(player2)
            player3 = datalayer.getOrCreateSavedPlayer("x", "player three")
            table = datalayer.findATableForPlayer(player3) 
            player4 = datalayer.getOrCreateSavedPlayer("x", "player four")
            table = datalayer.findATableForPlayer(player4) 
            
            currentStatusId = table.statusId
            
            self.assertEqual(4, len(table.players))
            for player in table.players: 
                playProcessor.checkForUpdates(table, player, currentStatusId)
           
            logging.log(logging.INFO, "Waiting 5 seconds to see if player is automatically evicted")
            table.PLAYER_TURN_LIMIT = 5 # 5 seconds
            time.sleep(6)
            
            playProcessor.checkForUpdates(table, player, currentStatusId)
            self.assertEqual(3, len(table.players))
            
                
        except Exception as error:
            print("Unable to test." + str(error))
            print ('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print ('-' * 60)
            
        finally:       
            datalayer.deleteTable(table)        

def buildPlayers(count):
    players = []
    for indx in range (1, count + 1):
        players.append(Player("player " + str(indx)))
    return players
