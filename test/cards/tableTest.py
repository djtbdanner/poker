import unittest
from table import Table
from player import Player, PlayerAction
import testFunctions
import logging

class TestDealerSet(unittest.TestCase):
	logging.basicConfig(level=logging.DEBUG)
	def test_SetDealerSetsAlls(self):
		pokerTable = Table()
		pokerTable.addPlayers(testFunctions.buildPlayers(5))
		
		playerIds = []
		for player in pokerTable.players:
			playerIds.append(player.name + " " + str(player.id))

		while (len(playerIds) > 0):
			pokerTable.setDealerAtRandom()
			for index, player in enumerate(pokerTable.players):
				if player.dealer:
					logging.info(" Setting " + str(index) + " " + player.name + " as dealer " + " " + str(player.id))
					if player.name + " " + str(player.id) in playerIds:
						playerIds.remove(player.name + " " + str(player.id))
					logging.info(" Player IDs, not yet dealer: " + str(playerIds))
	
		logging.info(" All players selected as dealer")
		self.assertFalse(len(playerIds) > 0)		

	def test_AddSamePlayerDoesNotAdd (self):
		pokerTable = Table()
		pokerTable.addPlayers(testFunctions.buildPlayers(5))
		
		self.assertEqual(5, len(pokerTable.players))
		#if (pokerTable.players[2] not in pokerTable.players):
		try:
			pokerTable.addPlayer(pokerTable.players[2])
			self.assertTrue(True, "should have excepted when adding same player again")
		except ValueError:
			self.assertTrue(True)
		
		self.assertEqual(5, len(pokerTable.players), "Should not be able to add same player more than once")
		
		pokerTable.players.append(Player("who is this dude"))
		self.assertEqual(6, len(pokerTable.players))
		
		for player in pokerTable.players:
			print(player.name)
			
	def test_setBlinds_and_reset (self):
		pokerTable = Table()
		pokerTable.addPlayers(testFunctions.buildPlayers(5))
		pokerTable.setDealerAtRandom()
		
		player1Chips = pokerTable.players[1].chips;
		player2Chips = pokerTable.players[2].chips
		
		pokerTable.setBlinds()
		
		self.assertEqual(pokerTable.players[1].chips, player1Chips -1)
		self.assertEqual(pokerTable.players[2].chips, player2Chips -2)
		self.assertEqual(pokerTable.players[1].currentBet, 1)
		self.assertEqual(pokerTable.players[2].currentBet, 2)
		self.assertEqual(pokerTable.players[1].currentAction, PlayerAction.CALL)
		self.assertEqual(pokerTable.players[2].currentAction, PlayerAction.CALL)
		self.assertEqual(pokerTable.pot, 3)
		self.assertEqual(pokerTable.currentBet, 2)
		
		idOfNextDealer = pokerTable.players[1].id
		
		pokerTable.prepareForNextHand()
		self.assertEqual(idOfNextDealer, pokerTable.players[0].id)
		self.assertEqual(pokerTable.pot, 0)
		self.assertEqual(pokerTable.currentBet, 0)
		self.assertEqual(pokerTable.players[1].currentAction, PlayerAction.NONE)
		self.assertEqual(pokerTable.players[2].currentAction, PlayerAction.NONE)	
		self.assertEqual(pokerTable.players[1].currentBet, 0)
		self.assertEqual(pokerTable.players[2].currentBet, 0)
		
	def test_deal_and_reset (self):
		pokerTable = Table()
		pokerTable.addPlayers(testFunctions.buildPlayers(5))
		pokerTable.setDealerAtRandom()
		
		pokerTable.dealRound()
		pokerTable.dealRound()
		
		for player in pokerTable.players:
			self.assertEqual(len(player.hand.cards), 2)
			
		pokerTable.prepareForNextHand()
		
		for player in pokerTable.players:
			self.assertEqual(len(player.hand.cards), 0)
			
	def test_round_complete (self):
		pokerTable = Table()
		pokerTable.addPlayers(testFunctions.buildPlayers(5))

		for player in pokerTable.players:
			player.currentAction = PlayerAction.FOLD
		
		self.assertTrue(pokerTable.isRoundComplete())
		
		pokerTable.currentBet = 2
		for player in pokerTable.players:
			player.currentAction = PlayerAction.CALL_CHECK_RAISE
			player.currentBet = 2
		
		self.assertTrue(pokerTable.isRoundComplete())		
		
		pokerTable.currentBet = 4
		for player in pokerTable.players:
			player.currentAction = PlayerAction.CALL_CHECK_RAISE
			player.currentBet = 4
			
		pokerTable.players[4].currentBet = 2
		
		self.assertFalse(pokerTable.isRoundComplete())	
		
		pokerTable.playerFold(4)
		
		self.assertTrue(pokerTable.isRoundComplete())		