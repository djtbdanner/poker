import unittest
import logging
from player import Hand, Player, PlayerAction
from deck import Deck
from table import Table
import db.jsonobj as jsob
import json


class TestJSON(unittest.TestCase):
    
#     def test_hand(self):
#         hand = buildHand(7)
#         print(hand)
#         
#         jsondata = json.dumps(hand,default=jsob.convert_to_dict,indent=4, sort_keys=True)
#         print(jsondata)
#         newHand = json.loads(jsondata, object_hook=jsob.dict_to_obj)
#         
#         logging.debug("comparing " + str (hand.cards[0]) + " and "+ str(newHand.cards[0]))
#         self.assertEqual(hand.cards[0], newHand.cards[0])
#         self.assertEqual(hand.cards[1], newHand.cards[1])
#         self.assertEqual(hand.cards[2], newHand.cards[2])
#         self.assertEqual(hand.cards[3], newHand.cards[3])
#         self.assertEqual(hand.cards[4], newHand.cards[4])
#         self.assertEqual(hand.cards[5], newHand.cards[5])
#         self.assertEqual(hand.cards[6], newHand.cards[6])
#         self.assertNotEqual(hand.cards[0], newHand.cards[4])
#  
# 
    def test_player(self):
        player = Player("Test Player", buildHand(7), 'unique_id', 100, True, False, 9, 'z')
        jsondata = json.dumps(player,default=jsob.convert_to_dict,indent=4, sort_keys=True)
        print(jsondata)
        playerII = json.loads(jsondata, object_hook=jsob.dict_to_obj)
        self.assertEqual(player.playerId, playerII.playerId)
        self.assertEqual(player.name, playerII.name)
        self.assertEqual(player.chips, playerII.chips)
        self.assertEqual(player.currentBet, playerII.currentBet)
        self.assertEqual(player.folded, playerII.folded)
        self.assertEqual(player.currentAction, playerII.currentAction)
        self.assertEqual(player.hand.cards[0], playerII.hand.cards[0])   
#         
    def test_table(self):
        table = Table();
        table.addPlayer(Player("Test Player 1", buildHand(7), 'unique_id1', 100, True, False, 9, PlayerAction.CALL_CHECK_RAISE))
        table.addPlayer(Player("Test Player 2", buildHand(7), 'unique_id2', 78, False, False, 10, 'z'))
        table.addPlayer(Player("Test Player 3", buildHand(7), 'unique_id3', 16, False, True, 11, 'z'))
        table.addPlayer(Player("Test Player 4", buildHand(7), 'unique_id4', 250, False, True, 11, 'z'))
        table.pot = 25
        table.cards.append(table.deck.deal());
        table.blind = 4
        jsondata = json.dumps(table,default=jsob.convert_to_dict,indent=4, sort_keys=True)
        print(jsondata)
        tableII = json.loads(jsondata, object_hook=jsob.dict_to_obj)
        
        self.assertEqual(table.players[0].name, tableII.players[0].name)
        self.assertEqual(table.cards[0],  tableII.cards[0])
        self.assertEqual(table.pot, tableII.pot)
        self.assertEqual(table.currentBet, tableII.currentBet)


def buildHand(howMany):
    deck = Deck()
    deck.shuffle()
    hand = Hand()
    for _ in range (0, howMany):
        hand.cards.append(deck.deal())
    return hand

