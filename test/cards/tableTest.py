import unittest
from table import Table
from player import Player
import testFunctions

class TestDealerSet(unittest.TestCase):
	
	def test_SetDealer(self):
		pokerTable = Table()
		pokerTable.players = testFunctions.buildPlayers(5)
		
		playersCopy = list(pokerTable.players)
	   	
		fiveFalse = [False,False,False,False,False]
		while (False in fiveFalse):
			pokerTable.setDealerAtRandom()
			for index, player in enumerate(pokerTable.players):
				if (player.dealer):
					print ("Setting " + str(index) + " " + player.name + " as dealer " + " " + str(player.id))
					fiveFalse[index] = True
					print(fiveFalse)
	
	
		print("All players selected as dealer")
		self.assertFalse(False in fiveFalse)		
		
		for index, player in enumerate(playersCopy):
			self.assertEqual(player.id, pokerTable.players[index].id, "Player order should not change")
			
	
	def test_AddSamePlayerDoesNotAdd (self):
		pokerTable = Table()
		pokerTable.players = testFunctions.buildPlayers(5)
		
		self.assertEqual(5, len(pokerTable.players))
		if (pokerTable.players[2] not in pokerTable.players):
			pokerTable.players.append(pokerTable.players[2])
			
		self.assertEqual(5, len(pokerTable.players), "Should not be able to add same player more than once")
		
		pokerTable.players.append(Player("who is this dude"))
		self.assertEqual(6, len(pokerTable.players))
		
		for player in pokerTable.players:
			print(player.name)
				