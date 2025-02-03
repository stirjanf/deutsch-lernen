import pandas as pd
from colorama import Fore, Style
import random
import os

def select():
    os.system('cls')
    print(f"[1] - Glagoli\n[2] - Imenice\n[3] - Pridjevi\n[4] - Prijedlozi i ostalo\n[5] - Sve\n[Q] - Quit")
    while True:
        opt = input(f"What do you want to practice? > ").strip()
        if opt:
            return opt

def play(obj,num):
    os.system('cls')
    unused = obj[:num]
    length = len(unused)
    used = []
    while unused:
        entry = random.choice(unused)
        used.append(entry)
        inpt = input(f"\n{Fore.GREEN}Riječ {len(used)}/{length}: {Fore.BLUE}{entry[-1]} {Style.RESET_ALL}> ")
        if inpt == "q":
            break    
        strng = " - ".join(map(str, entry[1:-1])) 
        print(f"{Fore.YELLOW}{strng}{Style.RESET_ALL}")
        unused.remove(entry)
        if not unused:
            break

sheets = ["Glagoli", "Imenice", "Pridjevi", "Prilozi"]
data = []
nwords = int(input(f"How many words do you want to practice? > "))

for sheet in sheets:
    df = pd.read_excel(r"C:\Users\User\OneDrive\Belgeler\deutsch.xlsx", sheet_name=sheet, header=1)
    words = []
    for index,row in df.iterrows():
        temp = []
        for column_name, value in row.items():
            if "Unnamed" not in column_name:
                if value == "sl":
                    break
                temp.append(str(value).strip())
        if temp:
            words.append(temp)
    data.append(words)

while True:
    opt = select()
    if opt == "q":
        break
    elif int(opt) == 5:
        play(data,nwords)
    else:
        play(data[int(opt)-1],nwords)