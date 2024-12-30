# 语言设置
# Language setting
# 'zhcn','en' 
LANGUAGE = 'zhcn'

# typrint方法的全局变速值，小于1表示加速
# Global speed var in Method: typrint() , less than 1 means print faster.
TYPRINT_SPEED_UP = 0.5

# 双方生命值的取值范围
# Range of health value for both sides
HEALTH_RANGE = [2,4]

# 双方在新的一轮/子弹打空后，拿到的物品数量的取值范围
# Range of item value for both sides in new round/while bullet reloading
ITEM_RANGE = [2,4]

# 游戏局数
# Game rounds
TOTAL_ROUND = 3

# 是否开启子弹随机选择
# Enable random bullet selection or not
USE_RANDOM_BULLET = False

# 不使用子弹随机选择时，预设的子弹排列组合
# [真弹数，空包弹数]
# The preset bullet arrangement when not using random bullet selection.
# [live, blank]
INIT_BULLET_LIST = [[3,2],[1,1],[4,4],[2,3],[1,3],[2,4]]

# 是否启动debug日志输出(beta)，目前仅支持中文且输出内容有限
# Enable debug log output(beta) 
# will output limited content in Chinese for now.
debugMode = False