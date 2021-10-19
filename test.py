nb_paires = int(input())
for i in range(nb_paires):
   a1 = int(input())
   a2 = int(input())
   a3 = int(input())
   a4 = int(input())
   b1 = int(input())
   b2 = int(input())
   b3 = int(input())
   b4 = int(input())
   if (a1>b1 and a1<b2 and ((a3>b3 and a3<b4) or (a4>b3 and a4<b4))) or (a2>b1 and a2<b2 and ((a4>b3 and a4<b4) or (a3>b3 and a3<b4))) or (b1>a1 and b1<a2 and ((b3>a3 and b3<a4) or (b4>a3 and b4<a4))) or (b2>a1 and b2<a2 and ((b4>a3 and b4<a4) or (b3>a3 and b3<a4))):
      print('OUI')
   else:
      print('NON')