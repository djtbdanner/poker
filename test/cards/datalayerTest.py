import unittest
import db.datalayer as datalayer
# from deck import Deck, Card
from player import Hand, Player
from deck import Deck
import logging
import string
import random

class TestDataLayer(unittest.TestCase):
    
    logging.basicConfig(level=logging.DEBUG)
    def test_getPlayer(self):
        playerRandomName = "Test Player " + random_string(5)
        player = datalayer.getOrCreateSavedPlayer('notAPlayerId', playerRandomName)
        print(player)
        
        playerII = datalayer.getOrCreateSavedPlayer(player.playerId)
        print(playerII)        
        
        self.assertEqual(player.playerId, playerII.playerId)
        self.assertEqual(player.name, playerII.name)
        self.assertEqual(player.chips, playerII.chips)
        self.assertEqual(player.currentBet, playerII.currentBet)
        self.assertEqual(player.folded, playerII.folded)
        self.assertEqual(player.currentAction, playerII.currentAction)
        
        playerII.chips = 1000
        playerII.name = "Some Test This is"
        playerII.folded = True
        hand = Hand()
        deck = Deck()
        deck.shuffle()
        hand.cards.append(deck.deal())
        hand.cards.append(deck.deal())
        playerII.hand = hand
        playerII.currentBet = 5
        
        datalayer.updatePlayer(playerII);
        playerIII = datalayer.getOrCreateSavedPlayer(player.playerId)     
        
        self.assertEqual(playerII.playerId, playerIII.playerId)
        self.assertEqual(playerII.name, playerIII.name)
        self.assertEqual(playerII.chips, playerIII.chips)
        self.assertEqual(playerII.currentBet, playerIII.currentBet)
        self.assertEqual(playerII.folded, playerIII.folded)
        self.assertEqual(playerII.currentAction, playerIII.currentAction)
        self.assertEqual(playerII.hand.cards[0], playerIII.hand.cards[0])
        
        datalayer.deletePlayer(player)  
        
    def test_Table(self):
        table = datalayer.getOrCreateSavedTable('notATableId')
        print(table)
        
        tableII = datalayer.getOrCreateSavedTable(table.tableId)
        print(tableII)        
        
        self.assertEqual(table.tableId, tableII.tableId)
        
        tableII.addPlayers(buildPlayers(5))
        tableII.setDealerAtRandom()
        tableII.setBlinds()
        tableII.prepareForNextHand()
        tableII.currentBet = 500
        
        datalayer.updateTable(tableII)
        tableIII = datalayer.getOrCreateSavedTable(tableII.tableId)
        
        self.assertEqual(tableII.tableId, tableIII.tableId)
        self.assertEqual(tableII.blind, tableIII.blind)
        self.assertEqual(tableII.currentBet, tableIII.currentBet)
        self.assertEqual(tableII.players[0].name, tableIII.players[0].name)
        self.assertEqual(tableII.players[1].name, tableIII.players[1].name)
        self.assertEqual(tableII.players[2].name, tableIII.players[2].name)
        self.assertEqual(tableII.players[3].name, tableIII.players[3].name)
        self.assertEqual(tableII.players[4].name, tableIII.players[4].name)
        self.assertEqual(tableII.statusId, tableIII.statusId)
                
        datalayer.deleteTable(tableII)
        
    def testFindATableForPlayer(self):
        players = buildPlayers(15)
        table = datalayer.findATableForPlayer(players[0])
        firstTableId = table.tableId
        
        for index in range(1,10):
            table = datalayer.findATableForPlayer(players[index])
            self.assertTrue(players[index] in table.players)
            self.assertEquals(table.tableId, firstTableId)

        table2 = datalayer.findATableForPlayer(players[11])
        self.assertNotEquals(table2.tableId, firstTableId)
        
        datalayer.deleteTable(table)
        datalayer.deleteTable(table2)

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def buildPlayers(count):
    players = []
    for _ in range (1, count + 1):
        players.append(Player("player " + random_string(5)))
    return players