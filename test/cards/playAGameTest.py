import unittest
from deck import Deck
from table import Table
import testFunctions
import evaluation.evaluator


class PlayAHand(unittest.TestCase):
    def test_playAGame(self):
        table = Table()
        table.players = testFunctions.buildPlayers(23)
        
        deck = Deck()
        deck.shuffle()  
        table.deck = deck    
        
        table.setDealerAtRandom()  
#         print("Dealer: " + table.getDealer().name)
        
        for int in range(len(table.players)):
            table.dealPlayer(int)
        for int in range(len(table.players)):
            table.dealPlayer(int)  

        
        for player in table.players:
            player.showHand()   
        
        print("--- flop")
        table.dealToTable(3)
        print("--- turn")
        table.dealToTable(1)
        print("--- river")
        table.dealToTable(1)
        
        for player in table.players:
            player.hand.cards.extend(table.cards)
        
        # set the best 5 cards of 7 for player
        for player in table.players:
            player.showHand()   
            player.hand.cards = player.hand.bestHandAsCards()
            player.showHand()
    
        winnerList = [table.players[0]]
        for player in table.players:
            if player not in winnerList:
                leftHand = player.hand.toEvalList()
                currentWinnerHand = winnerList[0].hand.toEvalList()
                result = evaluation.evaluator.compare_hands(leftHand, currentWinnerHand)
                print(result)
                if evaluation.evaluator.LEFT == result[0]:
                    winnerList.clear()
                    winnerList.append(player)
                elif evaluation.evaluator.TIE == result[0]:
                    winnerList.append(player)
#                  if evaluation.evaluator.leftIsGreaterOrEqual(handA, handB):
#                     if evaluation.evaluator.isEqual(handA, handB):
#                         winnerList.append(player)
#                     else:
#                         winnerList.clear()
#                         winnerList.append(player)
#         
        
        print("-------------- " + str(len(winnerList)) + " winner(s)! ------------" )
        for player in winnerList:
            print("Winner: " + player.name)
            print(player.showHand())


if __name__ == '__main__':
    unittest.main()


