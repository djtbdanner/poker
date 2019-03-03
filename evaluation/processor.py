import evaluation.evaluator
from player import Hand
import logging
logger = logging.getLogger()



def getBest5CardHand(hand):
    '''
    Get best hand from hand of 7 card objects
    Ties are ignored
    '''
    hands = get5CardCombosFrom7CardsForEval(hand)

    winner = hands[0]
    for hand in hands:
        handEval = evaluation.evaluator.compare_hands(hand, winner)
        if handEval[0] == evaluation.evaluator.LEFT:
            winner = hand
    return winner

def getBest5CardsAsHand(hand):
    '''
    Get best hand from hand of 7 card objects return hand object
    '''
    bestCards = getBest5CardHand(hand)
    bestHand = Hand()
    bestHand.setHandFromEvalList(bestCards)
    return bestHand


# Build all 5 card combinations of the 7  cards in the player's hand
# (At this time will not work for numbers in hand other than 7)
def get5CardCombosFrom7CardsForEval(hand):
    cards = hand.toEvalList()
    result = []
    cardsInHandCount = len(cards)
    if cardsInHandCount != 7:
        raise ValueError ("get5CardCombosFrom7CardsForEval should only be called if there are 7 cards in the hand" )
    
    # Pick to cards to exclude and build list with rest of them
    for firstCardindex in range (0, cardsInHandCount):
        for secondCardIndex in range (firstCardindex+1, cardsInHandCount):
            fiveCardHand = []
            for cardIndex in range (0, cardsInHandCount):
                if (cardIndex != firstCardindex and cardIndex != secondCardIndex):
                    fiveCardHand.append(cards[cardIndex])
            result.append(fiveCardHand)
    return result

def getWinners(table):
    
    logger.debug(" Checking for Winners : " + str(table)) 
    winnerList = []
    if table.haveAllButOnePlayerFolded():
        logger.info(" Player will win by default because all others folded.") 
        for player in table.players:
            if not player.folded:
                winnerList.append(player)
                return winnerList;
    
    players = []
    for player in table.players:
        if player.folded:
            logger.info(" Player folded will not be a winner : " + str(player)) 
        else:
            player.hand.cards.extend(table.cards)
            logger.info("Player; {0}, Hand: before best 5: {1} ".format(player.name, player.showHand()))   
            player.hand = evaluation.processor.getBest5CardsAsHand(player.hand)
            logger.info("Player; {0}, Hand: after best 5: {1} ".format(player.name, player.showHand()))   
            players.append(player)


    winnerList.append(players[0])
    for player in players:
        if player not in winnerList and not player.folded:
            leftHand = player.hand.toEvalList()
            currentWinnerHand = winnerList[0].hand.toEvalList()
            result = evaluation.evaluator.compare_hands(leftHand, currentWinnerHand)
            logger.info(" Evaluation result for winning hand: " + str(result))
            if evaluation.evaluator.LEFT == result[0]:
                winnerList.clear()
                winnerList.append(player)
            elif evaluation.evaluator.TIE == result[0]:
                winnerList.append(player)
    logger.info("Winners: " + str(winnerList))
    return winnerList
