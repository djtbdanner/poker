from collections import Counter

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
ALL_CARDS_FOR_VALIDATION = ['2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH','AH','11H','12H','13H','14H','2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD','AD','11D','12D','13D','14D','2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS','AS','11S','12S','13S','14S','2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC','AC','11C','12C','13C','14C']
CARD_RANK_NUMS = {'T':'10', 'J':'11', 'Q':'12', 'K':'13', 'A': '14'}
#Convert face cards and aces to numeric equivalent
def _convertCardRanksToNumeric(hand):
    
    handStrNumeric = hand.copy()
    for x in range(len(handStrNumeric)):
        if (handStrNumeric[x][0]) in CARD_RANK_NUMS.keys():
            handStrNumeric[x]=(str(CARD_RANK_NUMS[handStrNumeric[x][0]]) + handStrNumeric[x][1])
            
    handNumbersOnly = [x[:-1] for x in handStrNumeric]
    return [int(x) for x in handNumbersOnly]

def _isListSequential(mylist):
    
    for x in range(0,len(mylist)-1):
        if not mylist[x]+1 == mylist[x+1]:
            return False
    return True

def _stripKeyCardsFromHand(aList, values):
    
    listCopy = aList.copy()
    for value in values:
        listCopy = list(filter(lambda x: x!= value, listCopy))
    return listCopy
    
def _isStraight(handIntNumeric):
    
    handRanks = handIntNumeric.copy()
    handRanks.sort()
    if _isListSequential(handRanks):
        return True
    ## See if there is A, 2, 3, 4, 5 (in above code ace is considered a 14)
    if handRanks.count(14) == 1:
        for x in range(len(handRanks)):
            if handRanks[x] == 14:
                handRanks[x] = 1
        handRanks.sort()
        return _isListSequential(handRanks)
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

def _getHandCategory(hand, handNoSuitesNumericInt):
    '''
    Analyze hand and determine category as Flush, straight, full house, three of a kind, etc.
    Returns category, key cards (i.e. pair values if pairs, three of a kind value, etc. if not pair or other duplicate card hand, key cards will be all cards)
    '''
    isStraight = _isStraight(handNoSuitesNumericInt)
    isFlush = len(set([x[-1] for x in hand])) == 1# set of all suits is 1, it is a flush
    counterData = Counter(handNoSuitesNumericInt)
    firstMostCommon = counterData.most_common(1)[0]
    nextMostCommon = counterData.most_common(2)[-1]
    keyCards = []
    
    if isStraight and isFlush:
        if min(handNoSuitesNumericInt) == 10:
            return ROYAL_FLUSH, handNoSuitesNumericInt
        return STRAIGHT_FLUSH, handNoSuitesNumericInt

    elif firstMostCommon[1] == 4:
        keyCards.append(firstMostCommon[0])
        return FOUR_OF_A_KIND, keyCards
    
    elif firstMostCommon[1] == 3 and nextMostCommon[1] == 2:
        keyCards.append(firstMostCommon[0])
        keyCards.append(nextMostCommon[0])
        return FULL_HOUSE, keyCards
    
    elif isFlush:
        return FLUSH, handNoSuitesNumericInt
    
    elif isStraight:
        return STRAIGHT, handNoSuitesNumericInt
    
    elif firstMostCommon[1] == 3:
        keyCards.append(firstMostCommon[0])
        return THREE_OF_A_KIND, keyCards
    
    elif firstMostCommon[1] == 2 and nextMostCommon[1] == 2:
        keyCards.append(firstMostCommon[0])
        keyCards.append(nextMostCommon[0])
        return TWO_PAIR, keyCards
    
    elif firstMostCommon[1] == 2:
        keyCards.append(firstMostCommon[0])       
        return PAIR, keyCards
    
    else:
        return HIGH_CARD, handNoSuitesNumericInt
    
def _validate(hand):
    if len(hand) != 5:
        raise ValueError("Number of cards in hand must be 5 for poker.")
    for card in hand:
        if card not in ALL_CARDS_FOR_VALIDATION:
            raise ValueError(card + " is not a known card from a poker deck.")

def compare_hands(leftHand, rightHand):
    '''
    Compare hands for winner. Gets hand category and returns the winner. 
    If the category of both hands is the same, compares card values for highest value cards. If key (three of a kind, pairs, etc) cards are tie, and there are 
    leftover cards, the left overs are compared to determine a winner
    Returns tuple: first element is LEFT, RIGHT, TIE (to indicate winner), next is category of winning side, next is winning side hand (ties are left  hand), next is losing category and hand 
    '''
    _validate(leftHand)
    _validate(rightHand)
    leftHandNumeric, rightHandNumeric  = _convertCardRanksToNumeric(leftHand), _convertCardRanksToNumeric(rightHand)
    leftHandEval, rightHandEval = _getHandCategory(leftHand, leftHandNumeric), _getHandCategory(rightHand, rightHandNumeric)
    leftHandCategory, rightHandCategory = leftHandEval[0], rightHandEval[0] # Type of hand

    winningHand = RIGHT # default
    if leftHandCategory == rightHandCategory:
        leftKeyCards, rightKeyCards = leftHandEval[1], rightHandEval[1] # Key cards as int (pair val, 3 of a kind val, etc.)
        winningHand = _compare(leftKeyCards, rightKeyCards)
        if winningHand == TIE and leftHandNumeric != leftKeyCards: # if key cards are all cards, no need to analyze further
            leftHandLeftovers = _stripKeyCardsFromHand(leftHandNumeric, leftKeyCards)
            rightHandLeftovers = _stripKeyCardsFromHand(rightHandNumeric, rightKeyCards)
            winningHand = _compare(leftHandLeftovers, rightHandLeftovers)

    elif leftHandCategory[1] > rightHandCategory[1]:
        winningHand = LEFT
        
    if winningHand == LEFT or winningHand == TIE:
        return (winningHand, leftHandEval[0][0], leftHand, rightHandEval[0][0], rightHand)
    else:
        return (winningHand, rightHandEval[0][0], rightHand, leftHandEval[0][0], leftHand)