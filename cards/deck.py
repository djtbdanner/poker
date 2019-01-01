import random
suits = ('H', 'D', 'S', 'C')
suitValues = {'H':'Hearts', 'D':'Diamonds', 'S':'Spades', 'C':'Clubs'}
suitfonts = {'H':'♥', 'D':'♦', 'S':'♠', 'C':'♣'}
ranks = ('2', '3','4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14')
rankValues = {'2':'Two', '3':'Three', '4':'Four', '5':'Five', '6':'Six', '7':'Seven', '8':'Eight', '9':'Nine', '10':'Ten', 'J':'Jack', 'Q':'Queen', 'K':'King', 'A':'Ace','11':'Jack', '12':'Queen', '13':'King', '14':'Ace'}

### Card
class Card:

    def __init__(self,rank,suit):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return rankValues[self.rank] + ' of ' + suitValues[self.suit]
    
    def cardForList(self):
        return self.rank + self.suit
    @staticmethod
    def stringToCard(s):
        if len(s) == 3:
            rank = s[0]+s[1]
            suit = s[2]
            return Card(rank, suit)
        return Card(s[0], s[1])

#### Deck of cards
class Deck:

    def __init__(self):
        self.cards = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank,suit))  # build Card objects and add them to the list
    
    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.cards:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp + '\n' + str(len(self.cards)) + ' cards left in deck'

    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self):
        if len(self.cards) < 1:
            raise ValueError ("The deck is empty, no more cards can be dealt.")
        single_card = self.cards.pop()
        return single_card
            
    
# deck = Deck()
# deck.shuffle()
# for x in range(0, 52):
#     card = deck.deal()
#     print("Card# %d" % (x+1) + " - " + str(card) +  " -  " + str(rankValues[card.rank])+ ' of ' +suitfonts[card.suit])

# deck = Deck()
# s = ""
# for card in deck.cards:
#     s = s + "'" + card.cardForList() + "',"
#     print(card.cardForList())
# print(s)
