from rich.table import Table
from rich.console import Console
from gameConfig import LANGUAGE
import time
import os
import random

if LANGUAGE == "zhcn":
    from language_zhcn import *
elif LANGUAGE == "en":
    from language_en import *
else:
    from language_en import *

def cText(text,color):
    colors = {
        "red":"\033[91m",
        "green":"\033[92m",
        "yellow":"\033[93m",
        "blue":"\033[94m",
        "magenta":"\033[95m",
        "cyan":"\033[96m",
        "white":"\033[97m",
        "black":"\033[30m",
        "reset":"\033[0m"
    }
    return colors[color] + str(text) + colors["reset"]

# 模拟打字机效果
def tyPrint(text,sleepTime=0.1,endWithNewLine=True):
    meetColorsMark = False
    for i in text:
        print(i,end='',flush=True)
        if i == "\033":
            meetColorsMark = True
        if meetColorsMark and i == "m":
            meetColorsMark = False
        if meetColorsMark:
            continue
        else:
            time.sleep(sleepTime)
    if endWithNewLine:
        print()

def clear():
    os.system("cls") if os.name == "nt" else os.system("clear")

def displayDesk(PLAYER_OBJ,DEALER_OBJ,BULLET_LIST,IS_DAMAGE_UP=False,playerTurn=True,showBullet=False,thisRound=1,totalRound=3,dealerLast=-1,playerLast=-1,cheatMode=False):
    console = Console()
    table = Table(title="")
    if DEALER_OBJ.isSkip:
        table.add_column("☠️⛓️", justify="center",style="yellow")
    else:
        table.add_column("☠️", justify="center",style="yellow")
    if not showBullet:
        if playerTurn:

            table.add_column(f"[[cyan]{LANG_DESK_YOUR_TURN}[white]]", justify="right",style="green")
        else:
            table.add_column(f"[[red]{LANG_DESK_DEALER_TURN}[white]]", justify="right",style="green")
    dealerEmojiList = DEALER_OBJ.showInventoryEmoji()
    dealerThisLine1 = ""
    dealerThisLine2 = ""
    doubleDamage = ""
    if IS_DAMAGE_UP:
        doubleDamage = f"[red]{LANG_DESK_DAMAGE_UP}"
    if len(dealerEmojiList) <= 4:
        for i in range(0,len(dealerEmojiList)):
            dealerThisLine1 += f"{i}{dealerEmojiList[i]}  "
    else:
        for i in range(4):
            dealerThisLine1 += f"{i}{dealerEmojiList[i]}  "
        for i in range(4,len(dealerEmojiList)):
            dealerThisLine2 += f"{i}{dealerEmojiList[i]}  "
    table.add_row(dealerThisLine1, "⚡"*DEALER_OBJ.health)
    table.add_row(dealerThisLine2, doubleDamage)
    table.add_row("----------------------", "")
    bulletInfo = ""
    dealerLastBulletInfo = ""
    if showBullet:
        formated = ["🔴" if str(i) == '1' else "🔵" for i in BULLET_LIST]
        if not cheatMode:
            random.shuffle(formated)
        bulletInfo = "："
        for i in formated:
            bulletInfo += i
    else:
        if dealerLast == 1:
            dealerLastBulletInfo = "🔴  "
        elif dealerLast == 0:
            dealerLastBulletInfo = "🔵  "
        if playerLast == 1:
            bulletInfo = "  🔴"
        elif playerLast == 0:
            bulletInfo = "  🔵"
    table.add_row(dealerLastBulletInfo+"🔫"+bulletInfo, f"[white]{LANG_ROUND_THIS_ATHEAD}[green]{thisRound}/{totalRound}[white]{LANG_ROUND_ATTAIL}")
    table.add_row("----------------------", "")
    playerEmojiList = PLAYER_OBJ.showInventoryEmoji()
    playerThisLine1 = ""
    playerThisLine2 = ""
    beenSkip = ""
    if PLAYER_OBJ.isSkip:
        beenSkip = f"[white]{LANG_DESK_YOU_BEEN_ATHEAD}⛓️‍💥{LANG_DESK_YOU_BEEN_ATTAIL}"
    if len(playerEmojiList) <= 4:
        for i in range(0,len(playerEmojiList)):
            playerThisLine1 += f"{i}{playerEmojiList[i]}  "
    else:
        for i in range(4):
            playerThisLine1 += f"{i}{playerEmojiList[i]}  "
        for i in range(4,len(playerEmojiList)):
            playerThisLine2 += f"{i}{playerEmojiList[i]}  "
    table.add_row(playerThisLine1, beenSkip)
    table.add_row(playerThisLine2,  "⚡"*PLAYER_OBJ.health)
    console.print(table)

# 数字累加显示效果，像加油站或者出租车的表的数字一样，可以选择限制函数在多少秒内要显示完毕
def displayNumberAccumulate(start,end):
    if start < end:
        for i in range(start,end+1,len(str(abs(end-start)))*11):
            print(f"\r{i}",end='',flush=True)
            time.sleep(10/(abs(end-start)))
        print()
    else:
        for i in range(start,end-1,len(str(abs(start-end)))*-11):
            print(f"\r{i}",end='',flush=True)
            time.sleep(10/(abs(end-start)))
        print()
