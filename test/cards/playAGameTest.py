import unittest
from table import Table
import testFunctions
import evaluation.processor
import logging
from player import PlayerAction

class PlayAGame(unittest.TestCase):
    
    logging.basicConfig(level=logging.ERROR)
    def test_playAGame(self):
        table = Table()
#         table.players = testFunctions.buildPlayers(23)
        table.players = testFunctions.buildPlayers(5)

        table.setDealerAtRandom()  

        for _ in range(10):
            playAHand(table)
            table.prepareForNextHand()

def seekBets(firstPlayerIndex, table):
        
    while not table.isRoundComplete():
        for index in range(firstPlayerIndex, len(table.players) + firstPlayerIndex):
            if index >= len(table.players):
                index = index - len(table.players)
            
            player = table.players[index]
            
            if player.folded:
                print(' {0} folded - no bet for this player'.format(player.name))
                continue
            if player.currentAction == PlayerAction.CALL_CHECK_RAISE and player.currentBet == table.currentBet:
                print(' {0} called and no raises - no bet for this player'.format(player.name))
                continue
            inputString = '===============================\n'
            inputString += player.showHand()
            inputString += '\n'
            inputString += table.showHand()
            inputString += '\n'
            inputString += 'Pot is {} chip(s).'.format(table.pot)
            inputString += '\n'
            if table.currentBet == 0:
                inputString += '{0} chips to you (you have already bet {1}); check (c), raise (amount), or fold (f)? : '.format(table.currentBet, player.currentBet)
                val = input (inputString)
            else :
                inputString += '{0} chips to you (you have already bet {1} so a call would add {2} chip(s) for this round); call (c), raise (amount), or fold (f)? : '.format(table.currentBet, player.currentBet, (table.currentBet-player.currentBet))
                val = input (inputString)
            
            
            if val != 'c' and val != 'f':
                try:
                    int(val)
                except:
                    logging.info ("Looks like {0} is not a number or 'c' or 'f'. It will be set to the default of 'c' for check or call".format(val))
                    val = 'c'

            if val == 'c':
                table.playerBet(index, table.currentBet - player.currentBet)
            elif val == 'f':
                table.playerFold(index)
            else:
                table.playerBet(index, int(val))
            
def playAHand(table):
        
        for player in table.players:
            print(player)
    
        table.setBlinds()
        print('---- blinds set')

        table.dealRound()
        table.dealRound()
        
        seekBets(3, table)
        table.prepareForNextRound()

        print('\n--- flop ---\n ')
        table.dealToTable(3)
        seekBets(1, table)
        table.prepareForNextRound()
        print ('\n--- turn ---\n')
        table.dealToTable(1)
        seekBets(1, table)
        table.prepareForNextRound()
        print('\n--- river ---\n')
        table.dealToTable(1)
        seekBets(1, table)
        table.prepareForNextRound()
        
        for player in table.players:
            player.hand.cards.extend(table.cards)
            player.showHand()   
            player.hand = evaluation.processor.getBest5CardsAsHand(player.hand)
            player.showHand()

        winnerList =  evaluation.processor.getWinners(table.players)
        print("\n-------------- " + str(len(winnerList)) + " winner(s)! ------------\n" )
        for player in winnerList:
            print("Winner: " + player.name)
            logging.info(player.showHand())
            player.chips = player.chips + int(table.pot/len(winnerList))

if __name__ == '__main__':
    unittest.main()


