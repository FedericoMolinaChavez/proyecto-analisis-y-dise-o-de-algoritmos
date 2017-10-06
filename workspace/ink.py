from sys import stdin
from math import sqrt
listaFiguras = []

def segment(a, b):
  return [a,b,point(b.getX()-a.getX(), b.getY()-a.getY())]

def distancia(a,b):
  return (sqrt((a.getX()-b.getX()) + (a.getY()-b.getY())))

def perp(v):
  b = point(v.getY(), -v.getX())
  return b

class dforest(object):  #creado por Camilo Rocha para la clase de Analisis y diseño de algoritmos 2016-2.

  def __init__(self,size=100):
    """create an emtpy forest"""
    self.__parent = [ i for i in range(size) ]
    self.__size = [ 1 for i in range(size) ]
    self.__rank = [ 0 for i in range(size) ]
    
  def __str__(self):
    """return the string representation of the forest"""
    return str(self.__parent)

  def __len__(self):
    """return the number of elements in the forest"""
    return len(self.__parent)
  
  def __contains__(self,x):
    """return if x is an element of the forest"""
    return 0 <= x < len(self)

  def find(self,x):
    """return the representative of the tree of x"""
    assert x in self
    if self.__parent[x]!=x:
      self.__parent[x] = self.find(self.__parent[x])
    return self.__parent[x]

  def union(self,x,y):
    """make the union of the trees of x and y"""
    assert x in self and y in self
    rx,ry = self.find(x),self.find(y)
    if rx!=ry:
      nx,ny = self.__rank[rx],self.__rank[ry]
      if nx<=ny:
        self.__parent[rx] = ry
        self.__size[ry] += self.__size[rx]
        if nx==ny: self.__rank[ry]+=1
      else:
        self.__parent[ry] = rx
        self.__size[rx] += self.__size[ry]
        
  def size(self,x):
    """return the size of the tree of x"""
    assert x in self
    return self.__size[self.find(x)]

class point():
    x,y = 0,0
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
class pol():
    listPuntos,listEdges = [],[]
    funion = dforest(1)
    def __init__(self,listaPuntos):
        self.listEdges = []
        self.listPuntos = listaPuntos
        lenl = len(listaPuntos)
        #print(lenl,"tamaño lista dentro de pol")
        for i in range(lenl-1) :
          self.listEdges.append(segment(listaPuntos[i], listaPuntos[i+1]))
        self.listEdges.append(segment(listaPuntos[0],listaPuntos[lenl-1]))
        #print(len(self.listEdges),"tam lista edges")
    def getEdges(self):
      return self.listEdges
    def getPuntos(self):
      return self.listPuntos
      
def normalize(v):
  mag = sqrt(v.getX()*v.getX() + v.getY()*v.getY())
 
  b = point(v.getX()/mag, v.getY()/mag) 
  return b
        
def projection(pol, axis):
  axis = normalize(axis)
  minn = dotProduct(pol.getPuntos()[0],axis)
  maxx = minn
  for i in pol.getPuntos():
    proj = dotProduct(i,axis)
    if(proj<minn): minn = proj
    if(proj>maxx): maxx = proj
  projec = [minn,maxx]  
  return projec

def contains(n, ran):
  #print (ran)
  a = ran[0]
  b = ran[1]
  if(b<a): 
    a=b 
    b=ran[0]
  return (n>=a and n <= b)



def overlap (a , b):
  if (contains(a[0],b)): return 1
  if (contains(a[1],b)): return 1
  if (contains(b[0],a)): return 1
  if (contains(b[1],a)): return 1
  return 0        
def dotProduct(a,b):
  #print (a.x)
 # print (b.x)
  c = a.x*b.x + a.y*b.y
  return c


        
def sat (a, b):
  c = a.getEdges()
  d = b.getEdges()
 # print ("tam",len(c))
  #print ("tam",len (d))
  cont = 0
  for i in c:
    axis = i[2]
    axis = perp(axis)
    a1 = projection(a,axis)
    a2 = projection(b,axis)
    if (overlap(a1,a2) == 0): return 0

  cont = 0
  for i in d:
    axis = i[2]
    axis = perp(axis)
    a1 = projection(a,axis)
    a2 = projection(b,axis)
    if (overlap(a1,a2) == 0): return 0 
 
  return 1



def solve(num):
    global listaFiguras
    
    ans = []
    suma = 0
    funion = dforest(num)
    for i in range (num):
       for j in range (i,num):
           a = sat(listaFiguras[i],listaFiguras[j])
           if (a == 1):
             #print (i,j)
             funion.union(i,j)
   
    for j in range(num):
        a = funion.find(j)
        if(a not in ans):
          ans.append(a)
          suma += 1
    return suma
    
    
def main():
    global listaFiguras
    imp = stdin
    num = int(imp.readline().strip()) 
    while(num != 0):
        listaPuntos = []
        for j in range(num):
            linea = imp.readline().strip().split()
            for i in range(0,len(linea),2):
                x = int(linea[i])
                y = int(linea[i+1])
                punto = point(x,y)
               # print(punto.getX(),punto.getY())
                listaPuntos.append(punto)
           # print(len(listaPuntos), "tamaño previo")
            poligono = pol(listaPuntos)
            listaFiguras.append(poligono)
            listaPuntos = []
        print(solve(num))
        num = int(imp.readline().strip())
        listaFiguras = []
            
main()        
        
        
        