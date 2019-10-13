import datetime as dt


def Calc_Price_Optim(now,heattime,timearrivehome,timeleavehome,RadPot=11,Gas_Elect=1,Gas_Company=1,
                     Tarifa_Electr=0):
    #######################
    ####VARIABLES D'ENTRADA
    """
    now=dt.datetime.now()
    heattime=dt.time(1,5,0)
    RadPot=14
    #Gas=1 // Electric=2
    Gas_Elect=2
    
    #Endesa=1 // Gas_Nat=2 // Public=3
    Gas_Company=1
    
    #Public_Normal=1 // Public_Discriminacio=2 // Gas=0
    Tarifa_Electr=1
    
    timearrivehome=dt.time(16,30,0)
    timeleavehome=dt.time(12,30,0)
    """
    ########################
    ########################
    
    hora = float(now.hour)    
    minut = float(now.minute)
        
    h_actiu = float(heattime.hour)
    m_actiu = float(heattime.minute)
    
    pot = float(RadPot)
    
    actual = hora + minut/60
    t_actiu = h_actiu + m_actiu/60
    t_inicial = actual
    
    #print("Són les ", hora, ":", minut, "són", actual, "hores")
    
    tipus = int(Gas_Elect)
    
    consum = 0
    preus=[]
    relaciopreus=[]
    
    
    if tipus == 1:
        
        empresa = int(Gas_Company)    
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
        tarifa = int(Tarifa_Electr)
        
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
    h_actiu = int(actual)
    
    h_min = int(timearrivehome.hour)
    h_max = int(timeleavehome.hour)
    
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

#(now,heattime,timearrivehome,timeleavehome,RadPot=11,Gas_Elect=1,Gas_Company=1,Tarifa_Electr=0)
Calc_Price_Optim(now,heattime,dt.time(16,30,0),dt.time(12,30,0),11,2,2,1)