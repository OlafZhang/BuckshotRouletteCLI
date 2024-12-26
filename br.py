from gameConfig import LANGUAGE,TOTAL_ROUND,debugMode
import os
import time

if LANGUAGE == "zhcn":
    from language_zhcn import *
elif LANGUAGE == "en":
    from language_en import *
else:
    from language_en import *

def clear():
    os.system("cls") if os.name == "nt" else os.system("clear")

clear()
try:
    while True:
        print(f"{LANG_ENTRY_TITLE}")
        print(f"{LANG_ENTRY_SUBTITLE_1}")
        if debugMode:
            print(">Debug mode enabled.<")
        else:
            print("")
        print(f"1) {LANG_ENTRY_SELECT_1}")
        print(f"2) {LANG_ENTRY_SELECT_2}")
        print(f"3) {LANG_ENTRY_SELECT_3}")
        choice = input(">>> ")
        if choice == "1":
            clear()
            print("Developing.../开发中...")
            time.sleep(3)
        elif choice == "2":
            clear()
            from normal import normalGameMainThread
            normalGameMainThread(totalRound=TOTAL_ROUND)
        elif choice == "3":
            clear()
            break
        else:
            pass
        clear()
except KeyboardInterrupt:
    clear()

    