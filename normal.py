import time
import random
from gameConfig import *
from gameDispalay import *

import logging
from rich.logging import RichHandler
if debugMode:
    # To file.
    # logging.basicConfig(level="NOTSET",filename='br.log',filemode='a',format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="[%X]")
    # On screen.
    logging.basicConfig(level="NOTSET",format='%(message)s', datefmt="[%X]", handlers=[RichHandler()])
else:
    logging.basicConfig(level="WARNING", format = '%(message)s', datefmt="[%X]")

logger = logging.getLogger(__name__)
 
if LANGUAGE == "zhcn":
    from language_zhcn import *
elif LANGUAGE == "en":
    from language_en import *
else:
    print("Unsoported language, use English instead.")
    time.sleep(3)
    from language_en import *

# 游戏全局变量，会被加入到主游戏循环中
# 是否增伤
IS_DAMAGE_UP = False
# 玩家上一颗打出的子弹类型
# 1表示实弹 ，0表示空包弹，-1表示本局未打出子弹
PLAYER_LAST_BULLET = -1
# 庄家上一颗打出的子弹类型
DEALER_LAST_BULLET = -1
# 所有玩家在本轮子弹打光前，通过手机查看到的子弹位置
PHONE_BULLET_INDEX = -1
# 子弹列表，默认为空
# 真弹存放1，空包弹存放0
BULLET_LIST = []
# 当前霰弹枪的子弹index
CURRENT_BULLET_INDEX = 0

PLAYER_NAME = ""

# 游戏类
# 物品
# 2024.12.24，截止至Steam版《恶魔轮盘》v2.2.0，共有9种物品
ALL_ITEM_LIST_STRING = [
    "handSaw",                #手锯🔪
    "magnifyingGlass",        #放大镜🔍
    "handcuffs",              #手铐⛓️‍💥
    "cigarette",              #香烟🚬
    "beer",                   #啤酒🍺
    "phone",                  #手机📱
    "adrenaline",             #肾上腺素💉
    "inverter",               #逆转器🔄️
    "expiredMedicine",        #过期药品💊
]

# ---------------------------------------------

# 游戏编程思路：所有物品和玩家都是对象，共享全局变量
# 物品类
# 以对象形式存放在玩家道具列表（列表操作是玩家对象中的方法）
# 都只有use方法，部分会有返回值
# 调用use方法后，物品从列表中删除
# 故物品类没有destroy方法或is_used属性

class handSaw(object):
    def __init__(self):
        self.name = "handSaw"
        self.emoji = "🔪"
    def use():
        global IS_DAMAGE_UP
        IS_DAMAGE_UP=True
        return True

class magnifyingGlass(object):
    def __init__(self):
        self.name = "magnifyingGlass"
        self.emoji = "🔍"
    def use():
        global BULLET_LIST
        return BULLET_LIST[0]
    
class handcuffs(object):
    def __init__(self):
        self.name = "handcuffs"
        self.emoji = "⛓️‍💥"
    def use():
        return True

# 使用香烟恢复1点生命值，所以使用use方法后直接返回true
# 会直接修改对象的生命值
class cigarette(object):
    def __init__(self):
        self.name = "cigarette"
        self.emoji = "🚬"
    def use():
        return True

# 和香烟不一样，过期药品有50%恢复2点生命值，反之扣除1点生命值
# 会直接修改对象的生命值，返回值为判定结果（0为失败1为成功）
class expiredMedicine(object):
    def __init__(self):
        self.name = "expiredMedicine"
        self.emoji = "💊"
    def use():
        useResult = random.randint(0, 1)
        if useResult == 1:
            return True
        else:
            return False

# 使用啤酒将当前子弹退膛，返回子弹类型
class beer(object):
    def __init__(self):
        self.name = "beer"
        self.emoji = "🍺"
    def use(target):
        global BULLET_LIST, CURRENT_BULLET_INDEX, PLAYER_LAST_BULLET, DEALER_LAST_BULLET
        CURRENT_BULLET_INDEX+=1
        if target == "player":
            PLAYER_LAST_BULLET = BULLET_LIST.pop(0)
            return PLAYER_LAST_BULLET
        elif target == "dealer":
            DEALER_LAST_BULLET = BULLET_LIST.pop(0)
            return DEALER_LAST_BULLET
        else:
            return -1

class phone(object):
    def __init__(self):
        self.name = "phone"
        self.emoji = "📱"
    def use():
        global BULLET_LIST,PHONE_BULLET_INDEX
        if PHONE_BULLET_INDEX != -1:
            return PHONE_BULLET_INDEX,BULLET_LIST[PHONE_BULLET_INDEX]
        else:
            return -1,-1

class adrenaline(object):
    def __init__(self):
        self.name = "adrenaline"
        self.emoji = "💉"
    def use():
        return True
# 逆转当前的子弹类型
class inverter(object):
    def __init__(self):
        self.name = "inverter"
        self.emoji = "🔄️"
    def use():
        global BULLET_LIST
        if BULLET_LIST[0] == 0:
            BULLET_LIST[0] = 1
        else:
            BULLET_LIST[0] = 0
        return True

ALL_ITEM_LIST = {
    "handSaw": handSaw(),
    "magnifyingGlass": magnifyingGlass(),
    "handcuffs": handcuffs(),
    "cigarette": cigarette(),
    "beer": beer(),
    "phone": phone(),
    "adrenaline": adrenaline(),
    "inverter": inverter(),
    "expiredMedicine": expiredMedicine(),
}

# 返回扣除的生命值
def shot():
    global BULLET_LIST,IS_DAMAGE_UP,CURRENT_BULLET_INDEX
    CURRENT_BULLET_INDEX+=1
    thisBullet = BULLET_LIST.pop(0)
    if thisBullet == 1:
        if IS_DAMAGE_UP:
            IS_DAMAGE_UP = False
            return -2
        else:
            return -1
    else:
        return 0

# 玩家类
class Player(object):
    def __init__(self, health=3):
        self.health = health
        self.totalHealth = health
        self.inventory = []
        self.isSkip = False
    def healthModify(self, num):
        if self.health + num > self.totalHealth:
            self.health = self.totalHealth
        elif self.health + num < 0:
            self.health = 0
        else:
            self.health += num
        return self.health
    # 这个方法一次只能添加一次物品
    # 随机抽取,如果添加成功，返回物品名称
    # 物品总数不能超过8，超过则不能添加，返回"FAIL"(字符串)
    # 另外，玩家和庄家在有一个手机的情况下不能再拿一个手机
    def addItem(self):
        global ALL_ITEM_LIST, ALL_ITEM_LIST_STRING
        if len(self.inventory) >= 8:
            return "FAIL"
        else:
            thisItemString = ALL_ITEM_LIST_STRING[random.randint(0, len(ALL_ITEM_LIST_STRING)-1)]
            while thisItemString == "phone" and "phone" in self.showInventory():
                thisItemString = ALL_ITEM_LIST_STRING[random.randint(0, len(ALL_ITEM_LIST_STRING)-1)]
            item = ALL_ITEM_LIST[thisItemString]
            # debug
            # item = ALL_ITEM_LIST['phone']
            self.inventory.append(item)
            return item.name
    def useItem(self, index):
        global IS_DAMAGE_UP
        if self.inventory[index].name == "handSaw":
            if IS_DAMAGE_UP:
                tyPrint(LANG_PLAYER_HAD_USE_HANDSAW,sleepTime=TYPRINT_SPEED_UP*0.1)
                time.sleep(2)
                return -1
            else:
                tyPrint(LANG_PLAYER_USE_HANDSAW,sleepTime=TYPRINT_SPEED_UP*0.1)
                time.sleep(1)
                tyPrint(LANG_PLAYER_USE_HANDSAW_EXPLANATION,sleepTime=TYPRINT_SPEED_UP*0.1)
                time.sleep(3)
                handSaw.use()
                self.inventory.pop(index)
                return 0
        elif self.inventory[index].name == "magnifyingGlass":
            tyPrint(LANG_PLAYER_USE_MAGNIFYINGGLASS,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(2)
            tyPrint(LANG_PLAYER_USE_MAGNIFYINGGLASS_EXPLANATION_1,sleepTime=TYPRINT_SPEED_UP*0.1,endWithNewLine=False)
            time.sleep(1)
            tyPrint(LANG_PLAYER_USE_MAGNIFYINGGLASS_EXPLANATION_2,sleepTime=TYPRINT_SPEED_UP*0.1,endWithNewLine=False)
            time.sleep(random.randint(2,4))
            if magnifyingGlass.use() == 1:
                tyPrint(LANG_BULLET_LIVE,sleepTime=TYPRINT_SPEED_UP*0.1)
            else:
                tyPrint(LANG_BULLET_BLANK,sleepTime=TYPRINT_SPEED_UP*0.1)
            self.inventory.pop(index)
            time.sleep(3)
            return 0
        elif self.inventory[index].name == "handcuffs":
            tyPrint(LANG_PLAYER_USE_HANDCUFFS,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(1)
            tyPrint(LANG_PLAYER_USE_HANDCUFFS_EXPLANATION,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(3)
            handcuffs.use()
            self.inventory.pop(index)
            return 1
        elif self.inventory[index].name == "cigarette":
            tyPrint(LANG_PLAYER_USE_CIGARETTE,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(1)
            tyPrint(LANG_PLAYER_USE_CIGARETTE_EXPLANATION,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(3)
            self.inventory.pop(index)
            self.healthModify(1)
            return 0
        elif self.inventory[index].name == "beer":
            tyPrint(LANG_PLAYER_USE_BEER,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(2)
            tyPrint(LANG_PLAYER_USE_BEER_EXPLANATION,sleepTime=TYPRINT_SPEED_UP*0.1,endWithNewLine=False)
            time.sleep(random.randint(2,4))
            if beer.use("player") == 1:
                tyPrint(LANG_BULLET_LIVE,sleepTime=TYPRINT_SPEED_UP*0.1)
                self.inventory.pop(index)
                time.sleep(3)
                return 31
            else:
                tyPrint(LANG_BULLET_BLANK,sleepTime=TYPRINT_SPEED_UP*0.1)
                self.inventory.pop(index)
                time.sleep(3)
                return 30
        elif self.inventory[index].name == "phone":
            tyPrint(LANG_PLAYER_USE_PHONE,sleepTime=TYPRINT_SPEED_UP*0.1)
            getIndex,getType = phone.use()
            time.sleep(2)
            if getIndex == -1:
                tyPrint(LANG_HOW_UNFORTUNATE_RED,sleepTime=TYPRINT_SPEED_UP*0.1)
            else:
                tyPrint(f"{LANG_PLAYER_USE_PHONE_EXPLANATION_ATHEAD}{getIndex+1}{LANG_PLAYER_USE_PHONE_EXPLANATION_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1,endWithNewLine=False)                        
                time.sleep(random.randint(2,4))
                if getType == 1:
                    tyPrint(LANG_BULLET_LIVE,sleepTime=TYPRINT_SPEED_UP*0.1)
                else:
                    tyPrint(LANG_BULLET_BLANK,sleepTime=TYPRINT_SPEED_UP*0.1)
            self.inventory.pop(index)
            time.sleep(3)
            return 0
        elif self.inventory[index].name == "adrenaline":
            tyPrint(LANG_PLAYER_USE_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(2)
            self.inventory.pop(index)
            return 4
        elif self.inventory[index].name == "inverter":
            tyPrint(LANG_PLAYER_USE_INVERTER,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(2)
            tyPrint(LANG_PLAYER_USE_INVERTER_EXPLANATION,sleepTime=TYPRINT_SPEED_UP*0.1)
            inverter.use()
            self.inventory.pop(index)
            time.sleep(3)
            return 2
        elif self.inventory[index].name == "expiredMedicine":
            tyPrint(LANG_PLAYER_USE_EXPIREDMEDICINE,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(2)
            tyPrint(LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_1,sleepTime=TYPRINT_SPEED_UP*0.1,endWithNewLine=False)
            time.sleep(random.randint(2,4))
            if expiredMedicine.use():
                tyPrint(f"{LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_SUCCESS_ATHEAD}{cText('2','green')}{LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_SUCCESS_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                self.healthModify(2)
            else:
                print()
                clear(debugMode)
                tyPrint(f"{LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_FAIL_ATHEAD}{cText('1','red')}{LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_FAIL_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                self.healthModify(-1)
            self.inventory.pop(index)
            time.sleep(3)
            return 0
        else:
            return -1
    # 返回一个只有玩家物品栏中物品的名称的列表
    def showInventory(self):
        return [item.name for item in self.inventory]
    # 返回一个只有玩家物品栏中物品的emoji的列表
    def showInventoryEmoji(self):
        return [item.emoji for item in self.inventory]

#  AI庄家类，继承自玩家类
#  AI庄家的目标是尽可能使用当前已有道具了解情况，调整情况使得对自己有利并打赢玩家
# 可做出决策（回复生命值>查验类>手铐>子弹转换类，没有对应物品但有肾上腺素时，抢走玩家的物品）
# 只有在确定了当前子弹是什么类型的时候才会按这个顺序去使用道具：逆转器>手锯
# 具有记忆和剩余子弹概率推算
# 对于不确定的情况，如果剩余真弹:假弹=1:1，AI会选择打对方（猫说的）
# 会有一个方法根据记忆的历史子弹顺序、剩余的真/假弹数、使用过的查验类道具来尝试推测未来的子弹排列
# 当符合以下条件时，当前的子弹属于已知或可以推算剩余子弹的情况：
#  1. 剩余真弹==0，剩余假弹数!=0
#  2. 剩余真弹!=0，剩余假弹数==0
#  3. 当前子弹是AI使用查验类道具查出的子弹类型
#  4. AI使用了放大镜来检查子弹类型
#  会有一个变量/方法来告诉AI当前的情况是否需要只能通过概率来决定对谁开枪，还是可以通过推算/已知的子弹情况来决定对谁开枪
class Dealer(object):
    def __init__(self,totalLive,totalBlank,health=3):
        self.health = health
        self.totalHealth = health
        self.inventory = []
        self.isSkip = False
        self.memory = {}
        self.remainLive = totalLive
        self.remainBlank = totalBlank
        # 需要进行AI逻辑初始化（记忆初始化）
        # 就连AI也不允许直接查看弹夹
    # 获取AI庄家的记忆
    def getMemory(self):
        memory = self.memory
        return memory
    def whatIsIt(self,index):
        if index in self.memory:
            logger.debug(f'基于查验结果记忆：{index} 是 {self.memory[index]}')
            return self.memory[index]
        else:
            logger.debug(f'当前剩余真弹：{self.remainLive}，当前剩余空包弹：{self.remainBlank}')
            if self.remainLive >= self.remainBlank:
                logger.debug(f'基于剩余子弹概率比：{index} 是 1')
                return 1
            else:
                logger.debug(f'基于剩余子弹概率比：{index} 是 0')
                return 0
    # 记忆重置
    # 如果子弹打空了还没分出胜负，重新装填后调用这个方法
    def resetMemory(self,live,blank):
        logger.debug(f'记忆已重置，真弹数：{live}，空包弹数：{blank}')
        self.memory = {}
        self.remainLive = live
        self.remainBlank = blank
    # 手动更新庄家AI
    # 因为有逆转器这个道具
    def healthModify(self, num):
        if self.health + num > self.totalHealth:
            self.health = self.totalHealth
        elif self.health + num < 0:
            self.health = 0
        else:
            self.health += num
        return self.health
    # 这个方法一次只能添加一次物品
    # 随机抽取,如果添加成功，返回物品名称
    # 物品总数不能超过8，超过则不能添加，返回"FAIL"(字符串)
    # 不能再已经有手机的情况下再拿一个
    def addItem(self):
        global ALL_ITEM_LIST, ALL_ITEM_LIST_STRING
        if len(self.inventory) >= 8:
            return "FAIL"
        else:
            thisItemString = ALL_ITEM_LIST_STRING[random.randint(0, len(ALL_ITEM_LIST_STRING)-1)]
            while thisItemString == "phone" and "phone" in self.showInventory():
                thisItemString = ALL_ITEM_LIST_STRING[random.randint(0, len(ALL_ITEM_LIST_STRING)-1)]
            item = ALL_ITEM_LIST[thisItemString]
            # debug
            # item = ALL_ITEM_LIST['phone']
            self.inventory.append(item)
            return item.name
    # 返回扣除的生命值
    # 射击后必须在游戏逻辑调用flushMemory方法
    # 因为AI需要使用逻辑判断来使用物品
    # 所以不需要这个方法
    def useItem(self):
        pass
    # 返回一个只有玩家物品栏中物品的名称的列表
    def showInventory(self):
        return [item.name for item in self.inventory]
    # 返回一个只有玩家物品栏中物品的emoji的列表
    def showInventoryEmoji(self):
        return [item.emoji for item in self.inventory]
    # 查验类>手铐>子弹转换类

    # 处理生命值逻辑
    # 会一直执行这个逻辑直到生命值恢复到满值或庄家物品栏没有这类物品（在游戏主逻辑编程）
    def thinkHealth(self):
        logger.debug(f'执行生命值逻辑决策')
        # 判断是否负伤
        if self.health < self.totalHealth:
            # 只有生命值大于等于2才会考虑是否使用过期药品
            if self.health >= 2:
                for i in range(len(self.inventory)):
                    if self.inventory[i].name == "expiredMedicine":
                        # 返回真不会显示东西，如果收到了False值，只能表示使用了过期药品且扣除了生命值
                        result = expiredMedicine.use()
                        self.inventory.pop(i)
                        tyPrint(LANG_DEALER_USE_EXPIREDMEDICINE,sleepTime=TYPRINT_SPEED_UP*0.1)
                        time.sleep(random.randint(2,4))
                        if result:
                            tyPrint(f"{LANG_DEALER_USE_EXPIREDMEDICINE_SUCCESS_ATHEAD}{cText('2','green')}{LANG_DEALER_USE_EXPIREDMEDICINE_SUCCESS_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            self.healthModify(2)
                        else:
                            tyPrint(LANG_DEALER_USE_EXPIREDMEDICINE_FAIL,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(1)
                            tyPrint(f"{LANG_DEALER_USE_EXPIREDMEDICINE_FAIL_ATHEAD}{cText('1','red')}{LANG_DEALER_USE_EXPIREDMEDICINE_FAIL_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            self.healthModify(-1)
                        return result
                    else:
                        # 如果有香烟，使用香烟
                        for i in range(len(self.inventory)):
                            if self.inventory[i].name == "cigarette":
                                tyPrint(LANG_DEALER_USE_CIGARETTE,sleepTime=TYPRINT_SPEED_UP*0.1)
                                time.sleep(2)
                                self.inventory.pop(i)
                                self.healthModify(1)
                                return True
        # 通过返回DONOT来告诉一个处理逻辑可以跳出循环
        return 'DONOT'
    
    # 处理生命值逻辑（使用肾上腺素）
    # 会一直执行这个逻辑直到生命值恢复到满值或玩家物品栏没有这类物品（在游戏主逻辑编程）
    # 肾上腺素类方法都需要导入玩家的道具列表
    # 返回了物品名：成功偷走玩家物品并使用
    # 返回了DONOT：需要跳出逻辑循环
    def thinkHealthAdrenaline(self,getPlayerInventory):
        logger.debug(f'执行生命值逻辑决策（肾上腺素）')
        # 没有肾上腺素你偷啥？
        if 'adrenaline' not in self.showInventory():
            return 'DONOT'
        # 判断是否负伤
        if self.health < self.totalHealth:
            # 只有生命值大于等于2才会考虑是否使用过期药品
            if self.health >= 2:
                if 'expiredMedicine' in getPlayerInventory:
                    tyPrint(LANG_DEALER_USE_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    tyPrint(LANG_DEALER_RAP_EXPIREDMEDICINE,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    # 用掉肾上腺素并删除肾上腺素
                    for i in range(len(self.inventory)):
                        if self.inventory[i].name == "adrenaline":
                            result = expiredMedicine.use()
                            self.inventory.pop(i)
                            tyPrint(LANG_DEALER_USE_EXPIREDMEDICINE,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(random.randint(2,4))
                            if result:
                                tyPrint(f"{LANG_DEALER_USE_EXPIREDMEDICINE_SUCCESS_ATHEAD}{cText('2','green')}{LANG_DEALER_USE_EXPIREDMEDICINE_SUCCESS_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                                time.sleep(2)
                                self.healthModify(2)
                            else:
                                tyPrint(LANG_DEALER_USE_EXPIREDMEDICINE_FAIL,sleepTime=TYPRINT_SPEED_UP*0.1)
                                time.sleep(1)
                                tyPrint(f"{LANG_DEALER_USE_EXPIREDMEDICINE_FAIL_ATHEAD}{cText('1','red')}{LANG_DEALER_USE_EXPIREDMEDICINE_FAIL_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                                time.sleep(2)
                                self.healthModify(-1)
                            return "expiredMedicine"
                else:
                    tyPrint(LANG_DEALER_USE_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    tyPrint(LANG_DEALER_RAP_CIGARETTE,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    # 用掉肾上腺素并删除肾上腺素
                    for i in range(len(self.inventory)):
                        if self.inventory[i].name == "adrenaline":
                            tyPrint(LANG_DEALER_USE_CIGARETTE,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            self.inventory.pop(i)
                            self.healthModify(1)
                            return "cigarette"
        # 通过返回DONOT来告诉一个处理逻辑可以跳出循环
        return 'DONOT'
    
    # 查验类逻辑
    # 优先使用放大镜，其次是手机和啤酒
    # 会一直执行直到庄家没有此类物品或当前子弹已知（在游戏主逻辑编程）
    def thinkCheck(self,CURRENT_BULLET_INDEX):
        logger.debug(f'执行查验逻辑逻辑决策')
        # 全是真弹/假弹就不用查了
        if self.remainLive == 0 or self.remainBlank == 0:
            return 'DONOT'
        # 如果当前子弹未知才需要用放大镜
        if CURRENT_BULLET_INDEX not in self.memory:
            for i in range(len(self.inventory)):
                if self.inventory[i].name == "magnifyingGlass":
                    self.inventory.pop(i)
                    tyPrint(LANG_DEALER_USE_MAGNIFYINGGLASS,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    # 更新AI记忆
                    self.memory[CURRENT_BULLET_INDEX] = magnifyingGlass.use()
                    tyPrint(LANG_DEALER_VERY_INTERSTING,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    return True
        for i in range(len(self.inventory)):
            if self.inventory[i].name == "phone":
                self.inventory.pop(i)
                tyPrint(LANG_DEALER_USE_PHONE,sleepTime=TYPRINT_SPEED_UP*0.1)
                time.sleep(2)
                # 更新AI记忆
                getIndex,getType = phone.use()
                if getIndex == -1:
                    pass
                else:
                    self.memory[getIndex+CURRENT_BULLET_INDEX] = getType
                return True
        # 没有放大镜且当前子弹未知的情况会倾向于使用啤酒退膛
        if CURRENT_BULLET_INDEX not in self.memory:
            for i in range(len(self.inventory)):
                if self.inventory[i].name == "beer":
                    self.inventory.pop(i)
                    tyPrint(LANG_DEALER_USE_BEER,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    result = beer.use("dealer")
                    if result == 1:
                        tyPrint(LANG_DEALER_USE_BEER_IS_LIVE,sleepTime=TYPRINT_SPEED_UP*0.1)
                        self.remainLive -= 1
                        time.sleep(2)
                    else:
                        tyPrint(LANG_DEALER_USE_BEER_IS_BLANK,sleepTime=TYPRINT_SPEED_UP*0.1)
                        self.remainBlank -= 1
                        time.sleep(2)
                    return 'beer'
        # 通过返回DONOT来告诉一个处理逻辑可以跳出循环
        return 'DONOT'
    
    # 查验类逻辑（使用肾上腺素）
    # 优先抢走放大镜，其次是手机和啤酒
    # 会一直执行直到玩家没有此类物品或当前子弹已知（在游戏主逻辑编程）
    # 必须要在游戏主逻辑调用flushMemory方法
    def thinkCheckAdrenaline(self,getPlayerInventory,CURRENT_BULLET_INDEX):
        logger.debug(f'执行查验逻辑逻辑决策（肾上腺素）')
        if 'adrenaline' not in self.showInventory():
            return 'DONOT'
        # 全是真弹/假弹就不用查了
        if self.remainLive == 0 or self.remainBlank == 0:
            return 'DONOT'
        # 如果当前子弹未知才需要用放大镜
        if CURRENT_BULLET_INDEX not in self.memory and 'magnifyingGlass' in getPlayerInventory:
            tyPrint(LANG_DEALER_USE_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(2)
            tyPrint(LANG_DEALER_RAP_MAGNIFYINGGLASS,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(2)
            # 用掉肾上腺素并删除肾上腺素
            for i in range(len(self.inventory)):
                if self.inventory[i].name == "adrenaline":
                    tyPrint(LANG_DEALER_USE_MAGNIFYINGGLASS,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    self.inventory.pop(i)
                    self.memory[CURRENT_BULLET_INDEX] = magnifyingGlass.use()
                    tyPrint(LANG_DEALER_VERY_INTERSTING,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    return "magnifyingGlass"
        # 会有连续使用手机的bug，禁用
        # if 'phone' in getPlayerInventory:
        #     tyPrint(LANG_DEALER_USE_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
        #     time.sleep(2)
        #     tyPrint(LANG_DEALER_RAP_PHONE,sleepTime=TYPRINT_SPEED_UP*0.1)
        #     time.sleep(2)
        #     # 用掉肾上腺素并删除肾上腺素
        #     for i in range(len(self.inventory)):
        #         if self.inventory[i].name == "adrenaline":
        #             self.inventory.pop(i)
        #             tyPrint(LANG_DEALER_USE_PHONE,sleepTime=TYPRINT_SPEED_UP*0.1)
        #             time.sleep(2)
        #             getIndex,getType = phone.use()
        #             if getIndex == -1:
        #                 pass
        #             else:
        #                 self.memory[getIndex] = getType
        #             return "phone"
        # 没有放大镜、手机且当前子弹未知的情况会倾向于使用啤酒退膛
        if CURRENT_BULLET_INDEX not in self.memory and 'beer' in getPlayerInventory:
            tyPrint(LANG_DEALER_USE_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(2)
            tyPrint(LANG_DEALER_RAP_BEER,sleepTime=TYPRINT_SPEED_UP*0.1)
            time.sleep(2)
            # 用掉肾上腺素并删除肾上腺素
            for i in range(len(self.inventory)):
                if self.inventory[i].name == "adrenaline":
                    self.inventory.pop(i)
                    tyPrint(LANG_DEALER_USE_BEER,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    result = beer.use("dealer")
                    if result == 1:
                        tyPrint(LANG_DEALER_USE_BEER_IS_LIVE,sleepTime=TYPRINT_SPEED_UP*0.1)
                        self.remainLive -= 1
                        time.sleep(2)
                    else:
                        tyPrint(LANG_DEALER_USE_BEER_IS_BLANK,sleepTime=TYPRINT_SPEED_UP*0.1)
                        self.remainBlank -= 1
                        time.sleep(2)
                    return "beer"
        # 通过返回DONOT来告诉一个处理逻辑可以跳出循环
        return 'DONOT'
    
    # 如果当前是这两个情况，且有手铐的情况下，会使用手铐跳过玩家回合：
    # 1.当前子弹已知为真弹
    # 2.当前子弹已知为假弹，且有逆转器
    # 3.当前子弹已知为假弹，且能通过自己的肾上腺素偷走玩家的逆转器
    # 另外，只有玩家的isSkip为False时才能使用手铐
    def thinkHandcuffs(self,getPlayerInventory,CURRENT_BULLET_INDEX):
        logger.debug(f'执行手铐逻辑决策')
        shouldUse = False
        if 'handcuffs' not in self.showInventory():
            return False
        if CURRENT_BULLET_INDEX in self.memory:
            if self.memory[CURRENT_BULLET_INDEX] == 1:
                shouldUse = True
            elif self.memory[CURRENT_BULLET_INDEX] == 0 and 'inverter' in self.showInventory():
                shouldUse = True
            elif self.memory[CURRENT_BULLET_INDEX] == 0 and 'adrenaline' in self.showInventory() and 'inverter' in getPlayerInventory:
                shouldUse = True
            elif self.whatIsIt(CURRENT_BULLET_INDEX) == 1:
                    shouldUse = True
        if shouldUse:
            for i in range(len(self.inventory)):
                if self.inventory[i].name == "handcuffs":
                    self.inventory.pop(i)
                    tyPrint(LANG_DEALER_USE_HANDCUFFS,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    tyPrint(LANG_DEALER_USE_HANDCUFFS_EXPLANATION,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(2)
                    break
        return shouldUse

    # 如果当前是这两个情况，且玩家有手铐的情况下，会抢过手铐跳过玩家回合：
    # 1.当前子弹已知为真弹
    # 2.当前子弹已知为假弹，且有庄家有逆转器
    # 3.当前子弹已知为假弹，且还能通过自己的肾上腺素偷走玩家的逆转器
    # 庄家还有肾上腺素且玩家有逆转器的情况下，视为庄家有逆转器
    def thinkHandcuffsAdrenaline(self,getPlayerInventory,CURRENT_BULLET_INDEX):
        logger.debug(f'执行手铐逻辑决策（肾上腺素）')
        if 'adrenaline' not in self.showInventory():
            return 'DONOT'
        else:
            shouldUse = False
            if 'handcuffs' not in getPlayerInventory:
                return False
            if "handcuffs" in getPlayerInventory and CURRENT_BULLET_INDEX in self.memory:
                if self.memory[CURRENT_BULLET_INDEX] == 1:
                    shouldUse = True
                elif self.memory[CURRENT_BULLET_INDEX] == 0 and 'inverter' in self.showInventory():
                    shouldUse = True
                elif self.memory[CURRENT_BULLET_INDEX] == 0 and self.showInventory().count('adrenaline') >= 2 and 'inverter' in getPlayerInventory:
                    shouldUse = True
                elif self.whatIsIt(CURRENT_BULLET_INDEX) == 1:
                    shouldUse = True
            if shouldUse:
                tyPrint(LANG_DEALER_USE_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
                time.sleep(2)
                tyPrint(LANG_DEALER_RAP_HANDCUFFS,sleepTime=TYPRINT_SPEED_UP*0.1)
                time.sleep(2)
                for i in range(len(self.inventory)):
                    if self.inventory[i].name == "adrenaline":
                        self.inventory.pop(i)
                        tyPrint(LANG_DEALER_USE_HANDCUFFS,sleepTime=TYPRINT_SPEED_UP*0.1)
                        time.sleep(2)
                        tyPrint(LANG_DEALER_USE_HANDCUFFS_EXPLANATION,sleepTime=TYPRINT_SPEED_UP*0.1)
                        time.sleep(2)
                        break
        return shouldUse
    
    # 处理子弹事件逻辑（逆转器/手锯）
    # 庄家在这种情况下会使用逆转器（如果庄家有逆转器）：
    # 1.当前子弹已知为假弹或可预见剩下的全是假弹
    # 庄家在这种情况下会使用手锯（如果庄家有手锯）：
    # 1.当前子弹已知为真弹或可预见剩下的全是真弹，其中包括通过逆转器转换的真弹
    def thinkBulletChange(self,CURRENT_BULLET_INDEX,IS_DAMAGE_UP):
        logger.debug(f'执行子弹事件逻辑决策')
        if CURRENT_BULLET_INDEX in self.memory:
            if 'inverter' in self.showInventory() and (self.memory[CURRENT_BULLET_INDEX] == 0):
                self.memory[CURRENT_BULLET_INDEX] = 1
                self.remainBlank -= 1
                self.remainLive += 1
                for i in range(len(self.inventory)):
                    if self.inventory[i].name == "inverter":
                        inverter.use()
                        self.inventory.pop(i)
                        tyPrint(LANG_DEALER_USE_INVERTER,sleepTime=TYPRINT_SPEED_UP*0.1)
                        time.sleep(2)
                        break
                return True
            if 'handSaw' in self.showInventory() and (self.memory[CURRENT_BULLET_INDEX] == 1):
                if IS_DAMAGE_UP == 1 or IS_DAMAGE_UP == True:
                    return 'DONOT'
                for i in range(len(self.inventory)):
                    if self.inventory[i].name == "handSaw":
                        handSaw.use()
                        self.inventory.pop(i)
                        tyPrint(LANG_DEALER_USE_HANDSAW,sleepTime=TYPRINT_SPEED_UP*0.1)
                        time.sleep(2)
                        break
                return True
        return 'DONOT'

    # 处理子弹事件逻辑（逆转器/手锯），使用肾上腺素
    # 庄家在这种情况下会抢走玩家的逆转器（如果玩家有逆转器且庄家有肾上腺素）：
    # 1.当前子弹已知为假弹或可预见剩下的全是假弹
    # 庄家在这种情况下会抢走玩家的手锯（如果玩家有手锯且庄家有肾上腺素）：
    # 1.当前子弹已知为真弹或可预见剩下的全是真弹，其中包括通过逆转器转换的真弹
    def thinkBulletChangeAdrenaline(self,getPlayerInventory,CURRENT_BULLET_INDEX,IS_DAMAGE_UP):
        logger.debug(f'执行子弹事件逻辑决策（肾上腺素）')
        global PLAYER_OBJ
        if 'adrenaline' not in self.showInventory():
            return 'DONOT'
        else:
            if CURRENT_BULLET_INDEX in self.memory:
                if 'inverter' in getPlayerInventory and (self.memory[CURRENT_BULLET_INDEX] == 0):
                    self.memory[CURRENT_BULLET_INDEX] = 1
                    self.remainBlank -= 1
                    self.remainLive += 1
                    for i in range(len(self.inventory)):
                        if self.inventory[i].name == "adrenaline":
                            inverter.use()
                            self.inventory.pop(i)
                            tyPrint(LANG_DEALER_USE_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            tyPrint(LANG_DEALER_RAP_INVERTER,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            tyPrint(LANG_DEALER_USE_INVERTER,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            break
                    return 'inverter'
                if 'handSaw' in getPlayerInventory and (self.memory[CURRENT_BULLET_INDEX] == 1):
                    if IS_DAMAGE_UP == 1 or IS_DAMAGE_UP == True:
                        return 'DONOT'
                    for i in range(len(self.inventory)):
                        if self.inventory[i].name == "adrenaline":
                            handSaw.use()
                            self.inventory.pop(i)
                            tyPrint(LANG_DEALER_USE_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            tyPrint(LANG_DEALER_RAP_HANDSAW,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            tyPrint(LANG_DEALER_USE_HANDSAW,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            break
                    return 'handSaw'
            return 'DONOT'
            

    # 执行射击前最终的决策
    # 1、如果已知为真，打对方
    # 2、如果已知为假，打自己
    # 3、如果不知道，则使用`剩余未知真弹数和剩余未知假弹数`来计算概率，如果真弹数>=假弹数，打对方，否则打自己
    # 无论结果如何，AI必须要选择一个目标
    def thinkShot(self,CURRENT_BULLET_INDEX):
        logger.debug(f'执行决策')
        tyPrint(LANG_DEALER_RAISE_GUN,sleepTime=TYPRINT_SPEED_UP*0.1)
        time.sleep(2)
        if self.whatIsIt(CURRENT_BULLET_INDEX) == 1:
            logger.debug(f'决策射击对象：玩家')
            tyPrint(LANG_DEALER_AIM_YOU,sleepTime=TYPRINT_SPEED_UP*0.1)
            return 'player',False
        elif self.whatIsIt(CURRENT_BULLET_INDEX) == 0:
            logger.debug(f'决策射击对象：庄家')
            tyPrint(LANG_DEALER_AIM_SELF,sleepTime=TYPRINT_SPEED_UP*0.1)
            return 'dealer',False
        else:
            logger.debug(f'无法决策')
            return "DONOT",True

# ----------------------------------------------


# 子弹的初始化逻辑
# 是使用配置文件的随机参数（实弹空弹数量完全随机）
# 还是使用玩家的预设参数
# 玩家预设中所有子弹加起来不能超过10（会有配置文件设置器来约束这个条件）
# 随机参数的话，实弹或空弹不会超过5颗，这两种子弹至少会有1颗
def bulletDecision():
    global BULLET_LIST,USE_RANDOM_BULLET,INIT_BULLET_LIST,CURRENT_BULLET_INDEX
    live = 0
    blank = 0
    CURRENT_BULLET_INDEX = 0
    BULLET_LIST = []
    if USE_RANDOM_BULLET:
        logger.debug('使用随机选择')
        live = random.randint(1,5)
        blank = random.randint(1,5)
    else:
        logger.debug('使用预设')
        choice = random.choice(INIT_BULLET_LIST)
        logger.debug(f'选择预设：{choice}')
        live = choice[0]
        blank = choice[1]
    for i in range(0,live):
        BULLET_LIST.append(1)
    for i in range(0,blank):
        BULLET_LIST.append(0)
    for i in range(0,10):
        random.shuffle(BULLET_LIST)
        time.sleep(0.1)
    logger.debug(f'已完成装弹：{BULLET_LIST}')
    return live,blank

# “签署生死状”函数
# 其实就是设置玩家名称
def signWaiver():
    global PLAYER_NAME
    tyPrint(LANG_ASK_SIGN_WAIVER,sleepTime=TYPRINT_SPEED_UP*0.05)
    time.sleep(1)
    logger.debug('要求用户输入玩家名')
    while True:
        userName = input(LANG_SIGN_WAIVER_EXPLANATION)
        userName = userName.strip()
        if len(userName) > 6 or len(userName) < 1:
            continue
        if not userName.encode('utf-8').isalpha():
            continue
        userName = userName.upper()
        # 你怎么能是上帝和恶魔呢？
        if userName in ["GOD","DEALER","SATAN"]:
            continue
        PLAYER_NAME = userName
        logger.debug(f'玩家名：{PLAYER_NAME}')
        return True

# 生成确定的子弹位置
# 所有玩家在本轮子弹打光前，通过手机查看到的子弹位置
# 子弹的index从0开始
# 绝对位置：子弹在弹夹的实际index，如果弹夹刷新，位置也会刷新
# 相对位置：根据当前子弹index得到的相对玩家的位置
# 最终输出的是绝对位置
# 所以绝对位置取值在2-最后一颗子弹的index
# 如果剩余子弹数小于3，返回-1
# 每次检查时，绝对位置都是在2-最后一颗子弹的index的范围
# 如果还在这个范围，就不会刷新，否则需要刷新
def phoneBulletCheck():
    global PHONE_BULLET_INDEX,BULLET_LIST,CURRENT_BULLET_INDEX
    if len(BULLET_LIST) < 3:
        PHONE_BULLET_INDEX = -1
        return -1
    if PHONE_BULLET_INDEX in [2,len(BULLET_LIST)-1]:
        PHONE_BULLET_INDEX -= CURRENT_BULLET_INDEX
        return PHONE_BULLET_INDEX - CURRENT_BULLET_INDEX
    elif PHONE_BULLET_INDEX - CURRENT_BULLET_INDEX <= 1:
        PHONE_BULLET_INDEX = random.randint(2,len(BULLET_LIST)-1)
        return PHONE_BULLET_INDEX
    else:
        PHONE_BULLET_INDEX = random.randint(2,len(BULLET_LIST)-1)
        return PHONE_BULLET_INDEX

def normalGameMainThread(totalRound=3):
    global IS_DAMAGE_UP
    global PLAYER_LAST_BULLET
    global DEALER_LAST_BULLET
    global PHONE_BULLET_INDEX
    global BULLET_LIST
    global CURRENT_BULLET_INDEX
    global TYPRINT_SPEED_UP
    global PLAYER_NAME
    isGameOver = False
    cheatMode = False
    # 循环逻辑
    while True:
        clear(debugMode)
        logger.debug('游戏主循环开始')
        if PLAYER_NAME == "":
            signWaiver()
            # 彩蛋
            # 树懒都很慢
            if PLAYER_NAME == "FOLIVO":
                logger.debug('彩蛋：玩家为树懒时，TYPRINT_SPEED_UP设置为5，这会导致tyPrint方法输出变得非常慢')
                TYPRINT_SPEED_UP = 5
            # 你很急？
            if PLAYER_NAME == "HURRY":
                logger.debug('彩蛋：玩家很急，TYPRINT_SPEED_UP设置为0.05，这会导致tyPrint方法效果与print方法几乎一致')
                TYPRINT_SPEED_UP = 0.05
            if PLAYER_NAME == "JESUS":
                logger.debug('彩蛋：耶稣能在装弹前看到本轮弹夹的子弹顺序')
                cheatMode = True
            # 开发者可以是恶魔
            if PLAYER_NAME == "OLAF":
                logger.debug('彩蛋：说一下开发者是恶魔，其它没什么变化')
                tyPrint(f"{LANG_SAY_HELLO_ATHEAD}{cText(LANG_DEVIL,'yellow')} {cText(PLAYER_NAME,'yellow')}{LANG_SAY_HELLO_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                time.sleep(2)
                tyPrint(f"{LANG_DEALER_VERY_INTERSTING}",sleepTime=TYPRINT_SPEED_UP*0.05)
            else:
                tyPrint(f"{LANG_SAY_HELLO_ATHEAD}{cText(PLAYER_NAME,'yellow')}{LANG_SAY_HELLO_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
            isPlayerDeath = 0 
            time.sleep(1)
            tyPrint(LANG_TAKE_SEAT,sleepTime=TYPRINT_SPEED_UP*0.05)
            time.sleep(1)
        # 这里是每一局开始前的初始化代码
        for thisRound in range(1,totalRound+1):
            logger.debug(f'局：{thisRound}/{totalRound}')
            if thisRound >= 2:
                tyPrint(LANG_ENTRY_NEXT_ROUND,sleepTime=TYPRINT_SPEED_UP*0.05)
                time.sleep(2)
            tyPrint(f"{LANG_ROUND_THIS_ATHEAD}{thisRound}{LANG_ROUND_THIS_ATTAIL}{LANG_ROUND_TOTAL_ATHEAD}{totalRound}{LANG_ROUND_TOTAL_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
            time.sleep(4)
            # 只要双方还活着或者还有子弹就本局继续
            # 所以先初始化双方，在循环内写一个检测子弹是否为空的逻辑，还有初始化手机查到的子弹位置的逻辑
            # 决定道具数
            
            # 决定双方生命值
            healthForEach = random.randint(HEALTH_RANGE[0],HEALTH_RANGE[1])
            tyPrint("⚡"*healthForEach,sleepTime=TYPRINT_SPEED_UP*0.05,endWithNewLine=False)
            tyPrint(f"{LANG_HEALTH_ATHEAD}{cText(healthForEach,'yellow')}{LANG_HEALTH_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
            logger.debug(f'分配生命值：{healthForEach}')
            time.sleep(1)
            # 初始化玩家对象和庄家对象
            # 初始化弹夹，函数已装填子弹，这里返回的子弹组合情况
            thisLive,thisBlank = bulletDecision()
            logger.debug(f'真弹:假弹={thisLive}:{thisBlank}')
            PLAYER_OBJ = Player(healthForEach)
            # 庄家初始化前还需要告诉庄家这一局的子弹组合情况
            # 如果胜负未分，需要调用庄家的初始化函数resetMemory将记忆重置
            DEALER_OBJ = Dealer(thisLive,thisBlank,healthForEach)
            if len(ALL_ITEM_LIST_STRING) != 0:
                itemNumForEach = random.randint(ITEM_RANGE[0],ITEM_RANGE[1])
                 # 分配道具
                tyPrint(f"{LANG_ITEM_ATHEAD}{cText(itemNumForEach,'yellow')}{LANG_ITEM_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                time.sleep(1)
                for i in range(0,itemNumForEach):
                    if len(PLAYER_OBJ.inventory) >= 8:
                        logger.debug(f'玩家的道具栏已满')
                        # 随机获取一个物品名称来嘲讽玩家
                        playerPickUp = cText(ALL_ITEM_LIST_STRING_TRANS[random.choice(ALL_ITEM_LIST_STRING)],'yellow')
                        tyPrint(LANG_ITEM_OUT_OF_SPACE,sleepTime=TYPRINT_SPEED_UP*0.05)
                        time.sleep(1)
                        tyPrint(f"{LANG_ITEM_FULL_EXPLANATION_ATHEAD}{playerPickUp}{LANG_ITEM_FULL_EXPLANATION_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                        time.sleep(1)
                        tyPrint(LANG_HOW_UNFORTUNATE,sleepTime=TYPRINT_SPEED_UP*0.05)
                        time.sleep(1)
                        break
                    else:
                        playerPickUp = PLAYER_OBJ.addItem()
                        logger.debug(f'玩家道具添加结果：{playerPickUp}')
                        tyPrint(f"{LANG_ITEM_PLAYER_GET_ATHEAD}{cText(ALL_ITEM_LIST_STRING_TRANS[playerPickUp],'yellow')}{LANG_ITEM_PLAYER_GET_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                        time.sleep(1)
                for i in range(0,itemNumForEach):
                    if len(DEALER_OBJ.inventory) >= 8:
                        break
                    else:
                        dealerPickUp = DEALER_OBJ.addItem()
                        logger.debug(f'庄家道具添加结果：{dealerPickUp}')
                
            # 显示赌桌，展示子弹组合情况
            displayDesk(PLAYER_OBJ,DEALER_OBJ,BULLET_LIST,showBullet=True,thisRound=thisRound,totalRound=totalRound,cheatMode=cheatMode)
            tyPrint(f"{LANG_BULLET_SHOW_LIVE_ATHEAD}{cText(thisLive,'red')}{LANG_BULLET_SHOW_LIVE_ATTAIL} {LANG_BULLET_SHOW_BLANK_ATHEAD}{cText(thisBlank,'cyan')}{LANG_BULLET_SHOW_BLANK_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
            time.sleep(5)
            clear(debugMode)
            # 生命值归零判断主循环
            while not isGameOver:
                logger.debug(f'进入生命值归零判断主循环')
                # 玩家/庄家是否死亡
                if PLAYER_OBJ.health <= 0:
                    isGameOver = True
                    break
                if DEALER_OBJ.health <= 0:
                    isGameOver = True
                    break
                # 子弹检查
                if len(BULLET_LIST) == 0:
                    PLAYER_OBJ.isSkip = False
                    DEALER_OBJ.isSkip = False
                    time.sleep(2)
                    clear(debugMode)
                    tyPrint(LANG_BULLET_RELOADING,sleepTime=TYPRINT_SPEED_UP*0.05)
                    time.sleep(2)
                    # 重新分配道具
                    if len(ALL_ITEM_LIST_STRING) != 0:
                        #itemNumForEach = random.randint(ITEM_RANGE[0],ITEM_RANGE[1])
                        # 分配道具
                        tyPrint(f"{LANG_ITEM_ATHEAD}{cText(itemNumForEach,'yellow')}{LANG_ITEM_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                        time.sleep(1)
                        for i in range(0,itemNumForEach):
                            if len(PLAYER_OBJ.showInventory()) >= 8:
                                # 随机获取一个物品名称来嘲讽玩家
                                playerPickUp = cText(ALL_ITEM_LIST_STRING_TRANS[random.choice(ALL_ITEM_LIST_STRING)],'yellow')
                                tyPrint(LANG_ITEM_OUT_OF_SPACE,sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                                tyPrint(f"{LANG_ITEM_FULL_EXPLANATION_ATHEAD}{playerPickUp}{LANG_ITEM_FULL_EXPLANATION_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                                tyPrint(LANG_HOW_UNFORTUNATE,sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                                break
                            else:
                                playerPickUp = PLAYER_OBJ.addItem()
                                tyPrint(f"{LANG_ITEM_PLAYER_GET_ATHEAD}{cText(ALL_ITEM_LIST_STRING_TRANS[playerPickUp],'yellow')}{LANG_ITEM_PLAYER_GET_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                    for i in range(0,itemNumForEach):
                        if len(DEALER_OBJ.showInventory()) >= 8:
                            break
                        else:
                            DEALER_OBJ.addItem()
                    thisLive,thisBlank = bulletDecision()
                    DEALER_OBJ.resetMemory(thisLive,thisBlank)
                    displayDesk(PLAYER_OBJ,DEALER_OBJ,BULLET_LIST,showBullet=True,thisRound=thisRound,totalRound=totalRound,cheatMode=cheatMode)
                    time.sleep(1)
                    tyPrint(f"{LANG_BULLET_SHOW_LIVE_ATHEAD}{cText(thisLive,'red')}{LANG_BULLET_SHOW_LIVE_ATTAIL} {LANG_BULLET_SHOW_BLANK_ATHEAD}{cText(thisBlank,'cyan')}{LANG_BULLET_SHOW_BLANK_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                    time.sleep(5)
                    clear(debugMode)
                if PHONE_BULLET_INDEX == -1:
                    phoneBulletCheck()
                # 始终是玩家先手
                while True:
                    logger.debug(f'玩家回合开始，进入循环')
                    # 玩家/庄家是否死亡
                    if PLAYER_OBJ.health <= 0:
                        isGameOver = True
                        break
                    if DEALER_OBJ.health <= 0:
                        isGameOver = True
                        break
                    # 本局使用的逆转器次数
                    # 因为总有人闲着没事干上来就连续用两三个逆转器
                    inverterTimes = 0
                    IS_DAMAGE_UP = False
                    # 检查生命值是否为空
                    if PLAYER_OBJ.health == 0:
                        break
                    clear(debugMode)
                    displayDesk(PLAYER_OBJ,DEALER_OBJ,BULLET_LIST,IS_DAMAGE_UP=IS_DAMAGE_UP,playerTurn=True,thisRound=thisRound,totalRound=totalRound,dealerLast=DEALER_LAST_BULLET,playerLast=PLAYER_LAST_BULLET,cheatMode=cheatMode)
                    # 检查是否被跳过回合
                    if PLAYER_OBJ.isSkip:
                        tyPrint(LANG_PLAYER_BEEN_SKIP,sleepTime=TYPRINT_SPEED_UP*0.1)
                        time.sleep(1)
                        PLAYER_OBJ.isSkip = False
                        break
                    # 选择道具或射击操作
                    # 注意，如果上一颗是空包弹(前提是这一轮玩家已经开枪)，还能再开一枪
                    while True:
                        if len(BULLET_LIST) == 0:
                            PLAYER_OBJ.isSkip = False
                            DEALER_OBJ.isSkip = False
                            break
                        clear(debugMode)
                        displayDesk(PLAYER_OBJ,DEALER_OBJ,BULLET_LIST,IS_DAMAGE_UP=IS_DAMAGE_UP,playerTurn=True,thisRound=thisRound,totalRound=totalRound,dealerLast=DEALER_LAST_BULLET,playerLast=PLAYER_LAST_BULLET,cheatMode=cheatMode)
                        userCanContinue = True
                        # debug
                        logger.debug(f"当前子弹index:{CURRENT_BULLET_INDEX}")
                        logger.debug(f"当前弹夹：{BULLET_LIST}")
                        logger.debug(f"手机确定的index:{PHONE_BULLET_INDEX}")
                        userSelect = input(LANG_PLAYER_SELECT_ITEM_OR_SHOOT)
                        if str(userSelect).isdigit():
                            # 你没道具了你用啥道具？
                            if len(PLAYER_OBJ.inventory) == 0:
                                continue
                            if int(userSelect) >= 0 and int(userSelect) < len(PLAYER_OBJ.inventory):
                                tyPrint(f"{cText(ALL_ITEM_LIST_STRING_TRANS[PLAYER_OBJ.inventory[int(userSelect)].name],'yellow')}：{ALL_ITEM_LIST_EXPLANATION_TRANS[PLAYER_OBJ.inventory[int(userSelect)].name]}",sleepTime=TYPRINT_SPEED_UP*0.1)
                                print(f"0){LANG_PLAYER_SELECT_NO}\n1){LANG_PLAYER_SELECT_YES}")
                                itemConfirm = input()
                                if str(itemConfirm) == '1':
                                    resultCode = PLAYER_OBJ.useItem(int(userSelect))
                                    if resultCode == 1:
                                        if not DEALER_OBJ.isSkip:
                                            DEALER_OBJ.isSkip = True
                                        else:
                                            tyPrint(LANG_PLAYER_ADRENALINE_FAIL_HANDCUFFS_REASON,sleepTime=TYPRINT_SPEED_UP*0.1)
                                            PLAYER_OBJ.inventory.append(inverter())
                                    elif resultCode == 2:
                                        inverterTimes += 1
                                        if CURRENT_BULLET_INDEX in DEALER_OBJ.getMemory():
                                            if DEALER_OBJ.getMemory()[CURRENT_BULLET_INDEX] == 0:
                                                DEALER_OBJ.memory[CURRENT_BULLET_INDEX] = 1
                                            elif DEALER_OBJ.getMemory()[CURRENT_BULLET_INDEX] == 1:
                                                DEALER_OBJ.memory[CURRENT_BULLET_INDEX] = 0      
                                    elif resultCode == 30:
                                        DEALER_OBJ.remainBlank -= 1
                                        phoneBulletCheck()
                                    elif resultCode == 31:
                                        DEALER_OBJ.remainLive -= 1
                                        phoneBulletCheck()
                                    elif resultCode == 4:
                                        if len(DEALER_OBJ.showInventory()) == 0:
                                            tyPrint(LANG_PLAYER_ADRENALINE_FAIL_NOT_ITEM,sleepTime=TYPRINT_SPEED_UP*0.1)
                                            time.sleep(2)
                                            return -1
                                        while True:
                                            inputIndex = input(LANG_PLAYER_ADRENALINE_SELECT_ITEM)
                                            if inputIndex.isdigit():
                                                inputIndex = int(inputIndex)
                                                if inputIndex >= 0 and inputIndex < len(DEALER_OBJ.showInventory()):
                                                    if DEALER_OBJ.showInventory()[inputIndex] == "adrenaline":
                                                        tyPrint(LANG_PLAYER_ADRENALINE_FAIL_ADRENALINE,sleepTime=TYPRINT_SPEED_UP*0.1)
                                                        continue
                                                    # 也不能在对方回合被跳过时抢走手铐
                                                    elif DEALER_OBJ.showInventory()[inputIndex] == "handcuffs" and DEALER_OBJ.isSkip:
                                                        tyPrint(LANG_PLAYER_ADRENALINE_FAIL_HANDCUFFS_REASON ,endWithNewLine=False)
                                                        tyPrint(LANG_PLAYER_ADRENALINE_FAIL_HANDCUFFS,sleepTime=TYPRINT_SPEED_UP*0.1)
                                                        continue
                                                    # 也不能在伤害已加倍时抢走手锯
                                                    elif DEALER_OBJ.showInventory()[inputIndex] == "handSaw" and IS_DAMAGE_UP:
                                                        tyPrint(LANG_PLAYER_ADRENALINE_FAIL_HANDSAW_REASON,endWithNewLine=False)
                                                        tyPrint(LANG_PLAYER_ADRENALINE_FAIL_HANDSAW,sleepTime=TYPRINT_SPEED_UP*0.1)
                                                        continue   
                                                    PLAYER_OBJ.inventory.append(DEALER_OBJ.inventory.pop(int(inputIndex)))
                                                    # 此时玩家物品栏最末尾就是这个道具
                                                    resultCode == PLAYER_OBJ.useItem(-1)
                                                    if resultCode == 1:
                                                        DEALER_OBJ.isSkip = True
                                                    elif resultCode == 2:
                                                        inverterTimes += 1
                                                        if CURRENT_BULLET_INDEX in DEALER_OBJ.getMemory():
                                                            if DEALER_OBJ.getMemory()[CURRENT_BULLET_INDEX] == 0:
                                                                DEALER_OBJ.memory[CURRENT_BULLET_INDEX] = 1
                                                            elif DEALER_OBJ.getMemory()[CURRENT_BULLET_INDEX] == 1:
                                                                DEALER_OBJ.memory[CURRENT_BULLET_INDEX] = 0         
                                                    elif resultCode == 30:
                                                        DEALER_OBJ.remainBlank -= 1
                                                        phoneBulletCheck()
                                                    elif resultCode == 31:
                                                        DEALER_OBJ.remainLive -= 1
                                                        phoneBulletCheck()
                                                    break
                                            elif str(inputIndex) == str(""):
                                                PLAYER_OBJ.inventory.pop(int(userSelect))
                                                break

                                    if len(BULLET_LIST) == 0:
                                        PLAYER_OBJ.isSkip = False
                                        DEALER_OBJ.isSkip = False
                                        break    
                                continue
                            else:
                                continue
                        elif str(userSelect) == '+':
                            tyPrint(LANG_AGAIN_IF_SHOT_SELF_BLANK,sleepTime=TYPRINT_SPEED_UP*0.01)
                            tyPrint(LANG_PLAYER_AIM_TARGET,sleepTime=TYPRINT_SPEED_UP*0.1)
                            print(f"0){LANG_DEALER}\n1){LANG_SELF}")
                            while True: 
                                shotConfirm = input(LANG_PLAYER_AIM_INPUT)
                                if str(shotConfirm) == '0':
                                    tyPrint(LANG_PLAYER_AIM_TARGET_DEALER,sleepTime=TYPRINT_SPEED_UP*0.1)
                                    getDamage = shot()
                                    DEALER_OBJ.healthModify(getDamage)
                                    time.sleep(random.randint(2,4))
                                    if getDamage == 0:
                                        PLAYER_LAST_BULLET = 0
                                        userCanContinue = False
                                        tyPrint(LANG_SOUND_CLINK,sleepTime=TYPRINT_SPEED_UP*0.1)
                                        time.sleep(1)
                                        tyPrint(LANG_PLAYER_SHOOT_BLANK,sleepTime=TYPRINT_SPEED_UP*0.1)
                                        time.sleep(3)
                                        # 逆转器使用次数为奇数时，表示这颗子弹是逆转过的
                                        if inverterTimes % 2 != 0:
                                            DEALER_OBJ.remainLive -= 1
                                        else:
                                            DEALER_OBJ.remainBlank -= 1
                                        inverterTimes = 0
                                        IS_DAMAGE_UP = False
                                        phoneBulletCheck()
                                    else:
                                        PLAYER_LAST_BULLET = 1
                                        userCanContinue = False
                                        tyPrint(LANG_SOUND_BOOM,sleepTime=TYPRINT_SPEED_UP*0.1)
                                        time.sleep(1)
                                        tyPrint(LANG_PLAYER_SHOOT_LIVE,sleepTime=TYPRINT_SPEED_UP*0.1,endWithNewLine=False)
                                        time.sleep(1)
                                        tyPrint(f"{LANG_DAMAGE_DEALER_ATHEAD}{cText(abs(getDamage),'red')}{LANG_DAMAGE_DEALER_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                                        time.sleep(2)
                                        # 逆转器使用次数为奇数时，表示这颗子弹是逆转过的
                                        if inverterTimes % 2 != 0:
                                            DEALER_OBJ.remainBlank -= 1
                                        else:
                                            DEALER_OBJ.remainLive -= 1
                                        inverterTimes = 0
                                        IS_DAMAGE_UP = False
                                        phoneBulletCheck()
                                    break
                                elif str(shotConfirm) == '1':
                                    tyPrint(LANG_PLAYER_AIM_TARGET_SELF,sleepTime=TYPRINT_SPEED_UP*0.1)
                                    getDamage = shot()
                                    PLAYER_OBJ.healthModify(getDamage)
                                    time.sleep(random.randint(2,4))
                                    if getDamage == 0:
                                        PLAYER_LAST_BULLET = 0
                                        if len(BULLET_LIST) != 0:
                                            userCanContinue = True
                                        tyPrint(LANG_SOUND_CLINK,sleepTime=TYPRINT_SPEED_UP*0.1)
                                        time.sleep(1)
                                        tyPrint(LANG_PLAYER_SHOOT_BLANK,sleepTime=TYPRINT_SPEED_UP*0.1)
                                        time.sleep(3)
                                        # 逆转器使用次数为奇数时，表示这颗子弹是逆转过的
                                        if inverterTimes % 2 != 0:
                                            DEALER_OBJ.remainLive -= 1
                                        else:
                                            DEALER_OBJ.remainBlank -= 1
                                        inverterTimes = 0
                                        IS_DAMAGE_UP = False
                                        phoneBulletCheck()
                                    else:
                                        PLAYER_LAST_BULLET = 1
                                        userCanContinue = False
                                        clear(debugMode)
                                        tyPrint(LANG_SOUND_BOOM,sleepTime=TYPRINT_SPEED_UP*0.1)
                                        time.sleep(1)
                                        tyPrint(LANG_PLAYER_SHOOT_LIVE,sleepTime=TYPRINT_SPEED_UP*0.1,endWithNewLine=False)
                                        time.sleep(1)
                                        tyPrint(f"{LANG_DAMAGE_PLAYER_ATHEAD}{cText(abs(getDamage),'red')}{LANG_DAMAGE_PLAYER_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                                        time.sleep(2)
                                        # 逆转器使用次数为奇数时，表示这颗子弹是逆转过的
                                        if inverterTimes % 2 != 0:
                                            DEALER_OBJ.remainBlank -= 1
                                        else:
                                            DEALER_OBJ.remainLive -= 1
                                        inverterTimes = 0
                                        IS_DAMAGE_UP = False
                                        phoneBulletCheck()
                                    break
                                else:
                                    continue
                            if not userCanContinue:
                                break
                            else:
                                if len(BULLET_LIST) == 0:
                                    PLAYER_OBJ.isSkip = False
                                    DEALER_OBJ.isSkip = False
                                else:
                                    continue
                        else:
                            continue
                    if not userCanContinue:
                        break
                    else:
                        if len(BULLET_LIST) == 0:
                            PLAYER_OBJ.isSkip = False
                            DEALER_OBJ.isSkip = False
                            break
                        else:
                            continue
                logger.debug(f'玩家回合结束')
                clear(debugMode)
                # 玩家/庄家是否死亡
                if PLAYER_OBJ.health <= 0:
                    isGameOver = True
                    break
                if DEALER_OBJ.health <= 0:
                    isGameOver = True
                    break
                if len(BULLET_LIST) == 0:
                    PLAYER_OBJ.isSkip = False
                    DEALER_OBJ.isSkip = False
                    time.sleep(2)
                    clear(debugMode)
                    tyPrint(LANG_BULLET_RELOADING,sleepTime=TYPRINT_SPEED_UP*0.05)
                    time.sleep(2)
                    # 重新分配道具
                    if len(ALL_ITEM_LIST_STRING) != 0:
                        # temNumForEach = random.randint(ITEM_RANGE[0],ITEM_RANGE[1])
                        # 分配道具
                        tyPrint(f"{LANG_ITEM_ATHEAD}{cText(itemNumForEach,'yellow')}{LANG_ITEM_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                        time.sleep(1)
                        for i in range(0,itemNumForEach):
                            if len(PLAYER_OBJ.showInventory()) >= 8:
                                # 随机获取一个物品名称来嘲讽玩家
                                playerPickUp = cText(ALL_ITEM_LIST_STRING_TRANS[random.choice(ALL_ITEM_LIST_STRING)],'yellow')
                                tyPrint(LANG_ITEM_OUT_OF_SPACE,sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                                tyPrint(f"{LANG_ITEM_FULL_EXPLANATION_ATHEAD}{playerPickUp}{LANG_ITEM_FULL_EXPLANATION_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                                tyPrint(LANG_HOW_UNFORTUNATE,sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                                break
                            else:
                                playerPickUp = PLAYER_OBJ.addItem()
                                tyPrint(f"{LANG_ITEM_PLAYER_GET_ATHEAD}{cText(ALL_ITEM_LIST_STRING_TRANS[playerPickUp],'yellow')}{LANG_ITEM_PLAYER_GET_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                    for i in range(0,itemNumForEach):
                        if len(DEALER_OBJ.showInventory()) >= 8:
                            break
                        else:
                            DEALER_OBJ.addItem()
                    thisLive,thisBlank = bulletDecision()
                    DEALER_OBJ.resetMemory(thisLive,thisBlank)
                    displayDesk(PLAYER_OBJ,DEALER_OBJ,BULLET_LIST,showBullet=True,thisRound=thisRound,totalRound=totalRound,cheatMode=cheatMode)
                    time.sleep(1)
                    tyPrint(f"{LANG_BULLET_SHOW_LIVE_ATHEAD}{cText(thisLive,'red')}{LANG_BULLET_SHOW_LIVE_ATTAIL} {LANG_BULLET_SHOW_BLANK_ATHEAD}{cText(thisBlank,'cyan')}{LANG_BULLET_SHOW_BLANK_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                    time.sleep(5)
                    clear(debugMode)
                    continue
                # 然后是庄家
                IS_DAMAGE_UP = False
                clear(debugMode)
                displayDesk(PLAYER_OBJ,DEALER_OBJ,BULLET_LIST,IS_DAMAGE_UP=IS_DAMAGE_UP,playerTurn=False,thisRound=thisRound,totalRound=totalRound,dealerLast=DEALER_LAST_BULLET,playerLast=PLAYER_LAST_BULLET,cheatMode=cheatMode)
                logger.debug(f'庄家回合开始')
                while not DEALER_OBJ.isSkip:
                    logger.debug(f'进入庄家循环')
                    if len(BULLET_LIST) == 0:
                        PLAYER_OBJ.isSkip = False
                        DEALER_OBJ.isSkip = False
                        break
                    dealerCanContinue = True
                    # AI逻辑
                    # 1.检查生命值
                    result = DEALER_OBJ.thinkHealth()
                    logger.debug(f'检查生命值逻辑结果：{result}')
                    while result != 'DONOT':
                        result = DEALER_OBJ.thinkHealth()
                        logger.debug(f'检查生命值逻辑结果：{result}')
                    # 2.检查是否能通过肾上腺素来抢走玩家的道具并恢复生命值
                    result = DEALER_OBJ.thinkHealthAdrenaline(PLAYER_OBJ.showInventory())
                    logger.debug(f'检查生命值（肾上腺素）逻辑结果：{result}')
                    if result in ["cigarette","expiredMedicine"]:
                        for i in range(0,len(PLAYER_OBJ.inventory)):
                            if PLAYER_OBJ.inventory[i].name == result:
                                PLAYER_OBJ.inventory.pop(i)
                                break
                    while result != 'DONOT':
                        result = DEALER_OBJ.thinkHealthAdrenaline(PLAYER_OBJ.showInventory())
                        logger.debug(f'检查生命值（肾上腺素）逻辑结果：{result}')
                        if result in ["cigarette","expiredMedicine"]:
                            for i in range(0,len(PLAYER_OBJ.inventory)):
                                if PLAYER_OBJ.inventory[i].name == result:
                                    PLAYER_OBJ.inventory.pop(i)
                                    break
                    # 3.检查是否能查验子弹
                    result = DEALER_OBJ.thinkCheck(CURRENT_BULLET_INDEX)
                    logger.debug(f'查验子弹逻辑结果：{result}')
                    if result == 'beer':
                        phoneBulletCheck()
                    if len(BULLET_LIST) == 0:
                        break
                    while result != 'DONOT':
                        result = DEALER_OBJ.thinkCheck(CURRENT_BULLET_INDEX)
                        logger.debug(f'查验子弹逻辑结果：{result}')
                        if result == 'beer':
                            phoneBulletCheck()
                        if len(BULLET_LIST) == 0:
                            break
                    if len(BULLET_LIST) == 0:
                        break
                    # 4.检查是否能通过肾上腺素来抢走玩家的道具并查验子弹
                    result = DEALER_OBJ.thinkCheckAdrenaline(PLAYER_OBJ.showInventory(),CURRENT_BULLET_INDEX)
                    logger.debug(f'查验子弹（肾上腺素）逻辑结果：{result}')
                    if len(BULLET_LIST) == 0:
                        break
                    if result == 'beer':
                        phoneBulletCheck()
                    if result in ["magnifyingGlass","phone","beer"]:
                        for i in range(0,len(PLAYER_OBJ.inventory)):
                            if PLAYER_OBJ.inventory[i].name == result:
                                PLAYER_OBJ.inventory.pop(i)
                                break
                    while result != 'DONOT':
                        result = DEALER_OBJ.thinkCheckAdrenaline(PLAYER_OBJ.showInventory(),CURRENT_BULLET_INDEX)
                        logger.debug(f'查验子弹（肾上腺素）逻辑结果：{result}')
                        if len(BULLET_LIST) == 0:
                            break
                        if result == 'beer':
                            phoneBulletCheck()
                        if result in ["magnifyingGlass","phone","beer"]:
                            for i in range(0,len(PLAYER_OBJ.inventory)):
                                if PLAYER_OBJ.inventory[i].name == result:
                                    PLAYER_OBJ.inventory.pop(i)
                                    break
                    if len(BULLET_LIST) == 0:
                        break
                    # 5.检查是否需要使用手铐
                    # 这个函数比较特殊，不需要do while
                    # 返回True：AI认为需要铐住玩家
                    # 返回False：AI认为不需要铐住玩家/不具备铐住玩家的条件
                    result = DEALER_OBJ.thinkHandcuffs(PLAYER_OBJ.showInventory(),CURRENT_BULLET_INDEX)
                    logger.debug(f'手铐逻辑结果：{result}')
                    if result == True:
                        PLAYER_OBJ.isSkip = True
                    # 6.检查是否有肾上腺素且需要抢走玩家的手铐
                    # 同样，不需要do while
                    # 如果已经铐住了，就不需要这一步了
                    # 返回True：AI认为需要抢走玩家的手铐
                    # 返回False：AI认为不需要抢走玩家的手铐/不具备铐住玩家的条件/玩家没有手铐
                    if not PLAYER_OBJ.isSkip:
                        result = DEALER_OBJ.thinkHandcuffs(PLAYER_OBJ.showInventory(),CURRENT_BULLET_INDEX)
                        logger.debug(f'手铐逻辑（肾上腺素）结果：{result}')
                        if result == True:
                            PLAYER_OBJ.isSkip = True
                            for i in range(0,len(PLAYER_OBJ.inventory)):
                                if PLAYER_OBJ.inventory[i].name == "handcuffs":
                                    PLAYER_OBJ.inventory.pop(i)
                                    break
                    # 7.处理子弹事件
                    result = DEALER_OBJ.thinkBulletChange(CURRENT_BULLET_INDEX,IS_DAMAGE_UP)
                    logger.debug(f'子弹事件逻辑结果：{result}')
                    while result != 'DONOT':
                        result = DEALER_OBJ.thinkBulletChange(CURRENT_BULLET_INDEX,IS_DAMAGE_UP)
                        logger.debug(f'子弹事件逻辑结果：{result}')
                    # 8.是否需要使用肾上腺素来抢走玩家的道具并处理子弹事件
                    result = DEALER_OBJ.thinkBulletChangeAdrenaline(PLAYER_OBJ.showInventory(),CURRENT_BULLET_INDEX,IS_DAMAGE_UP)
                    logger.debug(f'子弹事件逻辑（肾上腺素）结果：{result}')
                    while result != 'DONOT':
                        result = DEALER_OBJ.thinkBulletChangeAdrenaline(PLAYER_OBJ.showInventory(),CURRENT_BULLET_INDEX,IS_DAMAGE_UP)
                        logger.debug(f'子弹事件逻辑（肾上腺素）结果：{result}')
                        if result in ["inverter","handSaw"]:
                            for i in range(0,len(PLAYER_OBJ.inventory)):
                                if PLAYER_OBJ.inventory[i].name == result:
                                    PLAYER_OBJ.inventory.pop(i)
                                    break
                    # 9.最终决策
                    logger.debug(f'当前子弹index：{CURRENT_BULLET_INDEX}')
                    logger.debug(f'当前弹夹：{BULLET_LIST}')
                    logger.debug(f'AI庄家记忆：{DEALER_OBJ.getMemory()}')
                    shouldShotTo,thisIsUnknown = DEALER_OBJ.thinkShot(CURRENT_BULLET_INDEX)
                    if shouldShotTo == 'dealer':
                        getDamage = shot()
                        DEALER_OBJ.healthModify(getDamage)
                        time.sleep(random.randint(2,4))
                        if getDamage == 0:
                            DEALER_LAST_BULLET = 0
                            if len(BULLET_LIST) != 0:
                                dealerCanContinue = True
                            tyPrint(LANG_SOUND_CLINK,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(1)
                            tyPrint(LANG_DEALER_SHOOT_BLANK,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(3)
                            IS_DAMAGE_UP = False
                            DEALER_OBJ.remainBlank -= 1
                            phoneBulletCheck()
                        else:
                            DEALER_LAST_BULLET = 1
                            dealerCanContinue = False
                            tyPrint(LANG_SOUND_BOOM,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(1)
                            tyPrint(LANG_DEALER_SHOOT_LIVE,sleepTime=TYPRINT_SPEED_UP*0.1,endWithNewLine=False)
                            time.sleep(1)
                            tyPrint(f"{LANG_DAMAGE_DEALER_ATHEAD}{cText(abs(getDamage),'red')}{LANG_DAMAGE_DEALER_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            IS_DAMAGE_UP = False
                            DEALER_OBJ.remainLive -= 1
                            phoneBulletCheck()
                    elif shouldShotTo == 'player':
                        getDamage = shot()
                        PLAYER_OBJ.healthModify(getDamage)
                        time.sleep(random.randint(2,4))
                        if getDamage == 0:
                            DEALER_LAST_BULLET = 0
                            dealerCanContinue = False
                            tyPrint(LANG_SOUND_CLINK,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(1)
                            tyPrint(LANG_DEALER_SHOOT_BLANK,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(3)
                            IS_DAMAGE_UP = False
                            DEALER_OBJ.remainBlank -= 1
                            phoneBulletCheck()
                        else:
                            DEALER_LAST_BULLET = 1
                            dealerCanContinue = False
                            clear(debugMode)
                            tyPrint(LANG_SOUND_BOOM,sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(1)
                            tyPrint(LANG_DEALER_SHOOT_LIVE,sleepTime=TYPRINT_SPEED_UP*0.1,endWithNewLine=False)
                            time.sleep(1)
                            tyPrint(f"{LANG_DAMAGE_PLAYER_ATHEAD}{cText(abs(getDamage),'red')}{LANG_DAMAGE_PLAYER_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.1)
                            time.sleep(2)
                            IS_DAMAGE_UP = False
                            DEALER_OBJ.remainLive -= 1
                            phoneBulletCheck()
                    if not dealerCanContinue:
                        break
                    else:
                        if len(BULLET_LIST) == 0:
                            PLAYER_OBJ.isSkip = False
                            DEALER_OBJ.isSkip = False
                        else:
                            continue 
                # 玩家/庄家是否死亡
                logger.debug(f'庄家回合结束')
                if PLAYER_OBJ.health <= 0:
                    isGameOver = True
                    break
                if DEALER_OBJ.health <= 0:
                    isGameOver = True
                    break
                if DEALER_OBJ.isSkip:
                    tyPrint(LANG_DEALER_BEEN_SKIP,sleepTime=TYPRINT_SPEED_UP*0.1)
                    time.sleep(1)
                    DEALER_OBJ.isSkip = False
                if len(BULLET_LIST) == 0:
                    PLAYER_OBJ.isSkip = False
                    DEALER_OBJ.isSkip = False
                    time.sleep(2)
                    clear(debugMode)
                    tyPrint(LANG_BULLET_RELOADING,sleepTime=TYPRINT_SPEED_UP*0.05)
                    time.sleep(2)
                    # 重新分配道具
                    if len(ALL_ITEM_LIST_STRING) != 0:
                        #itemNumForEach = random.randint(ITEM_RANGE[0],ITEM_RANGE[1])
                        # 分配道具
                        tyPrint(f"{LANG_ITEM_ATHEAD}{cText(itemNumForEach,'yellow')}{LANG_ITEM_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                        time.sleep(1)
                        for i in range(0,itemNumForEach):
                            if len(PLAYER_OBJ.showInventory()) >= 8:
                                # 随机获取一个物品名称来嘲讽玩家
                                playerPickUp = cText(ALL_ITEM_LIST_STRING_TRANS[random.choice(ALL_ITEM_LIST_STRING)],'yellow')
                                tyPrint(LANG_ITEM_OUT_OF_SPACE,sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                                tyPrint(f"{LANG_ITEM_FULL_EXPLANATION_ATHEAD}{playerPickUp}{LANG_ITEM_FULL_EXPLANATION_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                                tyPrint(LANG_HOW_UNFORTUNATE,sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                                break
                            else:
                                playerPickUp = PLAYER_OBJ.addItem()
                                tyPrint(f"{LANG_ITEM_PLAYER_GET_ATHEAD}{cText(ALL_ITEM_LIST_STRING_TRANS[playerPickUp],'yellow')}{LANG_ITEM_PLAYER_GET_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                                time.sleep(1)
                    for i in range(0,itemNumForEach):
                        if len(DEALER_OBJ.showInventory()) >= 8:
                            break
                        else:
                            DEALER_OBJ.addItem()
                    thisLive,thisBlank = bulletDecision()
                    DEALER_OBJ.resetMemory(thisLive,thisBlank)
                    displayDesk(PLAYER_OBJ,DEALER_OBJ,BULLET_LIST,showBullet=True,thisRound=thisRound,totalRound=totalRound,cheatMode=cheatMode)
                    time.sleep(1)
                    tyPrint(f"{LANG_BULLET_SHOW_LIVE_ATHEAD}{cText(thisLive,'red')}{LANG_BULLET_SHOW_LIVE_ATTAIL} {LANG_BULLET_SHOW_BLANK_ATHEAD}{cText(thisBlank,'cyan')}{LANG_BULLET_SHOW_BLANK_ATTAIL}",sleepTime=TYPRINT_SPEED_UP*0.05)
                    time.sleep(5)
                    clear(debugMode)
                    continue
            logger.debug(f'退出生命值归零判断主循环')
            # 走到这里说明主循环被跳出，检查是谁的生命值归零
            # 如果是玩家生命值归零，玩家死亡，主游戏逻辑退出
            # 如果是庄家生命值归零，庄家死亡，进入下一局
            if PLAYER_OBJ.health == 0:
                logger.debug(f'玩家死亡')
                tyPrint(LANG_YOU_DIED)
                isPlayerDeath = 1
                break
            else:
                clear(debugMode)
                logger.debug(f'玩家胜利')
                print(f"{PLAYER_NAME}{LANG_YOU_WIN}")
                isGameOver=False
                continue
        if isPlayerDeath:
            time.sleep(3)
            print("")
            tyPrint(LANG_PLAYER_CONTINUE_DEATH,sleepTime=TYPRINT_SPEED_UP*0.2)
            time.sleep(1)
            print(f"0){LANG_PLAYER_CONTINUE_YES}")
            print(f"1){LANG_PLAYER_CONTINUE_NO}")
            userInput = input(">>>")
            if str(userInput) == '0':
                tyPrint("...",sleepTime=TYPRINT_SPEED_UP*0.1)
                isPlayerDeath = 0
                time.sleep(2)
                clear()
                continue
            else:
                tyPrint("...",sleepTime=TYPRINT_SPEED_UP*0.1)
                time.sleep(2)
                clear()
                break
        else:
            time.sleep(3)
            print("")
            tyPrint(LANG_PLAYER_CONTINUE_ALIVE,sleepTime=TYPRINT_SPEED_UP*0.2)
            time.sleep(1)
            print(f"0){LANG_PLAYER_CONTINUE_YES}")
            print(f"1){LANG_PLAYER_CONTINUE_NO}")
            userInput = input(">>>")
            if str(userInput) == '0':
                tyPrint("...",sleepTime=TYPRINT_SPEED_UP*0.7)
                isPlayerDeath = 0
                time.sleep(2)
                clear(debugMode)
                continue
            else:
                tyPrint("...",sleepTime=TYPRINT_SPEED_UP*0.7)
                time.sleep(debugMode)
                clear()
                break
            