# in alfabet lambda va fi notat cu 0
f = open("ex.txt") #fisierul de intrare
# alfabetul va fi scris pe prima linie in .txt
alfabet = [x for x in f.readline().split()]
# pe a 2 a linie sunt scrise starile
stari = set([x for x in f.readline().split()])
# stare initiala
initial = f.readline().strip()
# stari finale
fin = [x for x in f.readline().split()]
d = {}
d_inv = {} # un dictionar invers pt a avea starea anterioara a fiecarei muchii
# de aici se citesc tranzitiile
for linie in f:
    x,y,z = linie.split()
    if x not in d:
        d[x] = {}
    if y not in d_inv:
        d_inv[y] = {}
    if y not in d[x]:
        d[x][y] = z
    else:
        d[x][y] += "+" + z
    if x not in d_inv[y]:
        d_inv[y][x] = z
    else:
        d_inv[y][x] += "+" + z



# Avem toate starile in dictionar de forma d[muchie_act][muchie_urm] = litera + inv lui
# Deja am facut lipirea dreptelor cu acs. nod_urm

#Facem o noua stare finala si una initiala

# ititiala
d["q_initial"] = {initial:"0"}
d_inv[initial]["q_initial"] = "0"

#finala

d_inv["q_final"] = {}

for x in fin:
    d[x]["q_final"] = "0"
    d_inv["q_final"][x] = "0"

# for x in d:
#     print(x)
#     for a,b in d[x].items():
#         print(f"{a}->{b}")

# for x in d_inv:
#     print(x)
#     for a,b in d_inv[x].items():
#         print(f"{a}->{b}")

for act in tuple(stari):
    lit_bucla = ""
    if act in d[act]:
        lit_bucla = d[act][act] if len(d[act][act]) == 1 else "(" + d[act][act] + ")"
    for pred in d_inv[act]:
        if (pred not in stari or pred == act) and (pred != "q_initial" and pred != "q_final"):
            continue
        for urm in d[act]:
            if (urm not in stari or urm == act) and (urm != "q_initial" and urm != "q_final"):
                continue
            # adaugare in d si d_inv noua latura
            # breakpoint()
            if urm not in d[pred]:
                d[pred][urm] = f"({d[pred][act]}){lit_bucla + "*" if lit_bucla else ""}({d[act][urm]})"
                d_inv[urm][pred] = f"({d[pred][act]}){lit_bucla + "*" if lit_bucla else ""}({d[act][urm]})"
            else:
                d[pred][urm] += f"+({d[pred][act]}){lit_bucla + "*" if lit_bucla else ""}({d[act][urm]})"
                d_inv[urm][pred] += f"+({d[pred][act]}){lit_bucla + "*" if lit_bucla else ""}({d[act][urm]})"
    stari.remove(act)
    # breakpoint()

# regex final dar trebuie infrumusetat (prea multe lambdauri si paranteze)
Regex = d["q_initial"]["q_final"]
# print(Regex)
# exit()



ok = 1

while ok == 1:
    ok = 0

    #scotator de paranteze
    i = 1
    while i< len(Regex)-1:
        st = Regex[i-1]
        act = Regex[i]
        dr = Regex[i+1]
        if st+act == "()":
            # breakpoint()
            Regex = Regex[:i-1] + Regex[i+1:]
            ok = 1
            i-=2
        elif st+dr == "()" and act.isalnum():
            # breakpoint()
            #stergere stanga
            Regex = Regex[:i-1] + Regex[i:]
            i-=1
            #stergere dreapta
            Regex = Regex[:i+1] + Regex[i+2:]
            i-=1
            ok = 1
        i+=1

    # breakpoint()
    # print(Regex)
    # exit()


    #stergere dubluri de 0
    i = 1
    while i< len(Regex):
        st = Regex[i-1]
        act = Regex[i]
        if st+act == "00":
            Regex = Regex[:i]+(Regex[i+1:] if i < len(Regex)-1 else "")
            i-=1
            ok = 1
        i+=1

    # print(Regex)
    # exit()


    #stergere zerouri inutile

    i = 0
    while i < len(Regex):
        st = Regex[i-1] if i > 0 else "("
        dr = Regex[i+1] if i+1 < len(Regex) else ")"
        s = st + dr
        if Regex[i] == "0" and s not in ("(+","++","+)"):
            Regex = Regex[:i] + Regex[i+1:]
            i-=1
            ok = 1
        i+=1

    # print(Regex) # f+de*+f+de*(df+de*)*+df+de*+f+de*(df+de*)*r((df+de*)*r)*(df+de*)*+df+de*
    # mai bine dar inca multa redundenta ex: f+de*+f+de* - asta este egal cu f+de*
    # aparent pt ca iau din dictionar valori - este random ce regex primesc la final - uneori este unul foarte scurt, alteori e lung

fara_dup = set()
ultimul_plus = -1
paranteze = 0
for i in range(len(Regex)):
    x = Regex[i]
    if x == "(":
        paranteze+=1
    elif x == ")":
        paranteze-=1
    elif x == "+":
        if paranteze == 0:
            # breakpoint()
            fara_dup.add(Regex[ultimul_plus+1:i])
            ultimul_plus = i
fara_dup.add(Regex[ultimul_plus+1:i+1])
# print(fara_dup)

# Mult mai bine - tot depinde de noroc pt a avea un regex mic dar este de 10 ori mai bine decat de unde am inceput
# Cel mai bun/mic raspuns generat de algoritm pe exemplu: ((f+d))(e+r*(d(f+d)))*(0+r*)
# Inca mai exista redundenta,chiar si in cel mai bun exemplu - (0+r*) poate fi scris doar ca r*, dar macar acum este citibil

print("+".join(fara_dup))