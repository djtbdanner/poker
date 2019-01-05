import unittest
from table import Table
import testFunctions
import evaluation.evaluator
import logging
from player import PlayerAction

class PlayAGame(unittest.TestCase):
    
    logging.basicConfig(level=logging.DEBUG)
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
            
            inputString = player.showHand()
            inputString += '\n'
            inputString += table.showHand()
            inputString += '\n'
            if table.currentBet == 0:
                inputString += '{0}, {1} chips to you (you have already bet {2}); check (c), raise (amount), or fold (f)? : '.format(player.name, table.currentBet, player.currentBet)
                val = input (inputString)
            else :
                inputString += ' {0}, {1} chips to you (you have already bet {2} so a call would add {3} chip(s) for this round); call (c), raise (amount), or fold (f)? : '.format(player.name, table.currentBet, player.currentBet, (table.currentBet-player.currentBet))
                val = input (inputString)
            
            
            if val != 'c' and val != 'f':
                try:
                    bet = int(val)
                except:
                    logging.info ("Looks like {0} is not a number or 'c' or 'f'. It will be set to the default of 'c' for check or call".format(val))
                    val = 'c'

            if val == 'c':
                table.playerBet(index, table.currentBet - player.currentBet)
            elif val == 'f':
                table.playerFold(index)
            else:
                table.playerBet(index, int(val))
            
def getWinners(table):
    winnerList = []
    winnerList.append(table.players[0])
    for player in table.players:
        if player not in winnerList and not player.folded:
            leftHand = player.hand.toEvalList()
            currentWinnerHand = winnerList[0].hand.toEvalList()
            result = evaluation.evaluator.compare_hands(leftHand, currentWinnerHand)
            logging.info(" Evaluation result for winning hand: " + str(result))
            if evaluation.evaluator.LEFT == result[0]:
                winnerList.clear()
                winnerList.append(player)
            elif evaluation.evaluator.TIE == result[0]:
                winnerList.append(player)
    return winnerList

def playAHand(table):
        
        for player in table.players:
            logging.info(player)
    
        table.setBlinds()

        table.dealRound()
        table.dealRound()
        
        seekBets(3, table)
        table.prepareForNextRound()

        print("--- flop")
        table.dealToTable(3)
        seekBets(1, table)
        table.prepareForNextRound()
        print("--- turn")
        table.dealToTable(1)
        seekBets(1, table)
        table.prepareForNextRound()
        print("--- river")
        table.dealToTable(1)
        seekBets(1, table)
        table.prepareForNextRound()
        
        for player in table.players:
            player.hand.cards.extend(table.cards)
        # set the best 5 cards of 7 for player
        for player in table.players:
            player.showHand()   
            player.hand.cards = player.hand.bestHandAsCards()
            player.showHand()

        winnerList = getWinners(table)
        logging.info("-------------- " + str(len(winnerList)) + " winner(s)! ------------" )
        for player in winnerList:
            logging.info("Winner: " + player.name)
            logging.info(player.showHand())
            player.chips = player.chips + int(table.pot/len(winnerList))

if __name__ == '__main__':
    unittest.main()


