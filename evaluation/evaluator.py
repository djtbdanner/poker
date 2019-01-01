
from collections import Counter
'''
Code concept swiped from StackOverflow: https://stackoverflow.com/questions/5293405/algorithm-to-determine-the-winner-of-a-texas-holdem-hand/24481308
'''
ROYAL_FLUSH = ['ROYAL FLUSH',10]
STRAIGHT_FLUSH = ['STRAIGHT FLUSH',9]
FOUR_OF_A_KIND = ['FOUR OF A KIND',8]
FULL_HOUSE = ['FULL HOUSE',7]
FLUSH = ['FLUSH',6]
STRAIGHT = ['STRAIGHT',5]
THREE_OF_A_KIND = ['THREE OF A KIND',4]
TWO_PAIR = ['TWO_PAIR',3]
PAIR = ['PAIR',2]
HIGH_CARD = ['HIGH_CARD',1]
RIGHT = "RIGHT"
LEFT = "LEFT"
TIE = "TIE"
ALL_CARDS = ['2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH','AH','11H','12H','13H','14H','2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD','AD','11D','12D','13D','14D','2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS','AS','11S','12S','13S','14S','2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC','AC','11C','12C','13C','14C']

#Convert face cards and aces to numeric equivalent
def _convertRanksToNumeric(hand, nums = {'T':10, 'J':11, 'Q':12, 'K':13, "A": 14}):
    for x in range(len(hand)):
        if (hand[x][0]) in nums.keys():
            hand[x]=(str(nums[hand[x][0]]) + hand[x][1])
    return hand

def _isListSequential(mylist):
    for x in range(0,len(mylist)-1):
        if not mylist[x]+1 == mylist[x+1]:
            return False
    return True

def _stripSuitsSetRankToInt(handNumeric):
    handNumbersOnly = [x[:-1] for x in handNumeric]
    handIntNumeric = [int(x) for x in handNumbersOnly]
    return handIntNumeric

def _stripKeyCardsFromHand(aList, values):
    listCopy = aList.copy()
    for value in values:
        listCopy = list(filter(lambda x: x!= value, listCopy))
    return listCopy
    
def _isStraight(handIntNumeric):

    handIntNumeric.sort()
    if _isListSequential(handIntNumeric):
        return True
    ## See if there is A, 2, 3, 4, 5 (in above code ace is considered a 14)
    if handIntNumeric.count(14) == 1:
        handCopy = handIntNumeric.copy()
        for x in range(len(handCopy)):
            if handCopy[x] == 14:
                handCopy[x] = 1
        if max(handCopy) < 6:            
            handCopy.sort()
            if _isListSequential(handCopy):
                return True
    return False

def _isFlush(hand):
    suits = [x[-1] for x in hand]
    if len(set(suits)) == 1:
        return True
    else:
        return False

def _compare(leftHand, rightHand):
    '''
    Compare numeric hand ranks in reverse sorted order... first high wins
    Will fail if ranks are Strings.
    '''
    leftHand, rightHand = list(sorted(leftHand, reverse =True)), list(sorted(rightHand, reverse = True))
    for i, c in enumerate(leftHand):
        if rightHand[i] > c:
            return RIGHT
        elif rightHand[i] < c:
            return LEFT
    return TIE

# 
def _getHandCategory(hand):
    '''
    Analyze hand and determine category as Flush, straight, full house, three of a kind, etc.
    '''
    handNoSuitesNumericInt = _stripSuitsSetRankToInt(hand)
    isStraight = _isStraight(handNoSuitesNumericInt)
    isFlush = _isFlush(hand)

    counterData = Counter(handNoSuitesNumericInt)
    firstMostCommon = counterData.most_common(1)[0]
    nextMostCommon = counterData.most_common(2)[-1]
    keyCards = []
    
    if isStraight and isFlush:
        if min(handNoSuitesNumericInt) == 10:
            return ROYAL_FLUSH, handNoSuitesNumericInt, handNoSuitesNumericInt
        return STRAIGHT_FLUSH, handNoSuitesNumericInt, handNoSuitesNumericInt

    elif firstMostCommon[1] == 4:
        keyCards.append(firstMostCommon[0])
        return FOUR_OF_A_KIND, keyCards, handNoSuitesNumericInt
    
    elif firstMostCommon[1] == 3 and nextMostCommon[1] == 2:
        keyCards.append(firstMostCommon[0])
        keyCards.append(nextMostCommon[0])
        return FULL_HOUSE, keyCards, handNoSuitesNumericInt
    
    elif isFlush:
        return FLUSH, handNoSuitesNumericInt, handNoSuitesNumericInt
    
    elif isStraight:
        return STRAIGHT, handNoSuitesNumericInt, handNoSuitesNumericInt
    
    elif firstMostCommon[1] == 3:
        keyCards.append(firstMostCommon[0])
        return THREE_OF_A_KIND, keyCards, handNoSuitesNumericInt
    
    elif firstMostCommon[1] == 2 and nextMostCommon[1] == 2:
        keyCards.append(firstMostCommon[0])
        keyCards.append(nextMostCommon[0])
        return TWO_PAIR, keyCards, handNoSuitesNumericInt
    
    elif firstMostCommon[1] == 2:
        keyCards.append(firstMostCommon[0])       
        return PAIR, keyCards, handNoSuitesNumericInt
    
    else:
        return HIGH_CARD, handNoSuitesNumericInt, handNoSuitesNumericInt

def compare_hands(leftHand,rightHand):
    '''
    Compare hands for winner. Gets hand category and returns the winner. 
    If the category of both hands is the same, compares card values for highest value cards.
    Returns list: first element is LEFT, RIGHT, TIE, next is category of winning side, next is winning side hand (ties is left hand), next is losing category and hand 
    '''
    validate(leftHand)
    validate(rightHand)
    leftHandNumeric, rightHandNumeric  = _convertRanksToNumeric(leftHand.copy()), _convertRanksToNumeric(rightHand.copy())
    leftHandEval, rightHandEval = _getHandCategory(leftHandNumeric), _getHandCategory(rightHandNumeric)
    leftHandType, rightHandType = leftHandEval[0], rightHandEval[0] # Type of hand
    leftKeyCards, rightKeyCards = leftHandEval[1], rightHandEval[1] # Key cards as int (pair val, 3 of a kind val, etc.)
    leftHandCardInts, rightHandCardInts = leftHandEval[2], rightHandEval[2] # The whole hand as int representation of card

    winningHand = RIGHT # default
    if leftHandType == rightHandType:
        
        if leftHandType == FOUR_OF_A_KIND or leftHandType == THREE_OF_A_KIND or leftHandType == TWO_PAIR or leftHandType == PAIR:
            winningHand = _compare(leftKeyCards, rightKeyCards)
            if winningHand == TIE:
                leftHandLeftovers = _stripKeyCardsFromHand(leftHandCardInts, leftKeyCards)
                rightHandLeftovers = _stripKeyCardsFromHand(rightHandCardInts, rightKeyCards)
                winningHand = _compare(leftHandLeftovers, rightHandLeftovers)

        elif leftHandEval[0] == FULL_HOUSE:
            winningHand = _compare(leftKeyCards, rightKeyCards)
        ## High card, straight flush, flush, straight all will work here
        else:
            winningHand = _compare(leftHandCardInts, rightHandCardInts)
    elif leftHandType[1] > rightHandType[1]:
        winningHand = LEFT
        
    if winningHand == LEFT or winningHand == TIE:
        return winningHand, leftHandEval[0][0], leftHand, rightHandEval[0][0], rightHand
    else:
        return winningHand, rightHandEval[0][0], rightHand, leftHandEval[0][0], leftHand

def validate(hand):
    if len(hand) != 5:
        raise ValueError("Number of cards in hand must be 5 for poker.")
    for card in hand:
        if card not in ALL_CARDS:
            raise ValueError(card + " is not a known card from a poker deck.")
