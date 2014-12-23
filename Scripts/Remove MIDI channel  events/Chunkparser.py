from reaper_python import *
import re

def msg(m):
    RPR_ShowConsoleMsg(m)

def getChunk():
    chunk = ""
    chunkLists = []
    itemL = []
    selItemCount = RPR_CountSelectedMediaItems(0)
    if selItemCount == 0:
        msg("Select MIDI-item(s)")
        return 0, 0
    else:

        for i in range(selItemCount):
            item = RPR_GetSelectedMediaItem(0, i)
            itemL.append(item)
            chunk = RPR_GetSetItemState2(itemL[i], "", 1024*1024*4, 1)[2]
            chunkLists.append(list(chunk.split("\n")))
        return chunkLists, itemL

def removeEvents(event):
    event = str(event)
    chunkLists, itemL = getChunk()

    if not chunkLists:
        return
    if not itemL:
        return
    for j, chunkL in enumerate(chunkLists):
        newChunk = ""
        newChunkL = []
        i = 0
        while i < len(chunkL) - 1:

            while not (chunkL[i].startswith("E ") or chunkL[i].startswith("e ") or
                chunkL[i].startswith("Em ") or chunkL[i].startswith("em ") or
                chunkL[i].startswith("<X ") or chunkL[i].startswith("<x ")):
                if i == len(chunkL) - 1:
                    break
                if chunkL[i].startswith("FILE "):
                    msg("In-project MIDI-items only")
                    return
                newChunkL.append(chunkL[i] + "\n")
                i += 1

            while (chunkL[i].startswith("E ") or chunkL[i].startswith("e ") or
                chunkL[i].startswith("Em ") or chunkL[i].startswith("em ") or
                chunkL[i].startswith("<X ") or chunkL[i].startswith("<x ")):
                if i == len(chunkL) - 1:
                    break

                if i < len(chunkL) - 3:
                    if (chunkL[i + 1].startswith("E ") or chunkL[i + 1].startswith("e ") or
                        chunkL[i + 1].startswith("Em ") or chunkL[i + 1].startswith("em ") or
                        chunkL[i + 1].startswith("<X ") or chunkL[i + 1].startswith("<x ")):

                        eventType = str(chunkL[i].split(" ")[2][0])
                        if eventType == event:
                            eventPos = int(chunkL[i].split(" ")[1])
                            nextEventPos = int(chunkL[i + 1].split(" ")[1])
                            a = str(chunkL[i + 1])
                            b = re.split("(\s+)", a)
                            b[2] = str(eventPos + nextEventPos)
                            chunkL[i + 1] = "".join([char for char in b])
                            i += 1
                            continue

                newChunkL.append(chunkL[i] + "\n")
                i += 1
        newChunk = "".join([char for char in newChunkL])
##            msg(newChunk)
        RPR_GetSetItemState2(itemL[j], newChunk, 1024*1024*4, 1)