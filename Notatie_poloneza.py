#Functie rang pt ordinea operatiilor
def rang(sign):
    match(sign):
        case "+":
            return 1
        case ".":
            return 2
        case "*":
            return 3
        case "(":
            return 0
        

def ReversePolishNotation(regex :str):
    fin = []
    stack = []
    for x in regex:
        if x.isalpha():
            fin.append(x)
        elif not stack or x == "(":
            stack.append(x)
        elif x == ")":
            act = stack.pop()
            while act != "(":
                fin.append(act)
                act = stack.pop()
        elif rang(x) <= rang(stack[-1]):
            while stack and rang(x) <= rang(stack[-1]):
                fin.append(stack.pop())
            stack.append(x)
        else:
            stack.append(x)

    while stack:
        x = stack.pop()
        fin.append(x)
    return fin
