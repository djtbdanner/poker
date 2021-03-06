import unittest
from table import Table
from player import Player, PlayerAction
import evaluation.processor
import logging


class TestDealerSet(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def test_SetDealerSetsAlls(self):
        pokerTable = Table()
        tableStatus = pokerTable.statusId
        pokerTable.addPlayers(buildPlayers(5))
        self.assertFalse(tableStatus == pokerTable.statusId)        
        
        playerIds = []
        for player in pokerTable.players:
            playerIds.append(player.name + " " + str(player.playerId))

        while (len(playerIds) > 0):
            pokerTable.setDealerAtRandom()
            for index, player in enumerate(pokerTable.players):
                if player.dealer:
                    logging.info(" Setting " + str(index) + " " + player.name + " as dealer " + " " + str(player.playerId))
                    if player.name + " " + str(player.playerId) in playerIds:
                        playerIds.remove(player.name + " " + str(player.playerId))
                    logging.info(" Player IDs, not yet dealer: " + str(id))
    
        logging.info(" All players selected as dealer")
        self.assertFalse(len(playerIds) > 0)
        self.assertFalse(tableStatus == pokerTable.statusId)

    def test_AddSamePlayerDoesNotAdd (self):
        pokerTable = Table()
        tableStatus = pokerTable.statusId
        pokerTable.addPlayers(buildPlayers(5))
        
        self.assertEqual(5, len(pokerTable.players))
        # if (pokerTable.players[2] not in pokerTable.players):
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
        self.assertFalse(tableStatus == pokerTable.statusId)
        
        count = 6;
        for player in pokerTable.players:
            count = count-1
            pokerTable.removePlayer(player)
            self.assertEqual(count, len(pokerTable.players), "Didn't remove player")
        
        # remove player not on table does not cause fail
        pokerTable.removePlayer(Player("This player isn't on the table"))

            
    def test_setBlinds_and_reset (self):
        pokerTable = Table()
        pokerTable.addPlayers(buildPlayers(5))
        pokerTable.blind = 2
        
        player1Chips = pokerTable.players[1].chips;
        player2Chips = pokerTable.players[2].chips
        
        pokerTable.setDealerAtRandom()

        self.assertEqual(pokerTable.players[1].chips, player1Chips - 1)
        self.assertEqual(pokerTable.players[2].chips, player2Chips - 2)
        self.assertEqual(pokerTable.players[1].currentBet, 1)
        self.assertEqual(pokerTable.players[2].currentBet, 2)
        self.assertEqual(pokerTable.players[1].currentAction, PlayerAction.NONE)
        self.assertEqual(pokerTable.players[2].currentAction, PlayerAction.NONE)
        self.assertEqual(pokerTable.pot, 3)
        self.assertEqual(pokerTable.currentBet, 2)
        
        idOfNextDealer = pokerTable.players[1].playerId
        
        pokerTable.prepareForNextHand()
        self.assertEqual(idOfNextDealer, pokerTable.players[0].playerId)
        self.assertEqual(pokerTable.pot, 3)
        self.assertEqual(pokerTable.currentBet, pokerTable.blind)
        self.assertEqual(pokerTable.players[1].currentAction, PlayerAction.NONE)
        self.assertEqual(pokerTable.players[2].currentAction, PlayerAction.NONE)    
        self.assertEqual(pokerTable.players[1].currentBet, 1)
        self.assertEqual(pokerTable.players[2].currentBet, 2)
        
    def test_deal_and_reset (self):
        pokerTable = Table()
        pokerTable.addPlayers(buildPlayers(5))
        pokerTable.setDealerAtRandom()
        
        while not pokerTable.doAllPlayersHaveTwoCards():
            pokerTable.dealRound()
        
        for player in pokerTable.players:
            self.assertEqual(len(player.hand.cards), 2)
            
        pokerTable.prepareForNextHand()
        
        for player in pokerTable.players:
            self.assertEqual(len(player.hand.cards), 0)
            
    def test_round_complete (self):
        pokerTable = Table()
        pokerTable.addPlayers(buildPlayers(5))

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
        
        pokerTable.playerFoldByIndex(4)
        
        self.assertTrue(pokerTable.isRoundComplete())        
        
    def test_play_a_hand (self):
        pokerTable = Table()
        
        self.assertFalse(pokerTable.isPlayActive())
        pokerTable.addPlayers(buildPlayers(5))
        self.assertFalse(pokerTable.hasDealer())
        pokerTable.setDealerPosition(0)  # ## Player 1 can be dealer
        self.assertTrue(pokerTable.hasDealer())
        pokerTable.blind = 2

        pokerTable.dealRound()
        pokerTable.dealRound()
        
        self.assertTrue(pokerTable.isPlayActive())
        
        while not pokerTable.isRoundComplete():
            # ## always 3 because dealer is 0, low blind is 1 and high is 2
            for index in range(3, len(pokerTable.players) + 3):
                if index >= len(pokerTable.players):
                    index = index - len(pokerTable.players)
                pokerTable.playerBetOrCallByIndex(index, pokerTable.currentBet - pokerTable.players[index].currentBet)

        pokerTable.prepareForNextRound()

        print('\n--- flop ---\n ')
        pokerTable.dealToTable(3)
        
        player = Player("Just Added Player", None, "1234ID")
        pokerTable.addPlayer(player)
        playerTest = pokerTable.findPlayerById("1234ID")
        self.assertTrue(playerTest.folded)
        

        while not pokerTable.isRoundComplete():
            # ## always 1 because dealer is 0
            for index in range(1, len(pokerTable.players) + 1):
                if index >= len(pokerTable.players):
                    index = index - len(pokerTable.players)
                pokerTable.playerCheckByIndex(index)
        pokerTable.prepareForNextRound()
        
        self.assertTrue(pokerTable.isPlayActive())

        print ('\n--- turn ---\n')
        pokerTable.dealToTable(1)
        while not pokerTable.isRoundComplete():
            # ## always 1 because dealer is 0
            for index in range(1, len(pokerTable.players) + 1):
                if index >= len(pokerTable.players):
                    index = index - len(pokerTable.players)
                pokerTable.playerCheckByIndex(index)
        pokerTable.prepareForNextRound()
    
        print('\n--- river ---\n')
        pokerTable.dealToTable(1)
        while not pokerTable.isRoundComplete():
            # ## always 1 because dealer is 0
            for index in range(1, len(pokerTable.players) + 1):
                if index >= len(pokerTable.players):
                    index = index - len(pokerTable.players)
                pokerTable.playerCheckByIndex(index)
        
        winners = evaluation.processor.getWinners(pokerTable)
        print ('We have {0} winner{x}! '.format(len(winners), x='' if len(winners) == 1 else 's'))
        for player in winners:
            player.chips += int(pokerTable.pot / len(winners))
            print ("WINNER: {} wins, winning hand {}".format(player, player.showHand()))
            
        for player in pokerTable.players:
            print(player)
            
    def test_find_player(self):
        table = Table();
        players = buildPlayers(5)
        table.addPlayers(players)
        
        player = players[2]
        
        playerX = table.findPlayerById(player.playerId)
        self.assertEquals(player.playerId, playerX.playerId)   
        
    def test_all_player_fold_flag(self):
        table = Table();
        players = buildPlayers(5)
        table.addPlayers(players)
        table.dealRound()
        table.dealRound()
        
        self.assertFalse(table.haveAllButOnePlayerFolded())
        
        table.players[0].folded = True;
        self.assertFalse(table.haveAllButOnePlayerFolded())
        table.players[1].folded = True;
        self.assertFalse(table.haveAllButOnePlayerFolded())
        table.players[2].folded = True;
        self.assertFalse(table.haveAllButOnePlayerFolded())
        table.players[3].folded = True;
        self.assertTrue(table.haveAllButOnePlayerFolded())        
        
def buildPlayers(count):
    players = []
    for indx in range (1, count + 1):
        players.append(Player("player " + str(indx)))
    return players
