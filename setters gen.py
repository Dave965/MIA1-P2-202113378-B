'''while True:
    s = input()
    
'''

s = input()
s = [x.strip() for x in s.split(",")]

for i in s:
    print("def setI"+i[1:]+"(self, "+i+"):\n        self."+i+" = "+i+"\n")

print()
for i in s:
    print('setI'+i[1:]+"("+i+")")

