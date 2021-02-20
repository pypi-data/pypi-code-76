import os
import sys

import shelve

import sync_dl.config as cfg

from sync_dl_ytapi.helpers import getPlId,pushOrderMoves
from sync_dl_ytapi.credentials import getCredentials,revokeTokens

from sync_dl_ytapi.ytapiWrappers import getItemIds,moveSong



# actual commands
def pushLocalOrder(plPath):
    credJson = getCredentials()
    if not credJson:
        return
    
    cfg.logger.info("Pushing Local Order to Remote...")
    
    with shelve.open(f"{plPath}/{cfg.metaDataName}", 'c',writeback=True) as metaData:
        url = metaData["url"]
        localIds = metaData["ids"]

    plId = getPlId(url)

    remoteIdPairs = getItemIds(credJson,plId)

    remoteIds,remoteItemIds = zip(*remoteIdPairs)

    cfg.logger.debug(f'Order Before Push: \n'+'\n'.join( [f'{i}: {str(remoteId)}' for i,remoteId in enumerate(remoteIds) ] ))

    moves = pushOrderMoves(remoteIds,remoteItemIds,localIds)



    for move in moves:
        newIndex, songId,itemId = move

        moveSong(credJson,plId,songId,itemId,newIndex)

def logout():
    revokeTokens()
    