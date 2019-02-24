import evaluation.processor as processor
import db.datalayer as datalayer
import logging
logger = logging.getLogger()


def makePlay(player, table, playerAction, actionAmount, currentStatus):
    try:
        if playerAction.lower() == "fold":
            table.playerFold(player)
        else:
            actionAmount = int(actionAmount)
            currentTableBet = table.currentBet
            playerCurrentBet = player.currentBet
            logger.info("Making play of actionAmount {0}, currentTableBet {1}, playerCurrentBet{2} for player {3}".format(actionAmount, currentTableBet, playerCurrentBet, player))
            if ((actionAmount + playerCurrentBet) < currentTableBet):
                raise ValueError("Player must call or bet more than current table bet.")
            if actionAmount > 0:
                logger.info("Player will call or bet")
                table.playerBetOrCall(player, actionAmount)
            else:
                logger.info("Player will check")
                table.playerCheck(player)
                
        logger.info("checking id round complete")   
        if (table.isRoundComplete()):
            logger.info("round is complete, now processing")
            if len(table.cards) == 0:
                table.dealToTable(3)
                table.prepareForNextRound()
            elif len(table.cards) < 5:
                table.dealToTable(1)
                table.prepareForNextRound()
            else:
                winnerList = processor.getWinners(table)
                winTotal = table.pot / len(winnerList)
                for player in winnerList:
                    player.chips = player.chips + winTotal
                table.winners = winnerList
                
        datalayer.updateTable(table)
        logger.info("make Play - table updated and returning.")
        return table
    except Exception as error:
        logger.exception("Failure making play for player.", error)

def checkForUpdates(table, player, currentStatus):
    if len(table.players) > 1:
        if not table.hasDealer():
            table.setDealerAtRandom()
        while not table.doAllPlayersHaveTwoCards():
            table.dealRound()
    datalayer.updateTable(table)
    return table
