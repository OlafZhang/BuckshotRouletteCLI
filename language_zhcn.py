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

ALL_ITEM_LIST_STRING_TRANS = {
    "handSaw":"手锯",
    "magnifyingGlass":"放大镜",
    "handcuffs":"手铐",
    "cigarette":"香烟",
    "beer":"啤酒",
    "phone":"手机",
    "adrenaline":"肾上腺素",
    "inverter":"逆转器",
    "expiredMedicine":"过期药品"
}

ALL_ITEM_LIST_EXPLANATION_TRANS = {
    "handSaw":"将下一次射击伤害提升至2点。",
    "magnifyingGlass":"查看当前的子弹类型。",
    "handcuffs":"跳过庄家1个回合。",
    "cigarette":"回复1点生命值。",
    "beer":"将当前子弹退膛。",
    "phone":"让你预知未来。",
    "adrenaline":"抢走对方的一个物品并立刻使用。",
    "inverter":"逆转当前子弹类型。",
    "expiredMedicine":"50%概率回复2点生命值，或扣除1点生命值。"
}

LANG_DEALER = "庄家"
LANG_PLAYER = "你"
LANG_SELF = "自己"
LANG_DEVIL = "恶魔"

LANG_ENTRY_TITLE = "《恶魔轮盘》命令行版"
LANG_ENTRY_SUBTITLE_1 = "原作者：Mike Klubnika"
LANG_ENTRY_SELECT_1 = "教程模式（不吃药）"
LANG_ENTRY_SELECT_2 = "普通模式（吃药）"
LANG_ENTRY_SELECT_3 = "退出"

LANG_DESK_YOUR_TURN = "你的回合"
LANG_DESK_DEALER_TURN = "对方回合"
LANG_DESK_DAMAGE_UP = "双倍伤害"
LANG_DESK_YOU_BEEN_ATHEAD = "你被"
LANG_DESK_YOU_BEEN_ATTAIL = ""

LANG_SOUND_CLINK = f"*{cText('咔哒','yellow')}*"
LANG_SOUND_BOOM = f"*{cText('嘣！','red')}*"

LANG_YOU_DIED = "你死了。"
LANG_YOU_WIN = " 胜利！"

LANG_ASK_SIGN_WAIVER = "请签署生死状。"
LANG_SIGN_WAIVER_EXPLANATION = "[名字只能为英文，且长度在1-6之间]:"
LANG_SAY_HELLO_ATHEAD = "你好，"
LANG_SAY_HELLO_ATTAIL = "。"
LANG_TAKE_SEAT = "坐下吧..."
LANG_ENTRY_NEXT_ROUND = "进入下一局。"
LANG_BULLET_LIVE = f"{cText('实弹','red')}。"
LANG_BULLET_BLANK = f"{cText('空包弹','cyan')}。"
LANG_HOW_UNFORTUNATE = "真遗憾..."
LANG_HOW_UNFORTUNATE_RED = f"{cText('真遗憾...','red')}"
LANG_DEALER_VERY_INTERSTING = f"[{LANG_DEVIL}]：真有意思..."
LANG_PLAYER_HAD_USE_HANDSAW = f"你已经使用过{cText('手锯','yellow')}了。"
LANG_PLAYER_USE_HANDSAW = f"你使用了{cText('手锯','yellow')}。"
LANG_PLAYER_USE_HANDSAW_EXPLANATION = f"下一次射击伤害提升至2点。(如果射出的是{cText('实弹','red')})"
LANG_PLAYER_USE_MAGNIFYINGGLASS = f"你使用了{cText('放大镜','yellow')}。"
LANG_PLAYER_USE_MAGNIFYINGGLASS_EXPLANATION_1 = "嗯..."
LANG_PLAYER_USE_MAGNIFYINGGLASS_EXPLANATION_2 = "你看到了..."
LANG_PLAYER_USE_HANDCUFFS = f"你使用了{cText('手铐','yellow')}。"
LANG_PLAYER_USE_HANDCUFFS_EXPLANATION = f"庄家回合{cText('将跳过','yellow')}一回合。"
LANG_PLAYER_USE_CIGARETTE = f"你使用了{cText('香烟','yellow')}。"
LANG_PLAYER_USE_CIGARETTE_EXPLANATION = f"你回复了{cText('1','green')}点生命值。"
LANG_PLAYER_USE_BEER = f"你使用了{cText('啤酒','yellow')}。"
LANG_PLAYER_USE_BEER_EXPLANATION = "退了一颗..."
LANG_PLAYER_USE_PHONE = f"你使用了{cText('手机','yellow')}。"
LANG_PLAYER_USE_PHONE_EXPLANATION_ATHEAD = "第"
LANG_PLAYER_USE_PHONE_EXPLANATION_ATTAIL = "发是..."
LANG_PLAYER_USE_ADRENALINE = f"你使用了{cText('肾上腺素','yellow')}。"
LANG_PLAYER_USE_INVERTER = f"你使用了{cText('逆转器','yellow')}。"
LANG_PLAYER_USE_INVERTER_EXPLANATION = f"当前的子弹类型已逆转。"
LANG_PLAYER_USE_EXPIREDMEDICINE = f"你使用了{cText('过期药品','yellow')}。"
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_1 = "你..."
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_SUCCESS_ATHEAD = "回复了"
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_SUCCESS_ATTAIL = "点生命值。"
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_FAIL_ATHEAD = "扣除了"
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_FAIL_ATTAIL = "点生命值。"
LANG_DEALER_USE_EXPIREDMEDICINE = f"{LANG_DEVIL}吃了一颗{cText('过期药品','yellow')}。"
LANG_DEALER_USE_EXPIREDMEDICINE_SUCCESS_ATHEAD = f"{LANG_DEALER}生命值恢复"
LANG_DEALER_USE_EXPIREDMEDICINE_SUCCESS_ATTAIL = "点。"
LANG_DEALER_USE_EXPIREDMEDICINE_FAIL = f"“咚”的一声，{LANG_DEVIL}晕倒在地。"
LANG_DEALER_USE_EXPIREDMEDICINE_FAIL_ATHEAD = f"{LANG_DEALER}生命值扣除"
LANG_DEALER_USE_EXPIREDMEDICINE_FAIL_ATTAIL = "点。"
LANG_DEALER_USE_CIGARETTE = f"{LANG_DEVIL}不紧不慢地点了一根{cText('香烟','yellow')}，{LANG_DEALER}生命值恢复{cText('1','green')}点。"
LANG_DEALER_USE_ADRENALINE = f"{LANG_DEVIL}把{cText('肾上腺素','yellow')}砸在地上。"
LANG_DEALER_RAP_EXPIREDMEDICINE = f"并抢走了你的{cText('过期药品','yellow')}。"
LANG_DEALER_RAP_HANDCUFFS = f"并抢走了你的{cText('手铐','yellow')}。"
LANG_DEALER_RAP_PHONE = f"并抢走了你的{cText('手机','yellow')}。"
LANG_DEALER_RAP_BEER = f"并抢走了你的{cText('啤酒','yellow')}。"
LANG_DEALER_RAP_CIGARETTE = f"并抢走了你的{cText('香烟','yellow')}。"
LANG_DEALER_RAP_INVERTER = f"并抢走了你的{cText('逆转器','yellow')}。"
LANG_DEALER_RAP_HANDSAW = f"并抢走了你的{cText('手锯','yellow')}。"
LANG_DEALER_RAP_MAGNIFYINGGLASS = f"并抢走了你的{cText('放大镜','yellow')}。"
LANG_DEALER_USE_MAGNIFYINGGLASS = f"{LANG_DEVIL}使用了{cText('放大镜','yellow')}。"
LANG_DEALER_USE_PHONE = f"{LANG_DEVIL}用{cText('手机','yellow')}打给了未来。"
LANG_DEALER_USE_BEER = f"{LANG_DEVIL}喝了瓶{cText('啤酒','yellow')}，顺手退了一颗子弹出来。"
LANG_DEALER_USE_BEER_IS_LIVE = f"是一颗{cText('实弹','red')}。"
LANG_DEALER_USE_BEER_IS_BLANK = f"是一颗{cText('空包弹','cyan')}。"
LANG_DEALER_USE_HANDCUFFS = f"{LANG_DEVIL}用{cText('手铐','yellow')}把你拷在了赌桌上。"
LANG_DEALER_USE_HANDCUFFS_EXPLANATION = f"你的下一个回合将会{cText('被跳过','red')}。"
LANG_DEALER_USE_INVERTER = f"{LANG_DEVIL}拼命砸碎了一个{cText('逆转器','yellow')}。"
LANG_DEALER_USE_HANDSAW = f"{LANG_DEVIL}用{cText('手锯','yellow')}把霰弹枪截短了。"
LANG_DEALER_RAISE_GUN = f"{LANG_DEVIL}举起了霰弹枪。"
LANG_DEALER_AIM_YOU = f"{cText('瞄准了你','red')}。"
LANG_DEALER_AIM_SELF = f"{cText('瞄准了自己','yellow')}。"
LANG_ROUND_THIS_ATHEAD = "第"
LANG_ROUND_THIS_ATTAIL = "局，"
LANG_ROUND_TOTAL_ATHEAD = "共"
LANG_ROUND_TOTAL_ATTAIL = "局。"
LANG_ROUND_ATTAIL = "局"
LANG_HEALTH_ATHEAD = "每人 "
LANG_HEALTH_ATTAIL = " 点生命值。"
LANG_ITEM_ATHEAD = "每人 "
LANG_ITEM_ATTAIL = " 件道具。"
LANG_ITEM_OUT_OF_SPACE = f"你的道具箱 {cText('已满','red')}。"
LANG_ITEM_FULL_EXPLANATION_ATHEAD = "你望着道具箱最上面的"
LANG_ITEM_FULL_EXPLANATION_ATTAIL = "干瞪眼。"
LANG_ITEM_PLAYER_GET_ATHEAD = "你获得了 "
LANG_ITEM_PLAYER_GET_ATTAIL = "。"
LANG_BULLET_SHOW_LIVE_ATHEAD = "实弹"
LANG_BULLET_SHOW_BLANK_ATHEAD = "空包弹"
LANG_BULLET_SHOW_LIVE_ATTAIL = "颗"
LANG_BULLET_SHOW_BLANK_ATTAIL = "颗"
LANG_BULLET_RELOADING = "子弹打空，重新装填。"
LANG_PLAYER_BEEN_SKIP = f"你的回合被{cText('跳过','red')}。"
LANG_DEALER_BEEN_SKIP = f"{LANG_DEALER}回合被{cText('跳过','red')}。"
LANG_PLAYER_SELECT_ITEM_OR_SHOOT = f'请输入你的道具编号来使用道具，输入+来选择射击目标:'
LANG_PLAYER_SELECT_YES = "确定使用"
LANG_PLAYER_SELECT_NO = "重新选择"
LANG_PLAYER_ADRENALINE_FAIL_NOT_ITEM = f"{LANG_DEALER}没有物品，无法使用{cText('肾上腺素','yellow')}。"
LANG_PLAYER_ADRENALINE_SELECT_ITEM = f"选择{LANG_DEALER}的物品编号，直接按下回车表示放弃使用并丢弃肾上腺素："
LANG_PLAYER_ADRENALINE_FAIL_ADRENALINE = f"{cText('不可以','red')}抢走{cText('肾上腺素','yellow')}。"
LANG_PLAYER_ADRENALINE_FAIL_HANDSAW = f"{cText('不可以','red')}抢走{cText('手锯','yellow')}。"
LANG_PLAYER_ADRENALINE_FAIL_HANDCUFFS = f"{cText('不可以','red')}抢走{cText('手铐','yellow')}。"
LANG_PLAYER_ADRENALINE_FAIL_HANDCUFFS_REASON = f"{LANG_DEALER}回合已经被跳过，"
LANG_PLAYER_ADRENALINE_FAIL_HANDSAW_REASON = "当前伤害已经翻倍，"
LANG_AGAIN_IF_SHOT_SELF_BLANK = "如果自己开枪射向自己的子弹是空包弹，则还可以再射击一次。"
LANG_PLAYER_AIM_TARGET = f"{cText('选择一个目标','red')}。"
LANG_PLAYER_AIM_INPUT = '你的选择：'
LANG_PLAYER_AIM_TARGET_SELF = "你把枪口朝向了自己。"
LANG_PLAYER_AIM_TARGET_DEALER = "你把枪口朝向了庄家。"
LANG_PLAYER_SHOOT_BLANK = f"你打出了 {cText('空包弹','cyan')}。"
LANG_PLAYER_SHOOT_LIVE = f"你打出了 {cText('实弹','red')}。"
LANG_DEALER_SHOOT_BLANK = f"{LANG_DEALER}打出了 {cText('空包弹','cyan')}。"
LANG_DEALER_SHOOT_LIVE = f"{LANG_DEALER}打出了 {cText('实弹','red')}。"
LANG_DAMAGE_DEALER_ATHEAD = f"{LANG_DEALER}受到了 "
LANG_DAMAGE_DEALER_ATTAIL = " 点伤害。"
LANG_DAMAGE_PLAYER_ATHEAD = "你受到了 "
LANG_DAMAGE_PLAYER_ATTAIL = " 点伤害。"

LANG_PLAYER_CONTINUE_ALIVE = "加倍还是放弃？"
LANG_PLAYER_CONTINUE_DEATH = "重新开始？"
LANG_PLAYER_CONTINUE_YES = "是"
LANG_PLAYER_CONTINUE_NO = "否"