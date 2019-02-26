Adic={}
Adic.update({"srs": "3"})
Adic.update({"sml": "1"})
Adic.update({"sdm": "6"})
Adic.update({"nyl": "2"})
Adic.update({"szx": "3"})

Adic.update({"ysh": "5"})

print("结果", Adic)
print(Adic.keys())
print(Adic.values())
print(Adic.keys())
print(Adic.values())

Bdic={}

Bdic.update({"nyl": "B"})
Bdic.update({"sml": "A"})
Bdic.update({"srs": "D"})
Bdic.update({"szx": "C"})
Bdic.update({"ysh": "E"})
Bdic.update({"sdm": "F"})
print(Bdic)
print(Bdic.keys())
print(Bdic.values())
print(Bdic.keys())
print(Bdic.values())
list=[]
newList = []
for i in Adic.keys():
    print(i, end=" ")
    list.append((i, Adic.get(i), Bdic.get(i)))
print("")
newList = sorted(list, key=lambda x: (x[1], x[2]))
print(">>>>>>>list is ", newList)
