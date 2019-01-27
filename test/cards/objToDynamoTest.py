### for a bug in the boto database stuff
import os
os.environ["TZ"] = "UTC"  

import unittest
import db.jsonobj as jsob
import json
import db.tableCreateDelete
from player import Player, Hand, PlayerAction
from deck import Deck
from table import Table

import logging


class TestJSONtoDynamoDb(unittest.TestCase):
    
    logging.basicConfig(level=logging.INFO)
    
    
    def setUp(self):
        pass
#         logging.info("Making sure table is TestPlayerTable and TestPokerTable are created. ")
#         db.tableCreateDelete.createATable('TestPlayerTable', 'playerId')
#         db.tableCreateDelete.createATable('TestPokerTable', 'tableId')
#         logging.info("Both TestPokerPlayer and TestPokerTable are created. ")

    def tearDown(self):
        pass
#         logging.info("Making sure table is TestPokerPlayer and TestPokerTable are deleted. ")
#         db.tableCreateDelete.deleteATable('TestPlayerTable')
#         db.tableCreateDelete.deleteATable('TestPokerTable')
#         logging.info("Both TestPokerPlayer and TestPokerTable are deleted. ")
# 
    def test_player(self):
        player = Player("Test Player", buildHand(7))
        jsondata = json.dumps(player,default=jsob.convert_to_dict,indent=None, sort_keys=False)
        logging.info("From Object: " + jsondata)
#         
#         db.tableCreateDelete.createATable(dbTableName, 'playerId')
        playerTable = db.tableCreateDelete.dynamodb.Table("TestPlayerTable")
        playerTable.put_item(
            Item={
                 'playerId': player.playerId,
                 'player': jsondata
             }
        )
#         
        response = playerTable.get_item(        
            Key={
                'playerId': player.playerId
                }
        )
        playerJsonFromDB = response['Item']['player']
        logging.info("From Database: " + playerJsonFromDB)
        playerII = json.loads(playerJsonFromDB, object_hook=jsob.dict_to_obj)
         
        print(playerII)

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
        table.addPlayer(Player("Test Player 2", buildHand(7), 'unique_id2', 78, False, False, 10, PlayerAction.NONE))
        table.addPlayer(Player("Test Player 3", buildHand(7), 'unique_id3', 16, False, True, 11, PlayerAction.NONE))
        table.addPlayer(Player("Test Player 4", buildHand(7), 'unique_id4', 250, False, True, 11, PlayerAction.NONE))
        table.pot = 25
        table.cards.append(table.deck.deal());
        table.blind = 4
        jsondata = json.dumps(table,default=jsob.convert_to_dict,indent=None, sort_keys=False)
        logging.info("From Object: " + jsondata)

        playerTable = db.tableCreateDelete.dynamodb.Table("TestPokerTable")
        playerTable.put_item(
            Item={
                 'tableId': table.tableId,
                 'table': jsondata
             }
        )
#         
        response = playerTable.get_item(        
            Key={
                'tableId': table.tableId
                }
        )
        playerJsonFromDB = response['Item']['table']
        logging.info("From Database: " + playerJsonFromDB)

        tableII = json.loads(playerJsonFromDB, object_hook=jsob.dict_to_obj)
         
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

