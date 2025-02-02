from openpyxl import load_workbook
from colorama import Fore, Style
import random

min_row = 3

def getData(maxr, sheet,name):
    header = sheet[2]
    columns = {cell.value: col for col, cell in enumerate(header, start=1)}
    idx = columns.get(name)
    if idx:
        return [cell[0] for cell in sheet.iter_rows(min_row, max_row=min_row+maxr-1, min_col=idx, max_col=idx, values_only=True)]

def select():
    opt = input(f"\n[1] - Glagoli\n[2] - Imenice\n[3] - Pridjevi\n[4] - Prijedlozi i ostalo\n[5] - Sve\n[Q] - Quit\nWhat do you want to practice? > ")
    print(f"\n")
    return opt

def reducieren(obj):
    return [entry for entry in obj if entry.get("remove") != "da"]

def play(obj):
    unused = obj.copy()
    used = []
    while unused:
        entry = random.choice(unused)
        used.append(entry)
        inpt = input(f"{Fore.GREEN}Riječ {len(used)}/{len(obj)}: {Fore.BLUE}{entry['translation']} {Style.RESET_ALL}> ")
        if inpt == "q":
            break
        if "verb" in entry:
            print(f"{Fore.GREEN}Glagol: {Fore.YELLOW}{entry['verb']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Prošlost: {Fore.YELLOW}{entry['past']}{Style.RESET_ALL}\n")        
        if "gender" in entry:
            print(f"{Fore.GREEN}Imenica: {Fore.YELLOW}{entry['gender']} {entry['noun']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Množina: {Fore.YELLOW}{entry['plural']}{Style.RESET_ALL}\n")   
        if "word" in entry:
            print(f"{Fore.GREEN}Njemački: {Fore.YELLOW}{entry['word']} {Style.RESET_ALL}\n")
        unused.remove(entry)
        if not unused:
            break

workbook = load_workbook(r"C:\Users\User\OneDrive\Documents\deutsch.xlsx")
sheets = workbook.sheetnames

obj = []
obj_verbs = []
obj_nouns = []
obj_adj = []
obj_adv = []

maxr = int(input(f"Number of words? > "))

for sheet in sheets:
    active = workbook[sheet]
    if sheet == "Glagoli":
        znam = getData(maxr, active, "Znam")
        verbs = getData(maxr, active, "Glagol")
        pasts = getData(maxr, active, "Prošlost")
        trs = getData(maxr, active, "Prijevod")
        for i in range(len(trs)):
            obj_verbs.append({
            "remove": znam[i],
            "verb": verbs[i],
            "past": pasts[i],
            "translation": trs[i]
            })
    if sheet == "Imenice":
        znam = getData(maxr, active, "Znam")
        gndrs = getData(maxr, active, "Rod")
        nouns = getData(maxr, active, "Imenica")
        plrls = getData(maxr, active, "Plural")
        trs = getData(maxr, active, "Prijevod")
        for i in range(len(trs)):
            obj_nouns.append({
            "remove": znam[i],
            "gender": gndrs[i],
            "noun": nouns[i],
            "plural": plrls[i],
            "translation": trs[i]
            })
    if sheet == "Pridjevi":
        znam = getData(maxr, active, "Znam")
        wrds = getData(maxr, active, "Pridjev")
        trs = getData(maxr, active, "Prijevod")
        for i in range(len(trs)):
            obj_adj.append({
            "remove": znam[i],
            "word": wrds[i],
            "translation": trs[i]
            })
    if sheet == "Prilozi":
        wrds = getData(maxr, active, "Prilog")
        trs = getData(maxr, active, "Prijevod")
        znam = getData(maxr, active, "Znam")
        for i in range(len(trs)):
            obj_adv.append({
            "remove": znam[i],
            "word": wrds[i],
            "translation": trs[i]
            })

objs = [obj_verbs, obj_nouns, obj_adj, obj_adv]
obj = [item for sublist in [obj_verbs, obj_nouns, obj_adj, obj_adv] for item in sublist]

while True:
    opt = select()
    if opt == "q":
        break
    elif int(opt) == 5:
        play(obj)
    else:
        play(objs[int(opt)-1])