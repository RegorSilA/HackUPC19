import numpy as np
import time
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D



def TTiming(Temp):
    start_time = time.time()
    ####DADES
    #[En metres]
    PasX=1
    PasY=1
    
    #[En Metres]
    LX=20
    LY=10
    
    SizeRoom=np.array([LX,LY])
    
    TAmb=20
    TRad=70
    Funci=0
    TObj=26
    Error=0.5
    
    #Radiator-Room Size
    RelSizSauX=5
    RelSizSauY=5
    
    
    ####POT DEPENDRE DEL TEMPS
    KappaT=1.9*10**-3.2
    ####
    PasSecs=5
    
    
    #Array de tamany = num cel·les
    RoomOrig=np.zeros((int(LX/PasX),int(LY/PasY)))
    SizeArray=RoomOrig.shape
    
    #SumInvPasQua=(((1/PasX)**2)+((1/PasX)**2))
    PasXQua=PasX**2
    PasYQua=PasY**2
    InvPasXQua=1/PasXQua
    InvPasYQua=1/PasYQua
    
    InvSumInvPasQua=1/(2*((1/PasXQua)+(1/PasYQua)))
    
    #Prepare Room (+Walls)
    RoomM=np.copy(RoomOrig)
    RoomM[:,:]=TAmb
    
    TWalls=TAmb+3
    RoomM[0,:]=TWalls
    RoomM[-1,:]=TWalls
    RoomM[:,0]=TWalls
    RoomM[:,-1]=TWalls
    
    
    #Create representation of sources
    SizeSauce=(np.asarray((LX/RelSizSauX,LY/RelSizSauY))/2).astype(int)
    RSauces=np.copy(RoomOrig)
    LXpart2=int((LX/PasX)/2)
    LYpart2=int((LY/PasY)/2)
    
        
    RSauces[0:SizeSauce[0]+1,LYpart2-SizeSauce[1]:LYpart2+SizeSauce[1]]=TRad
    
    IsSauce=RSauces!=0
    
    RoomM[IsSauce]=TRad
    
    MeanedRoom=np.copy(IsSauce)
    MeanedRoom[0,:]=True
    MeanedRoom[-1,:]=True
    MeanedRoom[:,0]=True
    MeanedRoom[:,-1]=True
    
    RoomMN=np.copy(RoomM)
    Condi=True
    cont=0
    Sx=KappaT*PasSecs*InvPasXQua
    Sy=KappaT*PasSecs*InvPasYQua
    
    while Condi:
        cont+=1
        
        for x in range(1,int(RoomOrig[:,0].size-1)):
            for y in range(1,int(RoomOrig[0,:].size-1)):
                
                RoomMN[x,y]=RoomM[x,y]+Sx*(RoomM[x-1,y]+RoomM[x+1,y]-2*RoomM[x,y])+ \
                                       Sy*(RoomM[x,y-1]+RoomM[x,y+1]-2*RoomM[x,y])
                                       
                RoomMN[IsSauce]=TRad    
                                       
        TMitj=np.mean(RoomMN[~MeanedRoom])
                                       
        RoomMN[~MeanedRoom]=TMitj
                                       
        Diff=TMitj-TWalls
                                       
        if Diff > 0:
            TWalls += Diff/1500
                                           
        RoomMN[0,:]=TWalls
        RoomMN[-1,:]=TWalls
        RoomMN[:,0]=TWalls
        RoomMN[:,-1]=TWalls

    
        if ((TObj-RoomMN[LXpart2,LYpart2])<Error)or(cont>10000):
            Condi=False
        
        RoomM=RoomMN
    
    return str(dt.timedelta(seconds=cont*PasSecs))

print(TTiming(27))
        
        