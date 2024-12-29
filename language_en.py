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
    "handSaw":"Handsaw",
    "magnifyingGlass":"Magnifying Glass",
    "handcuffs":"Handcuffs",
    "cigarette":"Cigarette Pack",
    "beer":"Beer",
    "phone":"Burner Phone",
    "adrenaline":"Adrenaline",
    "inverter":"Inverter",
    "expiredMedicine":"Expired Medicine"
}

ALL_ITEM_LIST_EXPLANATION_TRANS = {
    "handSaw":"Shotgun deals 2 damage.",
    "magnifyingGlass":"Check the current round in the chamber.",
    "handcuffs":"Dealer skips the next turn.",
    "cigarette":"Takes the edge off. Regain 1 health.",
    "beer":"Racks the shotgun. Ejects current shell.",
    "phone":"A mysterious voice gives you insight from the future.",
    "adrenaline":"Steal an item and use it immediately.",
    "inverter":"Swaps the polarity of the current shell in the chamber.",
    "expiredMedicine":"50% chance to regain 2 healths.or lose 1 health."
}

LANG_DEALER = "DEALER"
LANG_PLAYER = "YOU"
LANG_SELF = "SELF"
LANG_DEVIL = "DEVIL"

LANG_ENTRY_TITLE = "Buckshot Roulette in CLI"
LANG_ENTRY_SUBTITLE_1 = "Original Author: Mike Klubnika"
LANG_ENTRY_SELECT_1 = "Tutorials Mode(NOT Consume pills)"
LANG_ENTRY_SELECT_2 = "Normal Mode(Consume pills)"
LANG_ENTRY_SELECT_3 = "Exit"

LANG_DESK_YOUR_TURN = "YOUR TURN"
LANG_DESK_DEALER_TURN = "DEALER TURN"
LANG_DESK_DAMAGE_UP = "DAMAGE x2"
LANG_DESK_YOU_BEEN_ATHEAD = "You been"
LANG_DESK_YOU_BEEN_ATTAIL = ""

LANG_SOUND_CLINK = f"*{cText('click','yellow')}*"
LANG_SOUND_BOOM = f"*{cText('BOOM!','red')}*"

LANG_YOU_DIED = "YOU DIED."
LANG_YOU_WIN = " victory!"

LANG_ASK_SIGN_WAIVER = "PLEASE SIGN THE WAIVER."
LANG_SIGN_WAIVER_EXPLANATION = "[Only English name(length in range of 1-6)]:"
LANG_SAY_HELLO_ATHEAD = "WELCOME, "
LANG_SAY_HELLO_ATTAIL = "."
LANG_TAKE_SEAT = "TAKE A SEAT..."
LANG_ENTRY_NEXT_ROUND = "Next round."
LANG_BULLET_LIVE = f"{cText('LIVE','red')}."
LANG_BULLET_BLANK = f"{cText('blank','cyan')}."
LANG_HOW_UNFORTUNATE = "HOW_UNFORTUNATE..."
LANG_HOW_UNFORTUNATE_RED = f"{cText('HOW_UNFORTUNATE...','red')}"
LANG_DEALER_VERY_INTERSTING = f"[{LANG_DEVIL}]：VERY INTERSTING..."
LANG_PLAYER_HAD_USE_HANDSAW = f"You've already used {cText('Handsaw','yellow')}."
LANG_PLAYER_USE_HANDSAW = f"You use your {cText('Handsaw','yellow')}."
LANG_PLAYER_USE_HANDSAW_EXPLANATION = f"Converts the shotgun into a sawed-off shotgun that takes two charges if the shell is {cText('LIVE','red')}."
LANG_PLAYER_USE_MAGNIFYINGGLASS = f"You use your {cText('Magnifying Glass','yellow')}."
LANG_PLAYER_USE_MAGNIFYINGGLASS_EXPLANATION_1 = "Hum..."
LANG_PLAYER_USE_MAGNIFYINGGLASS_EXPLANATION_2 = "You saw a..."
LANG_PLAYER_USE_HANDCUFFS = f"You use your {cText('Handcuffs','yellow')}."
LANG_PLAYER_USE_HANDCUFFS_EXPLANATION = f"{LANG_DEALER} will miss its next turn."
LANG_PLAYER_USE_CIGARETTE = f"You use your {cText('Cigarette Pack','yellow')}."
LANG_PLAYER_USE_CIGARETTE_EXPLANATION = f"Regain {cText('1','green')} health."
LANG_PLAYER_USE_BEER = f"You use your {cText('Beer','yellow')}."
LANG_PLAYER_USE_BEER_EXPLANATION = "Ejecting..."
LANG_PLAYER_USE_PHONE = f"You use your {cText('Burner Phone','yellow')}."
LANG_PLAYER_USE_PHONE_EXPLANATION_ATHEAD = "NO."
LANG_PLAYER_USE_PHONE_EXPLANATION_ATTAIL = " shell is..."
LANG_PLAYER_USE_ADRENALINE = f"You use your {cText('Adrenaline','yellow')}."
LANG_PLAYER_USE_INVERTER = f"You use your {cText('Inverter','yellow')}."
LANG_PLAYER_USE_INVERTER_EXPLANATION = f"The current live shell becomes a blank shell, and vice versa."
LANG_PLAYER_USE_EXPIREDMEDICINE = f"You use your {cText('Expired Medicine','yellow')}."
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_1 = "You..."
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_SUCCESS_ATHEAD = "regain "
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_SUCCESS_ATTAIL = " health."
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_FAIL_ATHEAD = "lose "
LANG_PLAYER_USE_EXPIREDMEDICINE_EXPLANATION_FAIL_ATTAIL = " health."
LANG_DEALER_USE_EXPIREDMEDICINE = f"{LANG_DEVIL} take a {cText('Expired Medicine','yellow')}."
LANG_DEALER_USE_EXPIREDMEDICINE_SUCCESS_ATHEAD = f"{LANG_DEALER} Regain "
LANG_DEALER_USE_EXPIREDMEDICINE_SUCCESS_ATTAIL = " health."
LANG_DEALER_USE_EXPIREDMEDICINE_FAIL = f"{LANG_DEVIL} fainted on the ground."
LANG_DEALER_USE_EXPIREDMEDICINE_FAIL_ATHEAD = f"{LANG_DEALER} lose "
LANG_DEALER_USE_EXPIREDMEDICINE_FAIL_ATTAIL = " health."
LANG_DEALER_USE_CIGARETTE = f"{LANG_DEVIL} inhaled deeply on a {cText('Cigarette','yellow')}, {LANG_DEALER} regain {cText('1','green')} health."
LANG_DEALER_USE_ADRENALINE = f"{LANG_DEVIL} smash an {cText('adrenaline','yellow')} to the ground."
LANG_DEALER_RAP_EXPIREDMEDICINE = f"and steal your {cText('Expired Medicine','yellow')}."
LANG_DEALER_RAP_HANDCUFFS = f"and steal your {cText('Handcuffs','yellow')}."
LANG_DEALER_RAP_PHONE = f"and steal your {cText('Burner Phone','yellow')}."
LANG_DEALER_RAP_BEER = f"and steal your {cText('Beer','yellow')}."
LANG_DEALER_RAP_CIGARETTE = f"and steal your {cText('Cigarette','yellow')}."
LANG_DEALER_RAP_INVERTER = f"and steal your {cText('Inverter','yellow')}."
LANG_DEALER_RAP_HANDSAW = f"and steal your {cText('Handsaw','yellow')}."
LANG_DEALER_RAP_MAGNIFYINGGLASS = f"and steal your {cText('Magnifying Glass','yellow')}."
LANG_DEALER_USE_MAGNIFYINGGLASS = f"{LANG_DEVIL} use a {cText('Magnifying Glass','yellow')}."
LANG_DEALER_USE_PHONE = f"{LANG_DEVIL} {cText('dial','yellow')} to the future."
LANG_DEALER_USE_BEER = f"{LANG_DEVIL} drink a can of {cText('Beer','yellow')} with a shell ejected."
LANG_DEALER_USE_BEER_IS_LIVE = f"That's a {cText('LIVE','red')}."
LANG_DEALER_USE_BEER_IS_BLANK = f"That's a {cText('blank','cyan')}."
LANG_DEALER_USE_HANDCUFFS = f"{LANG_DEVIL} use a {cText('Handcuffs','yellow')} and you been cuffed to the desk."
LANG_DEALER_USE_HANDCUFFS_EXPLANATION = f"You {cText('miss your next turn','red')}."
LANG_DEALER_USE_INVERTER = f"{LANG_DEVIL} smash a {cText('inverter','yellow')} with force."
LANG_DEALER_USE_HANDSAW = f"{LANG_DEVIL} use a {cText('handsaw','yellow')} and turn shotgun into a sawed-off shotgun."
LANG_DEALER_RAISE_GUN = f"{LANG_DEVIL} raise the shotgun."
LANG_DEALER_AIM_YOU = f"{cText('AIM AT YOU','red')}."
LANG_DEALER_AIM_SELF = f"{cText('Aim at self','yellow')}."
LANG_ROUND_THIS_ATHEAD = "Round "
LANG_ROUND_THIS_ATTAIL = ", "
LANG_ROUND_TOTAL_ATHEAD = "Total "
LANG_ROUND_TOTAL_ATTAIL = "."
LANG_ROUND_ATTAIL = ""
LANG_HEALTH_ATHEAD = ""
LANG_HEALTH_ATTAIL = " healths point each."
LANG_ITEM_ATHEAD = ""
LANG_ITEM_ATTAIL = " item(s) each."
LANG_ITEM_OUT_OF_SPACE = f"You are {cText('OUT OF SPACE','red')}."
LANG_ITEM_FULL_EXPLANATION_ATHEAD = "You cannot get the "
LANG_ITEM_FULL_EXPLANATION_ATTAIL = " on the top of prop box."
LANG_ITEM_PLAYER_GET_ATHEAD = "You got a "
LANG_ITEM_PLAYER_GET_ATTAIL = "."
LANG_BULLET_SHOW_LIVE_ATHEAD = ""
LANG_BULLET_SHOW_BLANK_ATHEAD = ""
LANG_BULLET_SHOW_LIVE_ATTAIL = " LIVE"
LANG_BULLET_SHOW_BLANK_ATTAIL = " blank"
LANG_BULLET_RELOADING = "Out of bullets, reloading."
LANG_PLAYER_BEEN_SKIP = f"You {cText('missed your turn','red')}."
LANG_DEALER_BEEN_SKIP = f"{LANG_DEALER} {cText('missed its turn','red')}."
LANG_PLAYER_SELECT_ITEM_OR_SHOOT = f'Enter the item number to use your item in you inventory, enter + to select the target to shoot:'
LANG_PLAYER_SELECT_YES = "Use it."
LANG_PLAYER_SELECT_NO = "Re-select."
LANG_PLAYER_ADRENALINE_FAIL_NOT_ITEM = f"Cannot use the {cText('Adrenaline','yellow')} because the {LANG_DEALER} have not items by now."
LANG_PLAYER_ADRENALINE_SELECT_ITEM = f"Enter the item number to use item in {LANG_DEALER} inventory, press enter without any input to give up and lose your {cText('Adrenaline','yellow')}."
LANG_PLAYER_ADRENALINE_FAIL_ADRENALINE = f"You cannot steal the {cText('Adrenaline','yellow')}."
LANG_PLAYER_ADRENALINE_FAIL_HANDSAW = f"You cannot steal the {cText('Handsaw','yellow')}."
LANG_PLAYER_ADRENALINE_FAIL_HANDCUFFS = f"You cannot steal the {cText('Handcuffs','yellow')}."
LANG_PLAYER_ADRENALINE_FAIL_HANDCUFFS_REASON = f"{LANG_DEALER} had missed its turn,"
LANG_PLAYER_ADRENALINE_FAIL_HANDSAW_REASON = "The shotgun is sawed-off now,"
LANG_AGAIN_IF_SHOT_SELF_BLANK = f"Shooting yourself will skip Dealer's turn if round is {LANG_BULLET_BLANK}."
LANG_PLAYER_AIM_TARGET = f"{cText('SELECT A TARGET','red')}."
LANG_PLAYER_AIM_INPUT = 'Your choice:'
LANG_PLAYER_AIM_TARGET_SELF = "You turned the gun on yourself."
LANG_PLAYER_AIM_TARGET_DEALER = f"You turned the gun on {LANG_DEALER}."
LANG_PLAYER_SHOOT_BLANK = f"The round is {cText('blank','cyan')}."
LANG_PLAYER_SHOOT_LIVE = f"The round is {cText('LIVE','red')}."
LANG_DEALER_SHOOT_BLANK = f"The round is {cText('blank','cyan')}."
LANG_DEALER_SHOOT_LIVE = f"The round is {cText('LIVE','red')}."
LANG_DAMAGE_DEALER_ATHEAD = f"{LANG_DEALER} lose "
LANG_DAMAGE_DEALER_ATTAIL = " health."
LANG_DAMAGE_PLAYER_ATHEAD = "You lose "
LANG_DAMAGE_PLAYER_ATTAIL = " health."

LANG_PLAYER_CONTINUE_ALIVE = "Double or nothing?"
LANG_PLAYER_CONTINUE_DEATH = "RETRY?"
LANG_PLAYER_CONTINUE_YES = "Yes"
LANG_PLAYER_CONTINUE_NO = "No"