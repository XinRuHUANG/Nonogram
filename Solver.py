import pprint as pp

#CONTRAINTES L/C (à compléter à la main)
L = {0: ['7'], 1: ['3a', '3b'], 2: ['1a', '1b'], 3: ['3'], 4: ['1a', '3', '1b'], 5: ['1', '6'], 6: ['3', '5'], 7: ['4'], 8: ['1', '5'], 9: ['1a', '1b']}
C = {0: ['3a', '3b'], 1: ['2', '1a', '1b'], 2: ['2', '1'], 3: ['1', '3'], 4: ['2', '6'], 5: ['2', '6'], 6: ['2', '6'], 7: ['2', '1'], 8: ['2', '1'], 9: ['1', '2']}

#DICT SOL
S = {n:[] for n in range(len(L))}
for n in range(len(L)):
    S[n]+=["?"]*len(C)

#TABLEAU ETAT
Etat_L = {i: {} for i in range(len(L))}
for i in range(len(L)):
    Etat_L[i][L[i][0]]=[0]
    for k in range(1,len(L[i])):
        Etat_L[i][L[i][k]]=[Etat_L[i][L[i][k-1]][0]+int(L[i][k-1][0])+1]
    Etat_L[i][L[i][-1]].append(len(C)-1)
    for k in range(len(L[i])-2,-1,-1):
        Etat_L[i][L[i][k]].append(Etat_L[i][L[i][k+1]][1]-int(L[i][k+1][0])-1)

Etat_C = {j: {} for j in range(len(C))}
for i in range(len(C)):
    Etat_C[i][C[i][0]]=[0]
    for k in range(1,len(C[i])):
        Etat_C[i][C[i][k]]=[Etat_C[i][C[i][k-1]][0]+int(C[i][k-1][0])+1]
    Etat_C[i][C[i][-1]].append(len(L)-1)
    for k in range(len(C[i])-2,-1,-1):
        Etat_C[i][C[i][k]].append(Etat_C[i][C[i][k+1]][1]-int(C[i][k+1][0])-1)

#TESTE
def NonResolu(S):
    Bol = False
    i,j = 0,0
    while i<len(S) and not Bol:
        while j < len(S[0]) and not Bol:
            if "?" in S[i][j]: Bol = True
            j+=1
        i+=1
    return Bol

#ZONES CROISES
def IndicesCroiseesLigne(L,i,k1,k2): #k1,k2 inclus
    I=[]
    for k in range(k1,k2+1):
        x=(Etat_L[i][L[i][k]][1]-Etat_L[i][L[i][k]][0]+1)-int(L[i][k][0]) #EspacesRestants
        if int(L[i][k][0])>x:
            for d in range(int(L[i][k][0])-x):
                S[i][Etat_L[i][L[i][k]][0]+x+d]=1
    return S

def IndicesCroiseesColonne(C,i,k1,k2):
    I=[]
    for k in range(k1,k2+1):
        x=(Etat_C[i][C[i][k]][1]-Etat_C[i][C[i][k]][0]+1)-int(C[i][k][0]) #EspacesRestants
        if int(C[i][k][0])>x:
            for d in range(int(C[i][k][0])-x):
                S[Etat_C[i][C[i][k]][0]+x+d][i]=1
    return S

#REMPLISSAGE
def RemplissageExtremites(S):
    #Ligne
    for i in range(len(L)):
        j=0
        while j<len(C) and S[i][j]!=1:
            j+=1
        if j<int(L[i][0]):
            for k in range(j+1,int(L[i][0])-j):
                S[i][k]=1
        j=len(C)-1
        while j>-1 and S[i][j]!=0:
            j-+1
        if len(C)-1-j<int(L[i][-1]):
            for k in range(len(C)-1-int(L[i][-1]),j):
                S[i][k]=1
    #Colonne
    for j in range (len(C)):
        i=0
        while i<len(L) and S[i][j]!=1:
            i+=1
        if i<int(C[j][0]):
            for k in range(i+1, int(C[j][0])-i):
                S[k][j]=1
        i=len(L)-1
        while i>-1 and S[i][j]!=0:
            i-+1
        if len(L)-1-i<int(C[j][-1]):
            for k in rang(len(L)-1-int(C[j][-1]),i):
                S[k][j]=1
    return S

def RemplissageLigne(L,i,k1,k2): #k1,k2 inclus
    BlocsPossibles = {i:[]}
    for p in range(len(Etat_L[i])):
        if k1+1<=Etat_L[i][L[i][p]][0] and k2-1>=Etat_L[i][L[i][p]][1]:
            BlocsPossibles[i].append(L[i][p])
    #Intervalle vide
    if len(BlocsPossibles[i])==0:
        for k in range((k2-1)-(k1+1)):
            S[i][k1+1+k]=0
    else:
        S=IndicesCroisees(BlocsPossibles,i,k1+1,k2-1)
    return S

def RemplissageColonne(C,i,k1,k2): #k1,k2 inclus
    BlocsPossibles = {i:[]}
    for p in range(len(Etat_C[i])):
        if k1<=Etat_C[i][C[i][p]][0] and k2>=Etat_C[i][C[i][p]][1]:
            BlocsPossibles[i].append(C[i][p])
    #Intervalle vide
    if len(BlocsPossibles[i])==0:
        for k in range(k2-k1+1):
            S[k1+k][i]=0
    else:
        S=IndicesCroisees(BlocsPossibles,i,k1,k2)
    return S


#ACTUALISATION TABLEAU ETAT
def ActualiserEtat(Etat_L,Etat_C):
    for i in range(len(L)):
        #Présence de croix et Espace insuffisant
        for p in range(len(L[i])):
            k=0
            while k<len(Etat[i][L[i][p]]):
                j=Etat[i][L[i][p]][k]
                while j<Etat_L[i][L[i][p]][k+1] and S[i][j]!=0:
                    j+=1
                if j<Etat_L[i][L[i][p]][k+1]:
                    #Réduction de l'intervalle
                    if j-Etat_L[i][L[i][p]][k]<int(L[i][p]):
                        Etat_L[i][L[i][p]][0]=j+1
                    elif Etat_L[i][L[i][p]][1]-j<int(L[i][p]):
                        Etat_L[i][L[i][p]][1]=j-1
                    #Ajout d'un nouveau intervalle
                    else:
                        for d in range(len(Etat[i][L[i][p]])+1,k+2,-1):
                            Etat_L[i][L[i][p]][d]=Etat_L[i][L[i][p]][d-2]
                        Etat_L[i][L[i][p]][k+2]=j+1
                        Etat_L[i][L[i][p]][k+1]=j-1
                k+=2
    for i in range(len(C)):
        #Présence de croix et Espace insuffisant
        for p in range(len(C[i])):
            k=0
            while k<len(Etat[i][C[i][p]]):
                j=Etat[i][C[i][p]][k]
                while j<Etat_C[i][C[i][p]][k+1] and S[j][i]!=0:
                    j+=1
                if j<Etat_C[i][C[i][p]][k+1]:
                    #Réduction de l'intervalle
                    if j-Etat_C[i][C[i][p]][k]<int(C[i][p]):
                        Etat_C[i][C[i][p]][0]=j+1
                    elif Etat_C[i][C[i][p]][1]-j<int(C[i][p]):
                        Etat_C[i][C[i][p]][1]=j-1
                    #Ajout d'un nouveau intervalle
                    else:
                        for d in range(len(Etat[i][C[i][p]])+1,k+2,-1):
                            Etat_C[i][C[i][p]][d]=Etat_C[i][C[i][p]][d-2]
                        Etat_C[i][C[i][p]][k+2]=j+1
                        Etat_C[i][C[i][p]][k+1]=j-1
                k+=2
    return Etat_L, Etat_C

#RECHERCHE CROIX
def RechercheBlocsFinis(L,C,Etat_L,Etat_C):
    #Ligne
    for i in range(len(L)):
        j=0
        while j<len(C):
            while j<len(C) and S[i][j]!=1:
                j+=1
            k=j
            while k<len(C) and S[i][k]==1:
                k+=1

            #Recherche de Blocs susceptibles d'être présents
            BlocsPossibles = []
            for p in range(len(Etat_L[i])):
                if j>=Etat_L[i][p][0] and k<=Etat_L[i][p][1]:
                    BlocsPossibles.append(Etat_L[i][p])
            if len(BlocsPossibles)==1:
                if int(BlocsPossibles[0][0])==k-j-1:
                    Etat_L[i][BlocsPossibles[0]][0]=j
                    Etat_L[i][BlocsPossibles[0]][1]=k-1
                    if j!=0: S[i][j]=0
                    if k!=len(C)-1: S[i][k]=0
            j=k+1
    #Colonne
    for i in range(len(C)):
        j=0
        while j<len(L):
            while j<len(L) and S[j][i]!=1:
                j+=1
            k=j
            while k<len(L) and S[k][i]==1:
                k+=1

            #Recherche de Blocs susceptibles d'être présents
            BlocsPossibles = []
            for p in range(len(Etat_C[i])):
                if j>=Etat_C[p][i][0] and k<=Etat_C[p][i][1]:
                    BlocsPossibles.append(Etat_C[p][i])
            if len(BlocsPossibles)==1:
                if int(BlocsPossibles[0][0])==k-j-1:
                    Etat_C[i][BlocsPossibles[0]][0]=j
                    Etat_C[i][BlocsPossibles[0]][1]=k-1
                    if j!=0: S[j][i]=0
                    if k!=len(L)-1: S[k][i]=0
            j=k+1
    return S

def RechercheIntervalleNonAtteignableLigne(L, Etat_L, i):
    Int={0:Etat_L[0]} #Intervalles atteignables
    for k in range(1, len(Etat_L[i])):
        for p in range(len(Int)):
            if Etat_L[i][k][0]<Int[p][0] and Etat_L[i][k][1]<Int[p][1]:
                Int[p][0]=Etat_L[i][k][0]
            elif Etat_L[i][k][1]>Int[p][1] and Etat_L[i][k][0]>Int[p][0]:
                Int[p][1]=Etat_L[i][k][1]
            elif Etat_L[i][k][0]<Int[p][0] and Etat_L[i][k][1]>Int[p][1]:
                Int[p][0]=Etat_L[i][k][0]
                Int[p][1]=Etat_L[i][k][1]
            elif Etat_L[i][k][1]<Int[p][0]:
                #Décalage des clés dans Int
                for d in range(len(Int),p+2,-1):
                    Int[d]=Int[d-1]
                Int[p]=Etat_L[i][k]
            elif Etat_L[i][k][0]>Int[p][1] and p==len(Int)-1:
                #Ajout d'un nouveau intervalle
                Int.append[Etat_L[i][k]]
    #Remplissage de croix
    if Int[0][0]!=0:
        for k in range(Int[0](0)):
            S[i][k]=0
    for p in range(len(Int)-1):
        if Int[p][1]<Int[p+1][0]:
            for k in range(Int[p][1]+1,Int[p+1][0]):
                S[i][k]=0
    return S

def RechercheIntervalleNonAtteignableColonne(C, Etat_C, i):
    Int={0:Etat_C[0]} #Intervalles atteignables
    for k in range(1,len(Etat_C[i])):
        for p in range(len(Int)):
            if Etat_C[i][k][0]<Int[p][0] and Etat_C[i][k][1]<Int[p][1]:
                Int[p][0]=Etat_C[i][k][0]
            elif Etat_C[i][k][1]>Int[p][1] and Etat_C[i][k][0]>Int[p][0]:
                Int[p][1]=Etat_C[i][k][1]
            elif Etat_C[i][k][0]<Int[p][0] and Etat_C[i][k][1]>Int[p][1]:
                Int[p][0]=Etat_C[i][k][0]
                Int[p][1]=Etat_C[i][k][1]
            elif Etat_C[i][k][1]<Int[p][0]:
                #Décalage des clés dans Int
                for d in range(len(Int),p+2,-1):
                    Int[d]=Int[d-1]
                Int[p]=Etat_C[i][k]
            elif Etat_C[i][k][0]>Int[p][1] and p==len(Int)-1:
                #Ajout d'un nouveau intervalle
                Int.append[Etat_C[i][k]]
    #Remplissage de croix
    if Int[0][0]!=0:
        for k in range(Int[0](0)):
            S[k][i]=0
    for p in range(len(Int)-1):
        if Int[p][1]<Int[p+1][0]:
            for k in range(Int[p][1]+1,Int[p+1][0]):
                S[k][i]=0
    return S


def SeparationLigne(L,i):
    j=0
    while j<len(C)-2:
        while j<len(C)-2 and not (S[i][j]==1 and S[i][j+1]==0 and S[i][j+2]==1): j+=1
        if j<len(C)-2:
            #Evaluation des longueurs des blocs
            g=0
            while S[i][j-g]==1: g+=1
            d=0
            while S[i][j+2+d]==1: d=+1

            BlocsPossibles = []
            for p in range(len(Etat_L[i])):
                if j-g+1>=Etat_L[i][p][0] and j+d+1<=Etat_L[i][p][1]:
                    BlocsPossibles.append(Etat_L[i][p])
            k=0
            while k<len(BlocsPossibles) and g+d+1>int(BlocsPossibles[k][0]):
                k+=1
            if k==len(BlocsPossibles):
                S[i][j+1]=0
        j+=d
    return S

def SeparationColonne(C,i):
    j=0
    while j<len(L)-2:
        while j<len(L)-2 and not (S[j][i]==1 and S[j+1][i]==0 and S[j+2][i]==1):
            j+=1
        if j<len(L)-2:
            #Evaluation des longueurs des blocs
            g=0
            while S[j-g][i]==1:
                g+=1
            d=0
            while S[j+2+d][i]==1:
                d=+1

            BlocsPossibles = []
            for p in range(len(Etat_C[i])):
                if j-g+1>=Etat_C[i][p][0] and j+d+1<=Etat_C[i][p][1]:
                    BlocsPossibles.append(Etat_C[i][p])
            k=0
            while k<len(BlocsPossibles) and g+d+1>int(BlocsPossibles[k][0]):
                k+=1
            if k==len(BlocsPossibles):
                S[j+1][i]=0
        j+=d
    return S


#SOLVER
def Solver(L,C):
    #Première recherche naïve
    for i in range(len(L)):
        S=IndicesCroiseesLigne(L,i,0,len(C)-1)
    for j in range(len(C)):
        S=IndicesCroiseesColonne(C,j,0,len(L)-1)

    #Replissage des extrémités
    S = RemplissageExtremites(S)

    #Recherche de croix
    S = RechercheBlocsFinis(L,C,Etat_L,Etat_C)
    for i in range(len(L)):
        S = RechercheIntervalleNonAtteignableLigne(L,Etat_L,i)
    for j in range(len(C)):
        S = RechercheIntervalleNonAtteignableColonne(C, Etat_C,i)
    Etat_L, Etat_C = ActualiserEtat(Etat_L, Etat_C)

    while NonResolu(S):
        #Remplissage
        for i in range(len(L)):
            k1, k2 = 0, 1
            while k2<len(C):
                while k2<len(C) and S[i][k2]!=0:
                    k2+=1
                S = RemplissageLigne(L,i,k1,k2-1)
                k1, k2 = k2+1, k2+2
        for j in range(len(C)):
            while k2<len(L):
                k1, k2 = 0, 1
                while k2<len(L) and S[k2][j]!=0:
                    k2+=1
                S = RemplissageColonne(C,j,k1,k2-1)
                k1, k2 = k2+1, k2+2
        #Recherche de croix
        S = RechercheBlocsFinis(L, C, Etat_L, Etat_C)
        for i in range(len(L)):
            S = RechercheIntervalleNonAtteignableLigne(L,Etat_L,i)
            S = SeparationLigne(L,i)
        for j in range(len(C)):
            S = RechercheIntervalleNonAtteignableColonne(C, Etat_C,i)
            S = SeparationColonne(C,j)

        #Actualisation
        Etat_L, Etat_C = ActualiserEtat(Etat_L, Etat_C)
    return S
