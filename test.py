nbMarchands = int(input())
lstMarchandes = []
for i in range(nbMarchands):
   lstMarchandes.append(int(input()))
lessExp = 10000000
moinscher = 0
print(lstMarchandes)
for i, exp in enumerate(lstMarchandes):
   if exp <= lessExp:
      print(i, exp)
      moinscher = i
print(moinscher)