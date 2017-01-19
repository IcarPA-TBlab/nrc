# LA LIBRERIA RICAVA UNA RAPPRESENTAZIONE DELLA SEQUENZA SOTTO FORMA DI MATRICE, METTENDO ASSIEME
# TUTE LE FREQUENZE DI UNA LISTA DI KMERI
import numpy as np

def findKmers(sequenza, K):
    """ 
    trova i k meri considerando anche le espansioni
    """
    sost={ "r":["g", "a"] , "y":["t","c"], "k":["g", "t"], "m":["a", "c"], "s":["g", "c"], "w":["a", "t"], "b":["g", "t", "c"], "d":["g", "a", "t"], "h":["a", "c", "t"], "v":["g", "c", "a"], "n":["a", "g", "c", "t"]}
    end=len(sequenza)
    out=[]
    for i in range(end-K+1):
        kmer=sequenza[i:i+K]  # sequenza candidata
        temp=[]     
        for k in kmer:          
            if k in sost.keys():
                temp.append(sost[k])
                
            else:
                temp.append([k])       
        out.append(temp) # out e' la lista impacchettata 
    out2=[]
    for o in out:
        temp=o[0]
        for i in range(1,len(o)):
            temp=[t+l for t in temp for l in o[i]]
        out2.extend(temp)
    return out2


#==============================================================================
def Kmer2Binary(kmer, Tabella):
    """
    trasforma il kmer in una stringa binaria seguendo la tabella
    """
    out=[]
    for k in kmer:
        out.append(Tabella[k])
    return ''.join(out)


#==============================================================================
def bin2RC(binario):
    """ 
    dal valore binario estrae coordinate righe e colonne
    i bit dispari (converititi in decimali) costituiscono il numero di riga
    i bit pari (convertiti in decimale) costituiscono il numero di colonna
    """
    pari=binario[0::2]  # estrae i bit pari facendo lo slicing ==> some_list[start:stop:step]
    dispari=binario[1::2]  

    r=int(''.join(pari), 2)
    c=int(''.join(dispari), 2)
    
    return (r,c)


#==============================================================================
def getMatrice(sequenza, k):
    Tabella={'a':'00', 'c':'01', 'g':'10', 't':'11' } # definisco la tabella per la conversione
    dim=2**k
   
    # genera la matrice di rappresentazione
    m3=np.zeros((dim,dim))
    
    KMERI=findKmers(sequenza, k)
    for kmer in KMERI:
        
        # genera la sequenza binaria
        binario=[]
        for km in kmer:
            binario.append(Tabella[km])
        sbinario="".join(binario)
        
        pari=sbinario[0::2]  # estrae i bit pari facendo lo slicing ==> some_list[start:stop:step]
        dispari=sbinario[1::2]  

        r=int(''.join(pari), 2)
        c=int(''.join(dispari), 2)
        
        m3[r][c] += 1
    
    return m3


#==============================================================================
def espandiMatrice(m):
    """
    A partire da m genera una matrice di dimensioni 2m ricopiando i valori 
    a blocchetti quadrati
    """
    R, C = m.shape
    out=np.zeros((2*R, 2*C))
    for r in range(R):
        for c in range(C):
            x=m[r][c]
            for r1 in range(2*r, 2*r+2):
                for c1 in range(2*c, 2*c+2):
                    out[r1][c1]+=x
    return out


#==============================================================================
def getComplexRepr(sequenza, K):
    """
    Crea la rappresentazione ottenuta dalla somma delle varie rappresentazioni 
    in una unica matrice. K e' la lista delle dimensioni dei k-mers.
    """
    m_init=getMatrice(sequenza, K[0])
    dim=2**K[-1]
    #out=np.zeros((dim, dim))
    for ki in K[1:]:
        m_init=espandiMatrice(m_init)
        # divido gli elementi per due per diminuire l'impatto dei termini 
        # piu' corti e quindi piu' comuni
        m_init /= 2.0
        temp=getMatrice(sequenza, ki)
        m_init=np.add(m_init,temp)
    return m_init
    
