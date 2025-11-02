from Notatie_poloneza import ReversePolishNotation as pol 
# am facut transformarea in forma poloneza in alt fisier pt a nu aglomera
v_REGEX = 'a.(a+b)*.b'
# ['a', 'a', 'b', '+', '*', '.', 'b', '.']
RegEx = pol(v_REGEX) #Exemplu de regex
symbols = {"+",".","*"}

#Trecem prin litere si le transformam in nfa  -- pastram intr-un tuplu doar nodul de start si cel final

i = 0 # contor noduri
d = {} # dictionar dublu d[nod][muchie] = nod_urmator
act = [] # lista cu nfa-uri partiale

# transform toate literele in nfa-uri

for x in RegEx:
    if x in symbols:
        act.append(x)
        continue
    d[f"q{i}"] = {}
    d[f"q{i+1}"] = {}
    d[f"q{i}"][x] = f"q{i+1}"
    act.append((f"q{i}",f"q{i+1}"))
    i+=2



while len(act) > 1:    # daca are un singur element inseamna ca nu mai e partial
    for j in range(len(act)):
        x = act[j]
        if x not in symbols:
            continue
        match x:
            case "+":
                a = act[j-1]
                b = act[j-2]
                d[f"q{i}"] = { "lambda":(a[0],b[0]) }
                d[f"q{i+1}"] = {}
                d[a[1]]["lambda"] = f"q{i+1}"
                d[b[1]]["lambda"] = f"q{i+1}"
                act.remove(b)
                act.remove(a)
                act[j-2] = (f"q{i}",f"q{i+1}")
                i+=2
                break
            case "*":
                a = act[j - 1]
                d[f"q{i + 1}"] = {}
                d[f"q{i}"] = { "lambda": (a[0],f"q{i+1}") }
                d[a[1]]["lambda"] = (f"q{i}",f"q{i+1}")
                act.remove(a)
                act[j-1] = (f"q{i}",f"q{i+1}")
                i+=2
                break
            case ".":
                a = act[j - 2]
                b = act[j - 1]
                d[f"q{i}"] = { "lambda":a[0] }
                d[a[1]]["lambda"] = b[0]
                act.remove(b)
                act.remove(a)
                act[j-2] = (f"q{i}",b[1])
                i+=1
                break

print(f"Starea initiala este {act[0][0]}")
print(f"Starea finala este {act[0][1]}")
print("Starile sunt:")
print(d)


