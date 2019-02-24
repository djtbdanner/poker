import unittest
from table import Table
import evaluation.processor
import logging
from player import Player, PlayerAction
logging.basicConfig(level=logging.DEBUG)

class PlayAGame(unittest.TestCase):
    


    def test_playAGame(self):
        table = Table()
#         table.players = testFunctions.buildPlayers(23)
        table.players = buildPlayers(5)

        table.setDealerAtRandom()  

        for _ in range(100):
            playAHand(table)
            table.prepareForNextHand()

def playAHand(table):
        
        for player in table.players:
            print(player)
    
        table.setBlinds()
        print('---- blinds set')

        table.dealRound()
        table.dealRound()
        
        seekBets(3, table)
        table.prepareForNextRound()

        logging.debug('\n--- flop ---\n ')
        table.dealToTable(3)
        seekBets(1, table)
        table.prepareForNextRound()
        logging.debug ('\n--- turn ---\n')
        table.dealToTable(1)
        seekBets(1, table)
        table.prepareForNextRound()
        logging.debug('\n--- river ---\n')
        table.dealToTable(1)
        seekBets(1, table)
        table.prepareForNextRound()

        winnerList =  evaluation.processor.getWinners(table)
        logging.debug("\n-------------- " + str(len(winnerList)) + " winner(s)! ------------\n" )
        for player in winnerList:
            logging.debug("Winner: {0} ".format(player.showHand()))
            player.chips = player.chips + int(table.pot/len(winnerList))
            
        for player in table.players:
            logging.debug(' {0} has {1} chips '.format(player.name, player.chips))

def seekBets(firstPlayerIndex, table):
        
    while not table.isRoundComplete():
        for index in range(firstPlayerIndex, len(table.players) + firstPlayerIndex):
            if index >= len(table.players):
                index = index - len(table.players)
            
            player = table.players[index]
            
            if player.folded:
                logging.debug(' {0} folded - no bet for this player'.format(player.name))
                continue
            if player.currentAction == PlayerAction.CALL_CHECK_RAISE and player.currentBet == table.currentBet:
                logging.debug(' {0} called and no raises - no bet for this player'.format(player.name))
                continue
            logging.debug('  {0} - {1}'.format(player.showHand(), table.showHand()))
            val = 'c'
            if val == 'c':
                logging.debug(' {0} calls or checks {1}'.format(player.name, table.currentBet - player.currentBet))
                table.playerBetOrCallByIndex(index, table.currentBet - player.currentBet)
            elif val == 'f':
                table.playerFoldByIndex(index)
            else:
                table.playerBetOrCallByIndex(index, int(val))

def buildPlayers(count):
    players = []
    for indx in range (1, count + 1):
        players.append(Player("player " + str(indx)))
    return players

if __name__ == '__main__':
    unittest.main()

