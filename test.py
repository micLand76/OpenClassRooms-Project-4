a = int(input())
b = []
for loop in range(a):
   b.append(int(input()))
   b.append(int(input()))
   b.append(int(input()))
   b.append(int(input()))

for i in range(a):
   print(int(b[0+4*i])+int(b[2+4*i])*int(b[3+4*i]))
