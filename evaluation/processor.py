import evaluation.evaluator
import logging
from player import Hand

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

def getWinners(players):
    
    winnerList = []
    winnerList.append(players[0])
    for player in players:
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
