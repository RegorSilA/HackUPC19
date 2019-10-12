hora = float(input("Hora: "))
while (hora>=24.0)or(hora<0.0):
    print("Format de hora erroni")
    hora = float(input("Hora: "))
    
minut = float(input("Minut: "))
while (minut>=60.0)or(minut<0.0):
    print("Format de minut erroni")
    minut = float(input("Minut: "))
    
h_actiu = float(input("Quantes hores ho vols tenir encès?"))
m_actiu = float(input("Quants minuts ho vols tenir encès?"))

pot = float(input("Quina potencia té el teu radiador? (En kW): "))

actual = hora + minut/60
t_actiu = h_actiu + m_actiu/60
t_inicial = actual

print("Són les ", hora, ":", minut, "són", actual, "hores")

tipus = int(input("Quin tipus de calefacció utilitzes? (Gas=1, Electric=2) "))
while (tipus != 1 and tipus != 2):
    tipus = int(input("Format incorrecte. (Gas=1, Electric=2) "))

consum = 0
preus=[]
relaciopreus=[]


if tipus == 1:
    
    empresa = int(input("Quina empresa tens contractada? (Endesa=1, Gas Natural= 2, Public=3) "))
    while (tipus != 1 and tipus != 2):
        empresa = int(input("Format incorrecte. (Endesa=1, Gas Natural= 2, Public=3) "))
    
    c = 0

    with open('tarifa_gas.txt', 'r') as inputFile:
            
        for preu in inputFile.readlines():
            preus.append(preu)
            lineStripped = preu.strip()
            taxa = lineStripped.split(';')
            relaciopreus.append(float(taxa[1]))
            c = c+1

    inputFile.close()
    
    consum = consum + t_actiu*relaciopreus[int(empresa)-1]*pot
    print("Has gastat", consum, "euros")

else:
    tarifa = int(input("Quin tarifa utilitzes? (Public Normal=1, Public Discriminacio=2) "))
    while (tarifa != 1 and tarifa != 2):
        tarifa = int(input("Format incorrecte. (Public Normal=1, Public Discriminacio=2) "))
    
    primera_dif = float(int(actual)+1) - actual

    c = 0

    with open('tarifa_gen.txt', 'r') as inputFile:
            
        for preu in inputFile.readlines():
            if c >= (2+28*(int(tarifa)-1)) and c <=(25+28*(int(tarifa)-1)):
                preus.append(preu)
                lineStripped = preu.strip()
                taxa = lineStripped.split(';')
                floataxa= float(taxa[1])
                relaciopreus.append(floataxa)
            c = c+1
    inputFile.close()
    
    if primera_dif<t_actiu:
        consum = consum + primera_dif*relaciopreus[int(actual)]
        actual = float(int(actual) + 1)
        cont= 0
        while(((t_actiu-actual+t_inicial)>=1) and cont<25):
            cont += 1 
            consum = consum + relaciopreus[int(actual)]*pot

            actual = float(int(actual) + 1)
            if actual >= 24.0:
                actual = 0.0
        consum = consum + (t_actiu+t_inicial-actual)*relaciopreus[int(actual)]*pot
        print("Has gastat", consum, "euros")
    
    else:
        consum = consum + t_actiu*relaciopreus[int(actual)]*pot
        print("Has gastat", consum, "euros")

    
        
#PROGRAMA D'ESTALVI ECONÒMIC

h_actiu = int(input("Quantes hores vols engegar la calefacció avui? "))

h_min = int(input("A quina hora arribes a casa? "))
h_max = int(input("A quina hora sortiràs de casa? "))

if h_max>h_min:
    diff = int(h_max-h_min)
else:
    diff = int(24+h_max-h_min)

calcul = []
if diff<h_actiu:
    print("Necessites engegar la calefacció menys hores de les que estaràs a casa!")
else:
    if tipus == 2:
        for j in range (0, diff-h_actiu):
            comput = 0
            counter = 0
            h_actual = h_min+j
            if h_actual>=24:
                h_actual = h_actual-24
            for i in range (0, h_actiu):
                if h_actual>=24:
                    h_actual = 0
                comput = comput + relaciopreus[int(h_actual)]

                h_actual = h_actual + 1
        calcul.append(comput)
        minim = min(calcul)
        print(minim)
    else:
        print("Si utilitzes gas no es pot optimitzar!")

            
            